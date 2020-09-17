import pygame as pg
from modules.component import Component
from modules.entitystate import EntityState, Direction


class UserControlComponent(Component):
    """Handles user input which modifies the state,
    velocity and direction of the Entity sprite."""

    def __init__(self, entity):
        super().__init__()
        self.entity = entity

        self.ZERO_VELOCITY = 0
        self.WALK_LEFT_VELOCITY = -180
        self.WALK_RIGHT_VELOCITY = 180
        self.JUMP_VELOCITY = -750
        self.CLIMB_UP_VELOCITY = -120
        self.CLIMB_DOWN_VELOCITY = 180

    def update(self):
        """Updates the state, direction and velocity
        of the entity based on the user input."""
        is_pressed = pg.key.get_pressed()
        state = self.entity.get_state()
        if state is EntityState.IDLE:
            self.handle_idle_entity(is_pressed)
        elif state is EntityState.WALKING:
            self.handle_walking_entity(is_pressed)
        elif state is EntityState.JUMPING:
            self.handle_jumping_entity(is_pressed)
        elif state is EntityState.HANGING:
            self.handle_hanging_entity(is_pressed)
        if self.entity.get_state() is EntityState.CLIMBING:
            self.handle_climbing_entity(is_pressed)

    def handle_idle_entity(self, is_pressed: dict):
        self.entity.set_x_velocity(self.ZERO_VELOCITY)
        self.entity.set_y_velocity(self.ZERO_VELOCITY)
        if is_pressed[pg.K_LEFT]:
            self.entity.set_state(EntityState.WALKING)
            self.entity.set_direction(Direction.LEFT)
            self.entity.set_x_velocity(self.WALK_LEFT_VELOCITY)
        if is_pressed[pg.K_RIGHT]:
            self.entity.set_state(EntityState.WALKING)
            self.entity.set_direction(Direction.RIGHT)
            self.entity.set_x_velocity(self.WALK_RIGHT_VELOCITY)
        if is_pressed[pg.K_SPACE]:
            self.entity.set_state(EntityState.JUMPING)
            self.entity.set_y_velocity(self.JUMP_VELOCITY)
            self.entity.message("JUMP")

    def handle_walking_entity(self, is_pressed: dict):
        if is_pressed[pg.K_LEFT]:
            self.entity.set_direction(Direction.LEFT)
            self.entity.set_x_velocity(self.WALK_LEFT_VELOCITY)
        if is_pressed[pg.K_RIGHT]:
            self.entity.set_direction(Direction.RIGHT)
            self.entity.set_x_velocity(self.WALK_RIGHT_VELOCITY)
        if not (is_pressed[pg.K_LEFT] or is_pressed[pg.K_RIGHT]):
            self.entity.set_state(EntityState.IDLE)
            self.entity.set_x_velocity(self.ZERO_VELOCITY)
        if is_pressed[pg.K_SPACE]:
            self.entity.set_state(EntityState.JUMPING)
            self.entity.set_y_velocity(self.JUMP_VELOCITY)
            self.entity.message("JUMP")

    def handle_jumping_entity(self, is_pressed: dict):
        if is_pressed[pg.K_LEFT]:
            self.entity.set_x_velocity(self.WALK_LEFT_VELOCITY)
            self.entity.set_direction(Direction.LEFT)
        if is_pressed[pg.K_RIGHT]:
            self.entity.set_x_velocity(self.WALK_RIGHT_VELOCITY)
            self.entity.set_direction(Direction.RIGHT)
        if not (is_pressed[pg.K_LEFT] or is_pressed[pg.K_RIGHT]):
            self.entity.set_x_velocity(self.ZERO_VELOCITY)

    def handle_hanging_entity(self, is_pressed: dict):
        self.entity.set_x_velocity(self.ZERO_VELOCITY)
        self.entity.set_y_velocity(self.ZERO_VELOCITY)
        if is_pressed[pg.K_UP] or is_pressed[pg.K_DOWN]:
            self.entity.set_state(EntityState.CLIMBING)
        if is_pressed[pg.K_LEFT]:
            self.entity.set_direction(Direction.RIGHT)
        if is_pressed[pg.K_RIGHT]:
            self.entity.set_direction(Direction.LEFT)
        if is_pressed[pg.K_SPACE]:
            self.entity.set_state(EntityState.JUMPING)
            self.entity.set_y_velocity(self.JUMP_VELOCITY)
            self.entity.message("JUMP")

    def handle_climbing_entity(self, is_pressed: dict):
        if is_pressed[pg.K_UP]:
            self.entity.set_y_velocity(self.CLIMB_UP_VELOCITY)
        if is_pressed[pg.K_DOWN]:
            self.entity.set_y_velocity(self.CLIMB_DOWN_VELOCITY)
        if not (is_pressed[pg.K_UP] or is_pressed[pg.K_DOWN]):
            self.entity.set_state(EntityState.HANGING)


class EnemyMovementComponent(Component):
    """Handles the back and forth movement of
    the Enemy sprites between two points."""

    def __init__(self, walking_speed=90):
        super().__init__()
        self.walking_speed = walking_speed

    def update(self, enemy):
        enemy.set_state(EntityState.WALKING)
        if enemy.get_direction() is Direction.LEFT:
            if enemy.rect.x > enemy.left_bound:
                enemy.set_x_velocity(-self.walking_speed)
            else:
                enemy.reverse_direction()
                enemy.set_x_velocity(self.walking_speed)
        elif enemy.get_direction() is Direction.RIGHT:
            if enemy.rect.x < enemy.right_bound:
                enemy.set_x_velocity(self.walking_speed)
            else:
                enemy.reverse_direction()
                enemy.set_x_velocity(-self.walking_speed)


class PhysicsComponent(Component):
    """Handles the physics of the Entity, which comprises of its
    acceleration due to gravity, its movement due to its velocity,
    and its collisions with the terrain and map boundaries."""

    def __init__(self):
        super().__init__()
        self.GRAVITY = 60

    def update(self, delta_time, entity, game_map):
        """Positions the entity at its future position, and handles all
        collisions between the entity and other sprites."""

        # TODO: Consider splitting this component into GravityComponent
        #  and RigidBodyComponent to fulfill Single Responsibility Principle
        # TODO: Make the discrete timestep logic more readable.

        DISCRETE_TIMESTEP = 1 / 60
        num_full_steps = int(delta_time / DISCRETE_TIMESTEP)
        remainder_time = delta_time % DISCRETE_TIMESTEP

        for i in range(0, num_full_steps):
            if entity.get_state() is not EntityState.CLIMBING \
                    and entity.get_state() is not EntityState.HANGING:
                entity.y_velocity += int(self.GRAVITY * DISCRETE_TIMESTEP * 60)
            entity.rect.y += int(entity.y_velocity * DISCRETE_TIMESTEP)
            self.handle_y_collisions(entity, game_map)
            entity.rect.x += int(entity.x_velocity * DISCRETE_TIMESTEP)
            self.handle_x_collisions(entity, game_map)

        if entity.get_state() is not EntityState.CLIMBING \
                and entity.get_state() is not EntityState.HANGING:
            entity.y_velocity += int(self.GRAVITY * remainder_time * 60)
        entity.rect.y += int(entity.y_velocity * remainder_time)
        if int(entity.y_velocity * remainder_time) != 0:
            self.handle_y_collisions(entity, game_map)
        entity.rect.x += int(entity.x_velocity * remainder_time)
        self.handle_x_collisions(entity, game_map)

        self.handle_map_boundary_collisions(entity, game_map)

    @staticmethod
    def handle_y_collisions(entity, map):
        """Handles collisions between entity and the terrain along the y-axis."""
        isJumping = True
        colliding_sprites = pg.sprite.spritecollide(
            entity, map.collideable_terrain_group, False)
        for colliding_sprite in colliding_sprites:
            if is_colliding_from_below(entity, colliding_sprite):
                entity.rect.top = colliding_sprite.rect.bottom
                entity.set_y_velocity(0)
            if is_colliding_from_above(entity, colliding_sprite):
                isJumping = False
                if entity.get_state() is EntityState.JUMPING:
                    entity.set_state(EntityState.IDLE)
                entity.rect.bottom = colliding_sprite.rect.top
                entity.set_y_velocity(0)
        if entity.get_state() is not EntityState.CLIMBING \
                and entity.get_state() is not EntityState.HANGING:
            if isJumping:
                entity.set_state(EntityState.JUMPING)

    @staticmethod
    def handle_x_collisions(entity, map):
        """Handles collisions between entity and the terrain along the x-axis."""
        colliding_sprites = pg.sprite.spritecollide(
            entity, map.collideable_terrain_group, False)
        for colliding_sprite in colliding_sprites:
            if not colliding_sprite.is_spike:
                if is_colliding_from_right(entity, colliding_sprite):
                    entity.rect.left = colliding_sprite.rect.right
                if is_colliding_from_left(entity, colliding_sprite):
                    entity.rect.right = colliding_sprite.rect.left

    @staticmethod
    def handle_map_boundary_collisions(entity, map):
        """Handles collisions between entity and the boundaries of the map."""
        map_width = map.rect.width
        if entity.rect.top < 0:
            entity.rect.top = 0
        if entity.rect.left < 0:
            entity.rect.left = 0
        elif entity.rect.right > map_width:
            entity.rect.right = map_width


class EnemyPhysicsComponent(PhysicsComponent):
    def __init__(self):
        super().__init__()

    @staticmethod
    def handle_x_collisions(enemy, map):
        """Handles collisions between the enemy and the terrain
        along the x-axis. Enemies would reverse its direction
        and velocity upon collision with a sprite."""
        colliding_sprites = pg.sprite.spritecollide(
            enemy, map.collideable_terrain_group, False)
        for colliding_sprite in colliding_sprites:
            if is_colliding_from_right(enemy, colliding_sprite):
                enemy.rect.left = colliding_sprite.rect.right
                enemy.set_direction(Direction.RIGHT)
            if is_colliding_from_left(enemy, colliding_sprite):
                enemy.rect.right = colliding_sprite.rect.left
                enemy.set_direction(Direction.LEFT)
            enemy.reverse_x_velocity()



def is_colliding_from_below(entity, colliding_sprite):
    return colliding_sprite.rect.top < entity.rect.top < colliding_sprite.rect.bottom


def is_colliding_from_above(entity, colliding_sprite):
    return colliding_sprite.rect.top < entity.rect.bottom < colliding_sprite.rect.bottom


def is_colliding_from_right(entity, colliding_sprite):
    return colliding_sprite.rect.left < entity.rect.left < colliding_sprite.rect.right


def is_colliding_from_left(entity, colliding_sprite):
    return colliding_sprite.rect.left < entity.rect.right < colliding_sprite.rect.right
