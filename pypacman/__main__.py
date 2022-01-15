from pypacman.helpersAndConstants import *
from pypacman.game import IntroView
import arcade


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = IntroView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
