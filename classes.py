from typing import Any
import colors
from pygame import Vector2
from math import sin, cos, radians

class Tile:
    innerColor = None
    outerColor = None
    innerWidth = None

    def __init__ (self, _inner_color, _outer_color, _inner_width = 0):
        # Set tile colors
        self.innerColor, self.outerColor = _inner_color, _outer_color
        self.innerWidth = _inner_width

class Grid:
    tileSize = 64
    innerMargin = 5
    cornerRadius = 5
    # map size: 25x15
    map = [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
            [1,0,2,2,2,2,2,2,2,0,0,0,0,4,0,0,2,0,0,0,0,0,0,0,1 ],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,4,0,0,2,0,0,0,0,1,0,0,1 ],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1,0,0,1 ],
            [1,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,1,0,0,1 ],
            [1,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
            [1,0,0,0,3,3,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
            [1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1 ],
            [1,0,0,0,0,4,4,4,0,0,0,0,0,0,0,2,0,0,0,0,0,0,4,0,1 ],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,4,4,4,4,0,1 ],
            [1,0,0,0,0,0,0,0,0,0,3,3,3,3,0,2,0,0,0,0,0,0,4,0,1 ],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1 ] ]
    tiles=[ Tile(colors.night, colors.gray, 5),
            Tile(colors.red, colors.maroon, 5),
            Tile(colors.yellow, colors.peach, 5),
            Tile(colors.green, colors.mint, 2),
            Tile(colors.sapphire, colors.lavender, 10) ] 

class Angle:
    @staticmethod
    def SerializeAngle(_angle: int | float):
        if _angle >= 360:
            _angle -= 360
        elif _angle < 0:
            _angle += 360
        return _angle

class Hit:
    bHit = False
    x = 0
    y = 0
    tile_x = 0
    tile_y = 0
    tileID = 0
    distance = 0
    recurence_level = 0

class Player:
    # & variables
    #   * Move SECTION
    x = 0
    y = 0
    mov_speed = 10
    fov = 40

    #   * Rot SECTION
    angle = 0
    rot_speed = 6
    
    #   * Draw SECTION
    #   * dw - draw | dwc - draw_color
    dw_radius = 8
    dw_width = 3

    dw_look_start_offset_ratio = 0.9
    dw_look_length = 30
    dw_look_width = 2

    dwc_player = colors.player
    dwc_look = colors.look

    #   * DEBUG SECTION
    dbg_render_player = True
    dbg_render_grid = True
    dbg_render_horizontal_points = False
    dbg_render_vertical_points = False
    dbg_render_final_ray = True
    dbg_render_tile_ray = True
    dbg_render_scene = False

    # & Vector2 Getters
    @property
    def pos(self):
        return Vector2(self.x,self.y)
    
    @property
    def direction(self):
        return Vector2(sin(radians(self.angle)), cos(radians(self.angle)))
    
    # & Functions
    def Move(self, _x, _y):
        self.x += _x
        self.y += _y

    def Move(self, _delta: Vector2):
        self.x += _delta.x
        self.y += _delta.y

    def SetPosition(self, _x: int | float, _y: int | float):
        self.x = _x
        self.y = _y

    def SetPosition(self, _position: Vector2):
        self.x = _position.x
        self.y = _position.y