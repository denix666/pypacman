from helpersAndConstants import *
from player import Player


class IntroView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        intro_texture = arcade.load_texture(resource_path("images/intro.png"))
        arcade.draw_texture_rectangle(intro_texture.width // 2,
                                      intro_texture.height // 2, SCREEN_WIDTH, SCREEN_HEIGHT, intro_texture)

        # Show intro and instructions for game
        arcade.draw_text("SPACE - Shoot", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.YELLOW, font_size=33, anchor_x="center")
        arcade.draw_text("Up, Down, Left, Right - walk", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 210,
                         arcade.color.YELLOW, font_size=33, anchor_x="center")
        arcade.draw_text("Hit  SPACE  to  start  game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 300,
                         arcade.color.YELLOW, font_size=50, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ESCAPE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()

        self.game_view = game_view

    def on_draw(self):
        arcade.draw_rectangle_filled(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, 420, 70, arcade.color.BLACK)
        arcade.draw_text("Game  paused", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.GREEN, font_size=35, anchor_x="center")

        arcade.draw_text("Press  any  key  to  continue", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20,
                         arcade.color.GREEN, font_size=25, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        self.window.show_view(self.game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.csscolor.BLACK)

        # Game variables
        self.end_game = None
        self.level = None
        self.tile_map = None
        self.scene = None
        self.physics_engine = None

        self.player_list = None
        self.player_sprite = None
        self.player_pos_x = PLAYER_INIT_X
        self.player_pos_y = PLAYER_INIT_Y

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.last_direction = None
        self.cur_direction = None

        self.check_sprite = None
        self.check_sprite_list = None

    def setup(self):
        self.end_game = False
        self.level = 1
        self.cur_direction = "right"

        layer_options = {
            "Walls": {
                "use_spatial_hash": False,
            },
        }
        self.tile_map = arcade.load_tilemap(resource_path("maps/map_" + str(self.level) + ".json"), TILE_SCALING,
                                            layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.player_list = arcade.SpriteList()
        self.player_sprite = Player("left")
        self.player_sprite.center_x = self.player_pos_x
        self.player_sprite.center_y = self.player_pos_y
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Walls"]
        )

        self.check_sprite_list = arcade.SpriteList()
        self.check_sprite = arcade.Sprite(resource_path("images/check_sprite.png"), 0.4)
        self.check_sprite.center_x = 100
        self.check_sprite.center_y = 100
        self.check_sprite_list.append(self.check_sprite)

    def on_draw(self):
        arcade.start_render()
        self.scene.draw()
        self.check_sprite_list.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if can_go_left(self, self.player_sprite.center_x, self.player_sprite.center_y):
                self.cur_direction = "left"

        if key == arcade.key.UP:
            if can_go_up(self, self.player_sprite.center_x, self.player_sprite.center_y):
                self.cur_direction = "up"

        if key == arcade.key.RIGHT:
            if can_go_right(self, self.player_sprite.center_x, self.player_sprite.center_y):
                self.cur_direction = "right"

        if key == arcade.key.DOWN:
            if can_go_down(self, self.player_sprite.center_x, self.player_sprite.center_y):
                self.cur_direction = "down"

        if key == arcade.key.ESCAPE:
            if self.end_game:
                menu_view = IntroView()
                self.window.show_view(menu_view)
            else:
                pause = PauseView(self)
                self.window.show_view(pause)

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.scene.update_animation(
            delta_time, ["Player"]
        )

        # Moving player
        if self.cur_direction == "right":
            self.player_sprite.face_direction = "right"
            self.player_sprite.center_x += PLAYER_MOVEMENT_SPEED

        if self.cur_direction == "left":
            self.player_sprite.face_direction = "left"
            self.player_sprite.center_x -= PLAYER_MOVEMENT_SPEED

        if self.cur_direction == "up":
            self.player_sprite.face_direction = "up"
            self.player_sprite.center_y += PLAYER_MOVEMENT_SPEED

        if self.cur_direction == "down":
            self.player_sprite.face_direction = "down"
            self.player_sprite.center_y -= PLAYER_MOVEMENT_SPEED


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
