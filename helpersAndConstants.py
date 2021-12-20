import os
import arcade

SCREEN_WIDTH = 1150
SCREEN_HEIGHT = 750
SCREEN_TITLE = "PyPacman v0.1 dev"

# Constants used to scale our sprites from their original size
TILE_SCALING = 1
PLAYER_SCALING = 1

PLAYER_INIT_X = 75
PLAYER_INIT_Y = 75

PLAYER_ANIMATION_SPEED = 9
PLAYER_MOVEMENT_SPEED = 3

ENEMY_ANIMATION_SPEED = 7
ENEMY_MOVEMENT_SPEED = 3


def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def can_go_left(self, sprite_pos_x, sprite_pos_y):
    self.check_sprite.center_x = sprite_pos_x - 20
    self.check_sprite.center_y = sprite_pos_y
    if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
        return False
    else:
        return True


def can_go_right(self, sprite_pos_x, sprite_pos_y):
    self.check_sprite.center_x = sprite_pos_x + 20
    self.check_sprite.center_y = sprite_pos_y
    if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
        return False
    else:
        return True


def can_go_up(self, sprite_pos_x, sprite_pos_y):
    self.check_sprite.center_x = sprite_pos_x
    self.check_sprite.center_y = sprite_pos_y + 20
    if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
        return False
    else:
        return True


def can_go_down(self, sprite_pos_x, sprite_pos_y):
    self.check_sprite.center_x = sprite_pos_x
    self.check_sprite.center_y = sprite_pos_y - 20
    if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
        return False
    else:
        return True
