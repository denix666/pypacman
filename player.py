from helpersAndConstants import *


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = PLAYER_SCALING
        self.center_x = PLAYER_INIT_X
        self.center_y = PLAYER_INIT_Y
        self.cur_texture = 0
        self.update_interval = 0
        self.number_of_textures_in_animation = 2
        self.direction = "left"

        self.walk_right_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/player/r_%s.png" % i))
            self.walk_right_textures.append(texture)

        self.walk_left_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/player/l_%s.png" % i))
            self.walk_left_textures.append(texture)

        self.walk_up_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/player/u_%s.png" % i))
            self.walk_up_textures.append(texture)

        self.walk_down_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/player/d_%s.png" % i))
            self.walk_down_textures.append(texture)

        self.texture = self.walk_right_textures[0]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        # Animation
        self.update_interval += 1
        if self.update_interval > PLAYER_ANIMATION_SPEED:
            self.update_interval = 0

            if self.direction == "down":
                self.cur_texture += 1
                if self.cur_texture > self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.walk_down_textures[self.cur_texture]
            elif self.direction == "up":
                self.cur_texture += 1
                if self.cur_texture > self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.walk_up_textures[self.cur_texture]
            elif self.direction == "right":
                self.cur_texture += 1
                if self.cur_texture > self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.walk_right_textures[self.cur_texture]
            elif self.direction == "left":
                self.cur_texture += 1
                if self.cur_texture > self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.walk_left_textures[self.cur_texture]

        # Walk
        if self.direction == "down":
            self.center_y -= PLAYER_MOVEMENT_SPEED

        if self.direction == "up":
            self.center_y += PLAYER_MOVEMENT_SPEED

        if self.direction == "right":
            self.center_x += PLAYER_MOVEMENT_SPEED

        if self.direction == "left":
            self.center_x -= PLAYER_MOVEMENT_SPEED


class PlayerExplosion(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = PLAYER_SCALING
        self.current_texture = 0
        self.update_interval = 0
        self.animation_completed = False

        # Load textures for enemy
        self.player_animation_textures = []
        for i in range(15):
            texture = arcade.load_texture(resource_path("images/animations/player_die/%s.png" % i))
            self.player_animation_textures.append(texture)
        self.textures = self.player_animation_textures

    def update(self):
        self.update_interval += 1
        if self.update_interval > PLAYER_EXPLOSION_ANIMATION_SPEED:
            self.update_interval = 0
            self.current_texture += 1
            if self.current_texture < len(self.textures):
                self.set_texture(self.current_texture)
            else:
                self.remove_from_sprite_lists()
                self.animation_completed = True
