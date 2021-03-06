import pygame as pg
from .entitystate import EntityState, Direction, EntityMessage
from .animation import EntityAnimationComponent
from .component import SoundComponent, RenderComponent, HealthComponent, DeathComponent, EnemyCombatComponent
from .physics import UserControlComponent, EntityGravityComponent, EntityRigidBodyComponent
from .libraries import Library


class Entity(pg.sprite.Sprite):
    # TODO: Make a EntityPhysics and EntityStateManager object

    def __init__(self):
        super().__init__()
        self.x_velocity = 0              
        self.y_velocity = 0
        self.direction = Direction.RIGHT
        self.state = EntityState.IDLE
        self.image = None

    def update(self, *args):
        raise NotImplementedError

    def message(self, message):
        raise NotImplementedError

    def set_x_velocity(self, new_x_velocity):
        self.x_velocity = new_x_velocity

    def reverse_x_velocity(self):
        self.x_velocity = -self.x_velocity

    def set_y_velocity(self, new_y_velocity):
        self.y_velocity = new_y_velocity

    def get_direction(self):
        return self.direction

    def set_direction(self, new_direction: Direction):
        self.direction = new_direction

    def reverse_direction(self):
        self.set_direction(self.get_direction().get_reverse())

    def get_state(self):
        return self.state

    def set_state(self, new_state: EntityState):
        self.state = new_state


class Player(Entity):

    DEFAULT_STARTING_POS = (10, 10)

    def __init__(self, starting_position=DEFAULT_STARTING_POS):
        super().__init__()
        self.blit_rect = pg.Rect(15, 3.5, 20, 30)
        self.rect = pg.Rect(starting_position, (self.blit_rect.width, self.blit_rect.height))

        self.input_component = UserControlComponent(self)
        self.animation_component = EntityAnimationComponent(self, Library.player_animations)
        self.sound_component = SoundComponent(Library.entity_sounds)
        self.render_component = RenderComponent()
        self.health_component = HealthComponent(self)
        self.gravity_component = EntityGravityComponent()
        self.rigid_body_component = EntityRigidBodyComponent()
        self.death_component = DeathComponent(self)

    def message(self, message: EntityMessage):
        self.sound_component.receive(message)
        self.health_component.receive(message)
        self.death_component.receive(message)

    def update(self, delta_time, map):
        self.input_component.update()
        self.animation_component.update()
        self.gravity_component.update(self, delta_time)
        self.rigid_body_component.update(self, delta_time, map)
        self.health_component.update()
        self.death_component.update(map)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface)


class Enemy(Entity):

    def __init__(self, type_object, ai_component, render_component, starting_position):
        super().__init__()
        self.ai_component = ai_component
        self.render_component = render_component
        self.gravity_component = EntityGravityComponent()
        self.rigid_body_component = EntityRigidBodyComponent()
        self.animation_component = EntityAnimationComponent(self, type_object.animation_library)
        self.sound_component = SoundComponent(type_object.sound_library)
        self.death_component = DeathComponent(self, is_game_over=False)
        self.combat_component = EnemyCombatComponent(self)

        self.blit_rect = type_object.blit_rect
        self.rect = pg.Rect(starting_position, (self.blit_rect.width, self.blit_rect.height))
        self.image = self.animation_component.get_initial_image()

    def message(self, message):
        self.ai_component.receive(message, self)
        self.death_component.receive(message)
    
    def update(self, delta_time, map, player):
        self.ai_component.update(self, map)
        self.gravity_component.update(self, delta_time)
        self.combat_component.update(player)
        self.rigid_body_component.update(self, delta_time, map)
        self.animation_component.update()
        self.death_component.update(map)

    def render(self, camera, surface):
        self.render_component.update(self, camera, surface)


class EnemyType:
    """Template object representing the type of enemy, which
    is passed into the Enemy constructor to instantiate an
    Enemy with the corresponding visuals, health and sounds."""

    def __init__(self):
        self.health = 100
        self.animation_library = {}
        self.sound_library = Library.entity_sounds


class PinkGuy(EnemyType):
    def __init__(self):
        super().__init__()
        self.blit_rect = pg.Rect(0, 0, 32, 32)
        self.animation_library = Library.pink_guy_animations


class TrashMonster(EnemyType):
    def __init__(self):
        super().__init__()
        self.blit_rect = pg.Rect(4, 0, 35, 32)
        self.animation_library = Library.trash_monster_animations


class ToothWalker(EnemyType):
    def __init__(self):
        super().__init__()
        self.blit_rect = pg.Rect(40, 0, 30, 65)
        self.animation_library = Library.tooth_walker_animations
