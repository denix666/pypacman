import random

from helpersAndConstants import *
from player import Player
from enemy import Enemy


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

        self.map = None

        # Player
        self.player_sprite = None

        # Enemy
        self.enemy_sprite = None

        # Some "sprite helper" to check if player can move up/down/left/right
        self.check_sprite = None
        self.check_sprite_list = None

        # Small coin
        self.small_coin_list = None

    def setup(self):
        self.end_game = False
        self.level = 1

        self.map = {}

        layer_options = {
            "Walls": {
                "use_spatial_hash": False,
            },
        }
        self.tile_map = arcade.load_tilemap(resource_path("maps/map_" + str(self.level) + ".json"), TILE_SCALING,
                                            layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Init player item
        self.player_sprite = Player()
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Walls"]
        )

        # Init check sprite helper item (It used to check it there are collision with walls in various scenarios)
        self.check_sprite_list = arcade.SpriteList()
        self.check_sprite = arcade.Sprite(resource_path("images/check_sprite.png"), 0.4)  # 0.4
        self.check_sprite_list.append(self.check_sprite)

        # Create map array depended on tiled map
        self.small_coin_list = arcade.SpriteList()
        for ix in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for iy in range(int((SCREEN_HEIGHT - 50) / TILE_SIZE)):
                self.check_sprite.center_x = TILE_SIZE * ix + TILE_SIZE / 2
                self.check_sprite.center_y = TILE_SIZE * iy + TILE_SIZE / 2
                if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
                    self.map["wall", ix, iy] = True
                else:
                    self.map["wall", ix, iy] = False

        # print(self.map["wall", 1, 1])

        # Init and add small coin items
        for ix in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for iy in range(int((SCREEN_HEIGHT - 50) / TILE_SIZE)):
                if not self.map["wall", ix, iy]:
                    coin_sprite = arcade.Sprite(resource_path("images/small_coin.png"), 1)
                    coin_sprite.center_x = TILE_SIZE * ix + TILE_SIZE / 2
                    coin_sprite.center_y = TILE_SIZE * iy + TILE_SIZE / 2
                    self.small_coin_list.append(coin_sprite)

        # Place enemy in random places
        for i in range(self.level * STARTING_AMOUNT_OF_ENEMY):
            item_placed_successfully = False
            while not item_placed_successfully:
                self.enemy_sprite = Enemy(random.choice(["red", "pinc", "blue"]))
                self.enemy_sprite.direction = random.choice(["right", "left", "up", "down"])
                e = random.choice(list(self.map.keys()))
                if not self.map["wall", e[1], e[2]]:
                    self.enemy_sprite.center_x = e[1] * TILE_SIZE + TILE_SIZE / 2
                    self.enemy_sprite.center_y = e[2] * TILE_SIZE + TILE_SIZE / 2
                    self.scene.add_sprite("Enemies", self.enemy_sprite)
                    item_placed_successfully = True

    def on_draw(self):
        arcade.start_render()
        self.small_coin_list.draw()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            if can_go_left(self.check_sprite, self.scene["Walls"],
                           self.player_sprite.center_x, self.player_sprite.center_y):
                self.player_sprite.direction = "left"

        if key == arcade.key.UP:
            if can_go_up(self.check_sprite, self.scene["Walls"],
                         self.player_sprite.center_x, self.player_sprite.center_y):
                self.player_sprite.direction = "up"

        if key == arcade.key.RIGHT:
            if can_go_right(self.check_sprite, self.scene["Walls"],
                            self.player_sprite.center_x, self.player_sprite.center_y):
                self.player_sprite.direction = "right"

        if key == arcade.key.DOWN:
            if can_go_down(self.check_sprite, self.scene["Walls"],
                           self.player_sprite.center_x, self.player_sprite.center_y):
                self.player_sprite.direction = "down"

        if key == arcade.key.ESCAPE:
            if self.end_game:
                menu_view = IntroView()
                self.window.show_view(menu_view)
            else:
                pause = PauseView(self)
                self.window.show_view(pause)

    def on_update(self, delta_time):
        self.physics_engine.update()

        self.scene.update(
            ["Player"]
        )

        self.scene.update(
            ["Enemies"]
        )

        # Check if we eat coin increase score and remove coin from list
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.small_coin_list)
        for hit in coin_hit_list:
            hit.remove_from_sprite_lists()

        for en in self.scene["Enemies"]:
            if en.direction == "right":
                en.center_x += ENEMY_MOVEMENT_SPEED
                if arcade.check_for_collision_with_list(en, sprite_list=self.scene["Walls"]):
                    en.center_x -= ENEMY_MOVEMENT_SPEED
                    en.direction = random.choice(["up", "down"])

            if en.direction == "left":
                en.center_x -= ENEMY_MOVEMENT_SPEED
                if arcade.check_for_collision_with_list(en, sprite_list=self.scene["Walls"]):
                    en.center_x += ENEMY_MOVEMENT_SPEED
                    en.direction = random.choice(["up", "down"])

            if en.direction == "down":
                en.center_y -= ENEMY_MOVEMENT_SPEED
                if arcade.check_for_collision_with_list(en, sprite_list=self.scene["Walls"]):
                    en.center_y += ENEMY_MOVEMENT_SPEED
                    en.direction = random.choice(["right", "left"])

            if en.direction == "up":
                en.center_y += ENEMY_MOVEMENT_SPEED
                if arcade.check_for_collision_with_list(en, sprite_list=self.scene["Walls"]):
                    en.center_y -= ENEMY_MOVEMENT_SPEED
                    en.direction = random.choice(["right", "left"])