import pygame
from math import *
from classes import *
from colors import night as night_color

# TODO: Add debug system for raycasting
# TODO: Add tile recognition to raycasting
# TODO: Add recurence to raycasting

# TODO: Minimap in second window and lock_in possibility based on windows location to each other
# TODO: Add customizable inner_tile margin and inner_tile coner radius to Tile Class

# ! Initialize PYGAME
pygame.init()
screen = pygame.display.set_mode((1600, 960))
clock = pygame.time.Clock()
running = True

everysecond_event = pygame.event.Event(100)
pygame.time.set_timer(everysecond_event, 1000)

font = pygame.font.Font(size=26)

resDump = 1

# & Functions
def GetGridCenter (_grid: Grid):
    center_tile_y = int(len(_grid.map) / 2)
    center_tile_x = int(len(_grid.map[center_tile_y]) / 2)
    # return Vector2(center_tile_x * _grid.tileSize + _grid.tileSize * 0.5,
    #                center_tile_y * _grid.tileSize + _grid.tileSize * 0.5)
    return Vector2(center_tile_x * _grid.tileSize, center_tile_y * _grid.tileSize) # Set center on tiles cross

def DebugOnScreen():
    player_pos_x_text = font.render("pos_x: " + str(p.x), False, colors.white)
    player_pos_y_text = font.render("pos_y: " + str(p.y), False, colors.white)
    
    player_rot_angle_text = font.render("angle: " + str(p.angle), False, colors.white)
    player_rot_direction_text = font.render("direction:" , False, colors.white)
    player_rot_direction_x_text = font.render("         x: " + str(p.direction.x) , False, colors.white)
    player_rot_direction_y_text = font.render("         y: " + str(p.direction.y) , False, colors.white)

    screen.blit(player_pos_x_text, Vector2(40, 20))
    screen.blit(player_pos_y_text, Vector2(40, 20 + player_pos_x_text.get_height()))

    screen.blit(player_rot_angle_text, Vector2(40, 20 + 10 + player_pos_x_text.get_height() + player_pos_y_text.get_height()))
    screen.blit(player_rot_direction_text, Vector2(40, 20 + 10 + player_pos_x_text.get_height() + player_pos_y_text.get_height() + player_rot_angle_text.get_height()))
    screen.blit(player_rot_direction_x_text, Vector2(40, 20 + 10 + player_pos_x_text.get_height() + player_pos_y_text.get_height() + player_rot_angle_text.get_height() + player_rot_direction_text.get_height()))
    screen.blit(player_rot_direction_y_text, Vector2(40, 20 + 10 + player_pos_x_text.get_height() + player_pos_y_text.get_height() + player_rot_angle_text.get_height() + player_rot_direction_text.get_height() + player_rot_direction_x_text.get_height()))

def GetVerticalAxis (_angle: int | float):
    if _angle > 90 and _angle < 270: # * facing UP
        return -1
    elif _angle != 90 and _angle != 270: # * facing down
        return 1
    else:
        return 0
def GetHorizontalAxis (_angle: int | float):
    if _angle > 0 and _angle < 180: # * facing LEFT
        return 1
    elif _angle != 0 and _angle != 180: # * facing RIGHT
        return -1
    else:
        return 0

def CastVerticalRay(_start_pos: Vector2, _angle: int | float, height: int | float = None, recurnece_index: int = 0):
    axis = GetVerticalAxis(_angle)
    nearestPoint_Height = height
    hit = Hit()
    recurence_limit = 20

    # * Apply height correction when facing down
    # *     and return empty hit when v_axis = 0
    # // Maybe add axis to startpoint so when standing at tiles cross nearest point never will be in player center
    if nearestPoint_Height == None:
        if axis == -1: # * facing UP
            nearestPoint_Height = (int(_start_pos.y      + axis) >> 6) << 6
        elif axis == 1: # * facing DOWN
            nearestPoint_Height = (int(_start_pos.y + 63 + axis) >> 6) << 6
            # slower but more accurate
            # if _start_pos.y % 64 != 0:
            #     nearestPoint_Height -= 64
        else:
            return Hit()

    nearestPoint_Width = (_start_pos.y - nearestPoint_Height) * -tan(radians(_angle)) + _start_pos.x
    # pygame.draw.circle(screen, colors.mint, Vector2(_start_pos.x, nearestPoint_Height), 3)
    if p.dbg_render_vertical_points:
        pygame.draw.circle(screen, colors.green, Vector2(nearestPoint_Width, nearestPoint_Height), 3)

    hit.x = nearestPoint_Width
    hit.y = nearestPoint_Height
    hit.tile_x = (int(hit.x) >> 6)
    hit.tile_y = (int(hit.y) >> 6)

    # * correct tile_y based on player v_axis
    if axis == -1:
        hit.tile_y -= 1

    # * clamp tile_x and tile_y indexes to grid size
    if hit.tile_y >= len(grid.map):
        hit.tile_y = len(grid.map) - 1
    elif hit.tile_y < 0:
        hit.tile_y = 0

    if hit.tile_x >= len(grid.map[hit.tile_y]) - 1:
        hit.tile_x = len(grid.map[hit.tile_y]) - 1
    elif hit.tile_x < 0:
        hit.tile_x = 0

    hit.distance = (_start_pos - Vector2(hit.x, hit.y)).length()
    hit.tileID = grid.map[hit.tile_y][hit.tile_x]

    if hit.tileID == 0 and recurnece_index < recurence_limit:
        return CastVerticalRay(_start_pos, _angle, nearestPoint_Height + grid.tileSize * axis, recurnece_index + 1)
    else:
        hit.recurence_level = recurnece_index
        hit.bHit = True
        return hit
def CastHoriznotalRay(_start_pos: Vector2, _angle: int | float, width: int | float = None, recurence_index: int = 0):
    axis = GetHorizontalAxis(_angle)
    nearestPoint_Width = width
    hit = Hit()
    recurence_limit = 25

    # * Apply width correction when facing right
    # *     and return empty hit when h_axis = 0
    # // Maybe add axis to startpoint so when standing at tiles cross nearest point never will be in player center
    if nearestPoint_Width == None:
        if axis == -1:
            nearestPoint_Width = (int(_start_pos.x       + axis) >> 6) << 6
        elif axis == 1:
            nearestPoint_Width = (int(_start_pos.x + 63  + axis) >> 6) << 6
            # slower but more accurate
            # if _start_pos.y % 64 != 0:
            #     nearestPoint_Height -= 64
        elif axis == 0:
            return Hit()
    
    nearestPoint_Height = (_start_pos.x - nearestPoint_Width) * tan(radians(_angle + 90)) + _start_pos.y
    # pygame.draw.circle(screen, colors.sky, Vector2(nearestPoint_Width, _start_pos.y), 3)
    if p.dbg_render_horizontal_points:
        pygame.draw.circle(screen, colors.lavender, Vector2(nearestPoint_Width, nearestPoint_Height), 3)

    hit.x = nearestPoint_Width
    hit.y = nearestPoint_Height
    hit.tile_x = (int(hit.x) >> 6)
    hit.tile_y = (int(hit.y) >> 6)

    # * correct tile_x based on player h_axis
    if axis == -1:
        hit.tile_x -= 1
        
    # * clamp tile_x and tile_y indexes to grid size
    if hit.tile_y >= len(grid.map):
        hit.tile_y = len(grid.map) - 1
    elif hit.tile_y < 0:
        hit.tile_y = 0

    if hit.tile_x >= len(grid.map[hit.tile_y]) - 1:
        hit.tile_x = len(grid.map[hit.tile_y]) - 1
    elif hit.tile_x < 0:
        hit.tile_x = 0

    hit.distance = (_start_pos - Vector2(hit.x, hit.y)).length()

    hit.tileID = grid.map[hit.tile_y][hit.tile_x]

    if hit.tileID == 0 and recurence_index < recurence_limit:
        return CastHoriznotalRay(_start_pos, _angle, nearestPoint_Width + grid.tileSize * axis, recurence_index + 1)
    else:
        hit.recurence_level = recurence_index
        hit.bHit = True
        return hit

def Raycast(_start_pos: Vector2, _angle: int | float):
    vertical_hit = CastVerticalRay(_start_pos, _angle)
    horizontal_hit = CastHoriznotalRay(_start_pos, _angle)
    vertical_recurence_level = font.render("vertical_recurence: " + str(vertical_hit.recurence_level), False, colors.white)
    horizontal_recurence_level = font.render("horizontal_recurence: " + str(horizontal_hit.recurence_level), False, colors.white)

    screen.blit(vertical_recurence_level, Vector2(20, 250))
    screen.blit(horizontal_recurence_level, Vector2(20, 250 + vertical_recurence_level.get_height()))


    # * DEBUG ON SCREEN
    vertical_hit_text = font.render("vertical_hit: tileID: " + str(vertical_hit.tileID) + "  distance: " + str(vertical_hit.distance) + "   bHit: " + str(vertical_hit.bHit), False, colors.white)
    horizontal_hit_text = font.render("horizontal_hit: tileID: " + str(horizontal_hit.tileID) + "  distance: " + str(horizontal_hit.distance) + "   bHit: " + str(horizontal_hit.bHit), False, colors.white)
    screen.blit(vertical_hit_text, Vector2(20, 150))
    screen.blit(horizontal_hit_text, Vector2(20, 150 + vertical_hit_text.get_height()))

    if not vertical_hit.bHit:
        return horizontal_hit
    
    if not horizontal_hit.bHit:
        return vertical_hit
    
    if vertical_hit.distance < horizontal_hit.distance:
        return vertical_hit
    else:
        return horizontal_hit

# & Instantiate game elements
grid = Grid()
p = Player()
p.SetPosition(GetGridCenter(grid))

while running:
    # & EVENTS
    # *     Events Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == everysecond_event.type:
            pygame.display.set_caption(str(int(clock.get_fps())))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                p.dbg_render_scene = not p.dbg_render_scene
            if event.key == pygame.K_h:
                p.dbg_render_horizontal_points = not p.dbg_render_horizontal_points
            if event.key == pygame.K_v:
                p.dbg_render_vertical_points = not p.dbg_render_vertical_points
            if event.key == pygame.K_p:
                p.dbg_render_player = not p.dbg_render_player
            if event.key == pygame.K_f:
                p.dbg_render_final_ray = not p.dbg_render_final_ray
            if event.key == pygame.K_t:
                p.dbg_render_tile_ray = not p.dbg_render_tile_ray
            if event.key == pygame.K_g:
                p.dbg_render_grid = not p.dbg_render_grid

    # *     Keyboard Inputs Handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        p.Move(p.direction * p.mov_speed)
    if keys[pygame.K_s]:
        p.Move(-p.direction * p.mov_speed)
    if keys[pygame.K_a]:
        p.Move(-p.direction.rotate(90) * p.mov_speed)
    if keys[pygame.K_d]:
        p.Move(p.direction.rotate(90) * p.mov_speed)

    if keys[pygame.K_LEFT]:
        p.angle = Angle.SerializeAngle(p.angle + p.rot_speed)
    if keys[pygame.K_RIGHT]:
        p.angle = Angle.SerializeAngle(p.angle - p.rot_speed)

    # & Render Game
    screen.fill(night_color)
    
    # 4000 x 0.08           --- fisheye
    # 3000 x sqrt(distance) --- no fisheye

    base_wall_heigh = 16000 * 4
    if p.dbg_render_scene:
        # * Color sky and ground
        top_layer = pygame.Rect(0,0, screen.get_width(), screen.get_height() / 2)
        bottom_layer = pygame.Rect(0,screen.get_height() / 2, screen.get_width(), screen.get_height())

        pygame.draw.rect(screen, colors.ceiling, top_layer)
        pygame.draw.rect(screen, colors.ground, bottom_layer)

        # * Render screen
        for i in range(int(screen.get_width() / resDump)):
            hit = Raycast(p.pos, Angle.SerializeAngle(p.angle - p.fov / 2 + p.fov / screen.get_width() * i * resDump))
            wall_height = base_wall_heigh / (hit.distance)
            pygame.draw.line(screen, grid.tiles[hit.tileID].innerColor, Vector2(screen.get_width() - i * resDump - 1, (screen.get_height() - wall_height) / 2), Vector2(screen.get_width() - i * resDump - 1, (screen.get_height() - wall_height) / 2 + wall_height), resDump)
    # *     Display grid
    if p.dbg_render_grid:
        for y in range(len(grid.map)):
            for x in range(len(grid.map[y])):
                tileID = grid.map[y][x]
                # Draw outer rectangle
                rect = pygame.Rect( x * grid.tileSize, y * grid.tileSize, grid.tileSize, grid.tileSize)
                pygame.draw.rect(screen, grid.tiles[tileID].outerColor, rect, 0, grid.cornerRadius)
                # Draw inner rectangle with rounded corners
                rect = pygame.Rect( x * grid.tileSize + grid.innerMargin / 2, y * grid.tileSize + grid.innerMargin / 2,
                                    grid.tileSize - grid.innerMargin, grid.tileSize - grid.innerMargin)
                pygame.draw.rect(screen, grid.tiles[tileID].innerColor, rect, grid.tiles[tileID].innerWidth, grid.cornerRadius)

    # *     Render Player
    if p.dbg_render_player:
        pygame.draw.circle(screen, p.dwc_player, p.pos, p.dw_radius, p.dw_width)    # draw player circle
        pygame.draw.line(screen, p.dwc_look,                                        # draw direction ray
                        p.pos + p.direction * p.dw_radius * p.dw_look_start_offset_ratio,      # start pos
                        p.pos + p.direction * p.dw_look_length,                                # end pos
                        p.dw_look_width)                                                       # diretion indicator width

    hit = Raycast(p.pos, p.angle)
    if p.dbg_render_final_ray:
        pygame.draw.line(screen, colors.lavender, p.pos, Vector2(hit.x, hit.y))
    if p.dbg_render_tile_ray:
        pygame.draw.line(screen, colors.mint, p.pos, Vector2(hit.tile_x * grid.tileSize + grid.tileSize * 0.5, hit.tile_y * grid.tileSize + grid.tileSize * 0.5))

    DebugOnScreen()

    pygame.display.flip()
    clock.tick(60)  #* limits FPS to 60

pygame.quit()
