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


def resource_path(relative_path):
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
