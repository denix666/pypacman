from pypacman.helpersAndConstants import *


class Eyes(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.scale = ENEMY_SCALING
        self.cur_texture = 0
        self.update_interval = 0
        self.direction = None
        self.turn_x = None
        self.turn_y = None
        self.center_area_x = None
        self.center_area_y = None
        self.possible_moves_list = []
        self.scared_mode = False
        self.number_of_textures_in_animation = 2
        self.time_on_air = 0

        self.right_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/eyes/eaten_right_%s.png" % i))
            self.right_textures.append(texture)

        self.left_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/eyes/eaten_left_%s.png" % i))
            self.left_textures.append(texture)

        self.up_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/eyes/eaten_up_%s.png" % i))
            self.up_textures.append(texture)

        self.down_textures = []
        for i in range(3):
            texture = arcade.load_texture(resource_path("images/eyes/eaten_down_%s.png" % i))
            self.down_textures.append(texture)

        self.texture = self.right_textures[0]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        # Eyes animation
        self.update_interval += 1
        if self.update_interval > ENEMY_ANIMATION_SPEED:
            self.update_interval = 0

            if self.direction == "down":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.down_textures[self.cur_texture]
            elif self.direction == "up":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.up_textures[self.cur_texture]
            elif self.direction == "right":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.right_textures[self.cur_texture]
            elif self.direction == "left":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                self.texture = self.left_textures[self.cur_texture]
