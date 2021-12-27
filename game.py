import random

from helpersAndConstants import *
from player import Player, PlayerExplosion
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


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game  over!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150,
                         arcade.color.YELLOW, font_size=60, anchor_x="center")
        arcade.draw_text("Hit  SPACE  to  start  new  game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 250,
                         arcade.color.YELLOW, font_size=35, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE or key == arcade.key.ESCAPE:
            game_view = GameView()
            GameView().score = 0
            GameView().lives = 3
            GameView().level = 1
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
        self.level_fail = None
        self.level = 1
        self.score = 0
        self.lives = 3
        self.tile_map = None
        self.scene = None
        self.physics_engine = None
        self.scared_mode = None
        self.player_explosion = None
        self.player_explosion_list = None

        self.map = None

        # Player
        self.player_sprite = None

        # Enemy
        self.enemy_sprite = None

        # Some "sprite helper" to check if player can move up/down/left/right
        self.check_sprite = None
        self.check_sprite_list = None

        # Coin lists
        self.small_coin_list = None
        self.big_coin_list = None

    def setup(self):
        self.end_game = False
        self.scared_mode = False

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

        # Player die animation
        self.player_explosion = PlayerExplosion()
        self.player_explosion_list = arcade.SpriteList()

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Walls"]
        )

        # Init check sprite helper item (It used to check it there are collision with walls in various scenarios)
        self.check_sprite_list = arcade.SpriteList()
        self.check_sprite = arcade.Sprite(resource_path("images/check_sprite.png"), 0.4)  # 0.4
        self.check_sprite_list.append(self.check_sprite)

        # Create map arrays depended on tiled map
        for ix in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for iy in range(int((SCREEN_HEIGHT - 50) / TILE_SIZE)):
                self.check_sprite.center_x = TILE_SIZE * ix + TILE_SIZE / 2
                self.check_sprite.center_y = TILE_SIZE * iy + TILE_SIZE / 2
                if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["Walls"]):
                    self.map["wall", ix, iy] = True
                else:
                    self.map["wall", ix, iy] = False

                if arcade.check_for_collision_with_list(self.check_sprite, sprite_list=self.scene["big_coins"]):
                    self.map["big_coin", ix, iy] = True
                else:
                    self.map["big_coin", ix, iy] = False

        # Init small coin items
        for ix in range(int(SCREEN_WIDTH / TILE_SIZE)):
            for iy in range(int((SCREEN_HEIGHT - 50) / TILE_SIZE)):
                if not self.map["wall", ix, iy] and not self.map["big_coin", ix, iy]:
                    self.map["small_coin", ix, iy] = True
                else:
                    self.map["small_coin", ix, iy] = False

        if not self.level_fail:
            self.small_coin_list = arcade.SpriteList()
            self.big_coin_list = arcade.SpriteList()
            for ix in range(int(SCREEN_WIDTH / TILE_SIZE)):
                for iy in range(int((SCREEN_HEIGHT - 50) / TILE_SIZE)):
                    if self.map["big_coin", ix, iy]:
                        big_coin_sprite = arcade.Sprite(resource_path("images/big_coin.png"), 1)
                        big_coin_sprite.center_x = TILE_SIZE * ix + TILE_SIZE / 2
                        big_coin_sprite.center_y = TILE_SIZE * iy + TILE_SIZE / 2
                        self.big_coin_list.append(big_coin_sprite)

                    if self.map["small_coin", ix, iy]:
                        small_coin_sprite = arcade.Sprite(resource_path("images/small_coin.png"), 1)
                        small_coin_sprite.center_x = TILE_SIZE * ix + TILE_SIZE / 2
                        small_coin_sprite.center_y = TILE_SIZE * iy + TILE_SIZE / 2
                        self.small_coin_list.append(small_coin_sprite)
        self.level_fail = False

        # Place enemy in random places
        for i in range(self.level * STARTING_AMOUNT_OF_ENEMY):
            item_placed_successfully = False
            while not item_placed_successfully:
                self.enemy_sprite = Enemy(random.choice(["red", "pinc", "blue", "green"]))
                self.enemy_sprite.direction = random.choice(["right", "left", "up", "down"])
                e = random.choice(list(self.map.keys()))
                if not self.map["wall", e[1], e[2]]:
                    self.enemy_sprite.center_x = e[1] * TILE_SIZE + TILE_SIZE / 2
                    self.enemy_sprite.center_y = e[2] * TILE_SIZE + TILE_SIZE / 2
                    if self.enemy_sprite.center_y != 75:  # Avoid to place enemy on the first row together with player
                        if self.enemy_sprite.direction in possible_moves(self.map,
                                                                         self.enemy_sprite.center_x,
                                                                         self.enemy_sprite.center_y,
                                                                         self.enemy_sprite.direction):
                            self.enemy_sprite.turn_x = 0
                            self.enemy_sprite.turn_y = 0
                            self.scene.add_sprite("Enemies", self.enemy_sprite)
                            item_placed_successfully = True

    def on_draw(self):
        arcade.start_render()

        self.small_coin_list.draw()
        self.big_coin_list.draw()
        self.scene.draw()
        self.player_explosion_list.draw()

        # Show score and current level number
        arcade.draw_text(f"Score: {self.score}", 10, SCREEN_HEIGHT - 35, arcade.color.YELLOW, 15)
        arcade.draw_text(f"Level: {self.level}", 260, SCREEN_HEIGHT - 35, arcade.color.WHITE, 15)

        # Show lives
        live_texture = arcade.load_texture(resource_path("images/player/r_1.png"))
        if self.lives >= 10:
            lives_to_draw = 10
        else:
            lives_to_draw = self.lives - 1

        for i in range(0, lives_to_draw):
            y = SCREEN_HEIGHT - live_texture.height
            x = (SCREEN_WIDTH - 50) - i * live_texture.height
            arcade.draw_texture_rectangle(live_texture.width // 2 + x,
                                          live_texture.height // 2 + y,
                                          live_texture.width,
                                          live_texture.height,
                                          live_texture, 0)

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

        # Check if player collided with enemy
        self.player_explosion_list.update()
        player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, sprite_list=self.scene["Enemies"])
        if len(player_hit_list) > 0:
            self.level_fail = True

            # Remove player and enemy from the field
            for en in player_hit_list:
                en.remove_from_sprite_lists()
            self.player_sprite.remove_from_sprite_lists()

            # Player die animation
            self.player_explosion.center_y = self.player_sprite.center_y
            self.player_explosion.center_x = self.player_sprite.center_x
            self.player_explosion_list.append(self.player_explosion)

        if self.player_explosion.animation_completed:
            arcade.pause(1)
            self.lives -= 1
            if self.lives < 1:
                game_view = GameOverView()
                self.window.show_view(game_view)
            else:
                self.setup()

        self.scene.update(
            ["Enemies"]
        )

        # Check if we eat coin increase score and remove coin from list
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.small_coin_list)
        for hit in coin_hit_list:
            hit.remove_from_sprite_lists()
            self.score += 10

        # Check if we eat big coin increase score and remove coin from list and enable scared mode for enemy
        big_coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.big_coin_list)
        for hit in big_coin_hit_list:
            hit.remove_from_sprite_lists()
            self.score += 50
            self.scared_mode = True

        # Moving enemies
        if not self.level_fail:
            for en in self.scene["Enemies"]:
                # Check if we are entered into scared enemy mode
                if self.scared_mode:
                    en.scared_mode = True
                    enemy_movement_speed = ENEMY_MOVEMENT_SPEED - 1
                else:
                    en.scared_mode = False
                    enemy_movement_speed = ENEMY_MOVEMENT_SPEED

                # Get the center of the tile
                en.center_area_x = int(en.center_x / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2
                en.center_area_y = int(en.center_y / TILE_SIZE) * TILE_SIZE + TILE_SIZE / 2

                # If we are not in the tile where decision was already taken - choose again random turn direction
                if int(en.center_x / TILE_SIZE) != en.turn_x or int(en.center_y / TILE_SIZE) != en.turn_y:
                    en.possible_moves_list = possible_moves(self.map, en.center_x, en.center_y, en.direction)

                # Increase possibility to get player or escape in scared mode
                if not self.scared_mode:
                    if en.center_x > self.player_sprite.center_x:
                        if "left" in en.possible_moves_list:
                            en.possible_moves_list.extend(["left"]*7)

                    if en.center_x < self.player_sprite.center_x:
                        if "right" in en.possible_moves_list:
                            en.possible_moves_list.extend(["right"]*7)

                    if en.center_y > self.player_sprite.center_y:
                        if "down" in en.possible_moves_list:
                            en.possible_moves_list.extend(["down"]*7)

                    if en.center_y < self.player_sprite.center_y:
                        if "up" in en.possible_moves_list:
                            en.possible_moves_list.extend(["up"]*7)
                else:
                    if en.center_x > self.player_sprite.center_x:
                        if "right" in en.possible_moves_list:
                            en.possible_moves_list.extend(["right"] * 7)

                    if en.center_x < self.player_sprite.center_x:
                        if "left" in en.possible_moves_list:
                            en.possible_moves_list.extend(["left"] * 7)

                    if en.center_y > self.player_sprite.center_y:
                        if "up" in en.possible_moves_list:
                            en.possible_moves_list.extend(["up"] * 7)

                    if en.center_y < self.player_sprite.center_y:
                        if "down" in en.possible_moves_list:
                            en.possible_moves_list.extend(["down"] * 7)

                if en.direction == "right":
                    en.center_x += enemy_movement_speed
                    if len(en.possible_moves_list) > 0:
                        if en.center_x >= en.center_area_x:
                            en.center_x = en.center_area_x
                            en.direction = random.choice(en.possible_moves_list)
                            en.turn_x = int(en.center_x / TILE_SIZE)
                            en.turn_y = int(en.center_y / TILE_SIZE)
                            en.possible_moves_list = []

                if en.direction == "left":
                    en.center_x -= enemy_movement_speed
                    if len(en.possible_moves_list) > 0:
                        if en.center_x <= en.center_area_x:
                            en.center_x = en.center_area_x
                            en.direction = random.choice(en.possible_moves_list)
                            en.turn_x = int(en.center_x / TILE_SIZE)
                            en.turn_y = int(en.center_y / TILE_SIZE)
                            en.possible_moves_list = []

                if en.direction == "up":
                    en.center_y += enemy_movement_speed
                    if len(en.possible_moves_list) > 0:
                        if en.center_y >= en.center_area_y:
                            en.center_y = en.center_area_y
                            en.direction = random.choice(en.possible_moves_list)
                            en.turn_x = int(en.center_x / TILE_SIZE)
                            en.turn_y = int(en.center_y / TILE_SIZE)
                            en.possible_moves_list = []

                if en.direction == "down":
                    en.center_y -= enemy_movement_speed
                    if len(en.possible_moves_list) > 0:
                        if en.center_y <= en.center_area_y:
                            en.center_y = en.center_area_y
                            en.direction = random.choice(en.possible_moves_list)
                            en.turn_x = int(en.center_x / TILE_SIZE)
                            en.turn_y = int(en.center_y / TILE_SIZE)
                            en.possible_moves_list = []
