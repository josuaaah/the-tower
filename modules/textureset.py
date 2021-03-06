import pygame as pg

"""
ADDING NEW TEXTURES TO THE TEXTURESET
--------------------------------------
1.  Add a new entry to the "textures" dictionary, with the string literal of the terrain type as the key
    and a TerrainType object containing the texture as the value
    Optional arguments can also be passed to the TerrainType constructor to specify the hitbox of the object 
    (this technically allows for larger objects to be instantiated)
2.  Add a new entry to the "code_to_textures_dictionary", with the string representation of the tile in the 
    .txt map file as the key, and the string literal of the terrain type as the value
"""

# TODO: Can implement reading from JSON to make this more modular

class TerrainType:
    """Stores a texture and its corresponding hitbox dimensions"""
    def __init__(self, image: pg.Surface, block_pos_x=0, block_pos_y=0, block_width=1, block_height=1):
        # All numbers are relative to the size of a normal block
        # (i.e. must be between 0 and 1, where 1 is the size of an actual block)
        self.image = image
        self.block_pos_x = block_pos_x
        self.block_pos_y = block_pos_y
        self.block_width = block_width
        self.block_height = block_height


class Tileset:
    """Utility class to load static textures from a spritesheet"""
    def __init__(self, filepath):
        self.spritesheet = pg.image.load(filepath)

    def get_image_at(self, rectangle, colorkey=None) -> pg.Surface:
        """Loads the image at the area specified by the given rectangle"""
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()

        # TODO: Convert to subsurface
        image.blit(self.spritesheet, (0, 0), rect)

        if colorkey is None:
            image.set_colorkey((0, 0, 0))
        else:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image


class TextureSet:
    """Contains a dictionary of the types of tiles and its corresponding TerrainType objects,
    and allows for the retrieval for the corresponding TerrainType object of the specified tile type"""
    def __init__(self):
        ruby = Tileset("assets/textures/environment/animated/ruby.png")
        tileset = Tileset("assets/textures/environment/static/terrain.png")
        decorations = Tileset("assets/textures/environment/static/decorations.png")
        self.textures = {
            # ------------------------------ INTERACTIVE BLOCKS ------------------------------ #
            "SPIKES_UPRIGHT": TerrainType(decorations.get_image_at(pg.Rect(208, 196, 32, 10)), 0, 0.7, 1, 0.3),
            "ENTRANCE/EXIT": TerrainType(tileset.get_image_at(pg.Rect(1584, 464, 32, 28)), 0, -0.5, 1, 1.5),
            "COIN": TerrainType(ruby.get_image_at(pg.Rect(0, 0, 15, 16)), 0.2, 0.2, 0.6, 0.6),
            "FALLING_BLOCK": TerrainType(tileset.get_image_at(pg.Rect(208, 672, 32, 32))),
            "MOVING_BLOCK": TerrainType(tileset.get_image_at(pg.Rect(1424, 656, 32, 32))),
            "LADDER": TerrainType(decorations.get_image_at(pg.Rect(184, 16, 32, 32))),
            "PUSHABLE": TerrainType(decorations.get_image_at(pg.Rect(209, 113, 14, 15))),

            # ------------------------------ COLLIDEABLE BLOCKS ------------------------------ #
            "CORNER_BOTTOM_LEFT":   TerrainType(tileset.get_image_at(pg.Rect(160, 720, 32, 32))),
            "CORNER_BOTTOM_RIGHT":  TerrainType(tileset.get_image_at(pg.Rect(512, 720, 32, 32))),
            "CORNER_TOP_LEFT_1":    TerrainType(tileset.get_image_at(pg.Rect(160, 448, 32, 32))),
            "CORNER_TOP_LEFT_2":    TerrainType(tileset.get_image_at(pg.Rect(192, 448, 32, 32))),
            "CORNER_TOP_LEFT_3":    TerrainType(tileset.get_image_at(pg.Rect(160, 480, 32, 32))),
            "CORNER_TOP_LEFT_4":    TerrainType(tileset.get_image_at(pg.Rect(192, 480, 32, 32))),
            "CORNER_TOP_RIGHT_1":   TerrainType(tileset.get_image_at(pg.Rect(480, 448, 32, 32))),
            "CORNER_TOP_RIGHT_2":   TerrainType(tileset.get_image_at(pg.Rect(512, 448, 32, 32))),
            "CORNER_TOP_RIGHT_3":   TerrainType(tileset.get_image_at(pg.Rect(480, 480, 32, 32))),
            "CORNER_TOP_RIGHT_4":   TerrainType(tileset.get_image_at(pg.Rect(512, 480, 32, 32))),
            "WALL_LEFT":            TerrainType(tileset.get_image_at(pg.Rect(160, 672, 32, 32))),
            "WALL_RIGHT":           TerrainType(tileset.get_image_at(pg.Rect(512, 672, 32, 32))),
            "CEILING":              TerrainType(tileset.get_image_at(pg.Rect(240, 448, 32, 32))),
            "FLOOR":                TerrainType(tileset.get_image_at(pg.Rect(240, 720, 32, 32))),
            "FLOOR_TOP_HALF":       TerrainType(tileset.get_image_at(pg.Rect(240, 720, 32, 16)), 0, 0.48, 1, 0.52),

            # ------------------------------ NON-COLLIDEABLE BLOCKS ------------------------------ #
            "BG_FILLER":               TerrainType(tileset.get_image_at(pg.Rect(48, 544, 32, 32))),
            "BG_WALL":              TerrainType(tileset.get_image_at(pg.Rect(1328, 472, 32, 32))),
            "BG_WALL_BOTTOM_HALF":  TerrainType(tileset.get_image_at(pg.Rect(1328, 488, 32, 16)), 0, 0.48, 1, 0.52),
            "BG_WINDOW_DOUBLE":    TerrainType(tileset.get_image_at(pg.Rect(1088, 240, 144, 128)), 0, 0, 4.5, 4),
            # single window adds one extra pixel to eliminate a hole
            "BG_WINDOW_SINGLE":     TerrainType(tileset.get_image_at(pg.Rect(1472, 96, 65, 64)), -0.5, -0.40625, 2, 2),
            # barred window adds one extra pixel to eliminate a hole
            "BG_WINDOW_BARRED":     TerrainType(tileset.get_image_at(pg.Rect(1552, 119, 32, 42)), 0, -0.28125, 1, 1.28125),
            "BG_SHELF_POTIONS":     TerrainType(decorations.get_image_at(pg.Rect(16, 64, 32, 64)), 0, -1, 1, 2),
            "BG_SHELF_BOOKS":       TerrainType(decorations.get_image_at(pg.Rect(16, 144, 32, 64)), 0, -1, 1, 2),
            "BG_SHELF_EMPTY":       TerrainType(decorations.get_image_at(pg.Rect(64, 144, 32, 64)), 0, -1, 1, 2),
            "BG_BANNER_RED_LARGE_1":  TerrainType(decorations.get_image_at(pg.Rect(304, 305, 112, 80)), -0.25, 0, 3.5, 2.5),
            "BG_BANNER_RED_LARGE_2": TerrainType(decorations.get_image_at(pg.Rect(496, 209, 112, 80)), -0.25, 0, 3.5, 2.5),

        }

        # TODO: Sort this in alphabetical order
        self.code_to_texture_dictionary = {"SP": "SPIKES_UPRIGHT",
                                           "GW": "ENTRANCE/EXIT",
                                           "CN": "COIN",
                                           "FB": "FALLING_BLOCK",
                                           "MB": "MOVING_BLOCK",
                                           "LB": "LADDER",
                                           "PB": "PUSHABLE",
                                           "f1": "FLOOR",
                                           "f2": "FLOOR_TOP_HALF",
                                           "l1": "WALL_LEFT",
                                           "r1": "WALL_RIGHT",
                                           "c1": "CEILING",
                                           "bl": "CORNER_BOTTOM_LEFT",
                                           "br": "CORNER_BOTTOM_RIGHT",
                                           "k1": "CORNER_TOP_LEFT_1",
                                           "k2": "CORNER_TOP_LEFT_2",
                                           "k3": "CORNER_TOP_LEFT_3",
                                           "k4": "CORNER_TOP_LEFT_4",
                                           "k5": "CORNER_TOP_RIGHT_1",
                                           "k6": "CORNER_TOP_RIGHT_2",
                                           "k7": "CORNER_TOP_RIGHT_3",
                                           "k8": "CORNER_TOP_RIGHT_4",
                                           "xx": "BG_FILLER",
                                           "wl": "BG_WALL",
                                           "wb": "BG_WALL_BOTTOM_HALF",
                                           "2w": "BG_WINDOW_DOUBLE",
                                           "1w": "BG_WINDOW_SINGLE",
                                           "bw": "BG_WINDOW_BARRED",
                                           "s1": "BG_SHELF_POTIONS",
                                           "s2": "BG_SHELF_BOOKS",
                                           "s3": "BG_SHELF_EMPTY",
                                           "b1": "BG_BANNER_RED_LARGE_1",
                                           "b2": "BG_BANNER_RED_LARGE_2"
                                           }

    def get_texture_from_code(self, code) -> TerrainType:
        """Returns the corresponding TerrainType object associated with the specified tile"""
        return self.textures[self.code_to_texture_dictionary[code]]