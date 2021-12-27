from helpersAndConstants import *


class Enemy(arcade.Sprite):
    def __init__(self, enemy_type):
        super().__init__()

        self.scale = ENEMY_SCALING
        self.cur_texture = 0
        self.update_interval = 0
        self.number_of_textures_in_animation = 2
        self.enemy_type = enemy_type
        self.direction = None
        self.turn_x = None
        self.turn_y = None
        self.center_area_x = None
        self.center_area_y = None
        self.possible_moves_list = []
        self.scared_mode = False

        # Regular textures ####################################################################################
        self.walk_right_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/%s_right_%s.png" % (self.enemy_type, i)))
            self.walk_right_textures.append(texture)

        self.walk_left_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/%s_left_%s.png" % (self.enemy_type, i)))
            self.walk_left_textures.append(texture)

        self.walk_up_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/%s_up_%s.png" % (self.enemy_type, i)))
            self.walk_up_textures.append(texture)

        self.walk_down_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/%s_down_%s.png" % (self.enemy_type, i)))
            self.walk_down_textures.append(texture)

        # Scared textures ####################################################################################
        self.scared_walk_right_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/scared_right_%s.png" % i))
            self.scared_walk_right_textures.append(texture)

        self.scared_walk_left_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/scared_left_%s.png" % i))
            self.scared_walk_left_textures.append(texture)

        self.scared_walk_up_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/scared_up_%s.png" % i))
            self.scared_walk_up_textures.append(texture)

        self.scared_walk_down_textures = []
        for i in range(2):
            texture = arcade.load_texture(resource_path("images/enemy/scared_down_%s.png" % i))
            self.scared_walk_down_textures.append(texture)

        self.texture = self.walk_right_textures[0]
        self.hit_box = self.texture.hit_box_points

    def update(self):
        # Enemy animation
        self.update_interval += 1
        if self.update_interval > ENEMY_ANIMATION_SPEED:
            self.update_interval = 0

            if self.direction == "down":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                if not self.scared_mode:
                    self.texture = self.walk_down_textures[self.cur_texture]
                else:
                    self.texture = self.scared_walk_down_textures[self.cur_texture]
            elif self.direction == "up":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                if not self.scared_mode:
                    self.texture = self.walk_up_textures[self.cur_texture]
                else:
                    self.texture = self.scared_walk_up_textures[self.cur_texture]
            elif self.direction == "right":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                if not self.scared_mode:
                    self.texture = self.walk_right_textures[self.cur_texture]
                else:
                    self.texture = self.scared_walk_right_textures[self.cur_texture]
            elif self.direction == "left":
                self.cur_texture += 1
                if self.cur_texture == self.number_of_textures_in_animation:
                    self.cur_texture = 0
                if not self.scared_mode:
                    self.texture = self.walk_left_textures[self.cur_texture]
                else:
                    self.texture = self.scared_walk_left_textures[self.cur_texture]
