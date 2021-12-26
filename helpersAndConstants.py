import os
import arcade

SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 750
SCREEN_TITLE = "PyPacman v0.2 dev"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
TILE_SIZE = 50

PLAYER_SCALING = 1
PLAYER_INIT_X = 625
PLAYER_INIT_Y = 75
PLAYER_ANIMATION_SPEED = 9
PLAYER_MOVEMENT_SPEED = 3

ENEMY_ANIMATION_SPEED = 6
ENEMY_MOVEMENT_SPEED = 2
ENEMY_SCALING = 1
STARTING_AMOUNT_OF_ENEMY = 3


def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def can_go_left(check_sprite, walls, sprite_pos_x, sprite_pos_y):
    check_sprite.center_x = sprite_pos_x - 20
    check_sprite.center_y = sprite_pos_y
    if arcade.check_for_collision_with_list(check_sprite, sprite_list=walls):
        return False
    else:
        return True


def can_go_right(check_sprite, walls, sprite_pos_x, sprite_pos_y):
    check_sprite.center_x = sprite_pos_x + 20
    check_sprite.center_y = sprite_pos_y
    if arcade.check_for_collision_with_list(check_sprite, sprite_list=walls):
        return False
    else:
        return True


def can_go_up(check_sprite, walls, sprite_pos_x, sprite_pos_y):
    check_sprite.center_x = sprite_pos_x
    check_sprite.center_y = sprite_pos_y + 20
    if arcade.check_for_collision_with_list(check_sprite, sprite_list=walls):
        return False
    else:
        return True


def can_go_down(check_sprite, walls, sprite_pos_x, sprite_pos_y):
    check_sprite.center_x = sprite_pos_x
    check_sprite.center_y = sprite_pos_y - 20
    if arcade.check_for_collision_with_list(check_sprite, sprite_list=walls):
        return False
    else:
        return True


def possible_moves(map_of_level, x, y, cur_direction):
    possible_moves_list = []
    tile_x = int(x / TILE_SIZE)
    tile_y = int(y / TILE_SIZE)

    # Check if we can move up
    if not map_of_level["wall", tile_x, tile_y + 1] and cur_direction != "down":
        if "up" not in possible_moves_list:
            possible_moves_list.append("up")

    # Check if we can move down
    if not map_of_level["wall", tile_x, tile_y - 1] and cur_direction != "up":
        if "down" not in possible_moves_list:
            possible_moves_list.append("down")

    # Check if we can move right
    if not map_of_level["wall", tile_x + 1, tile_y] and cur_direction != "left":
        if "right" not in possible_moves_list:
            possible_moves_list.append("right")

    # Check if we can move left
    if not map_of_level["wall", tile_x - 1, tile_y] and cur_direction != "right":
        if "left" not in possible_moves_list:
            possible_moves_list.append("left")

    return possible_moves_list
