import decimal

import arcade
from math import *
import random
from decimal import Decimal as Dec

decimal.getcontext().prec = 4

SPRITE_SCALING = 1
TILE_SCALING = 1.4
IMAGE_SIZE = 30
GLOBAL_SCALE = 1
SPRITE_SCALING *= GLOBAL_SCALE
TILE_SCALING *= GLOBAL_SCALE
SPRITE_SIZE = 45

SCREEN_HEIGHT = 720
SCREEN_WIDTH = round(SCREEN_HEIGHT * (16 / 9))
SCREEN_TITLE = "Test collisions"
FPS = 60

STEP = 4


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0



class Player(arcade.Sprite):
    """Player class"""

    def __init__(self, size, texture):
        super().__init__(texture, size)
        self.center_x = 0
        self.center_y = 0

        self.speed = 0
        self.change_x = 0
        self.change_y = 0


class Game(arcade.Window):
    """Main application class"""

    def __init__(self, width, height, title):
        """Initialize the game"""

        """Call the parent initializer function"""
        super().__init__(width, height, title, fullscreen=True, vsync=True, resizable=True, update_rate=1 / FPS)
        width = 1000
        height = 1000
        self.set_viewport(0, width, 0, height)

        """Scene object and scene info"""
        self.size_x = None
        self.size_y = None
        self.scene = None
        self.tilemap = None
        self.wall = None

        """GUI"""
        self.GUI = None

        "Main Camera"
        self.camera = None
        self.camera_position = None

        """Player"""
        self.player = None

        """Key presses and mouse presses"""
        self.z = None
        self.s = None
        self.q = None
        self.d = None
        self.space = None

        """Pause flag"""
        self.pause = None

        """Physics"""
        self.physics = None

        """Things"""
        self.gravity = None
        self.fps = None
        self.count = None

    def setup(self):
        """Set up the game and initialize the variables"""

        """Camera"""
        self.camera = arcade.Camera(self.width, self.height)
        self.GUI = arcade.Camera(self.width, self.height)


        """Setup map"""

        map_path = "assets/collisions.tmj"

        layer_options = {"Walls": {"use_spatial_hash": True}}

        self.tilemap = arcade.load_tilemap(map_path, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        self.size_x = self.tilemap.width * self.tilemap.tile_width * TILE_SCALING
        self.size_y = self.tilemap.height * self.tilemap.tile_height * TILE_SCALING

        # Setup Player
        self.player = Player(SPRITE_SCALING, "assets/player.png")
        self.player.center_x = 640
        self.player.center_y = 1000
        self.scene.add_sprite("Player", self.player)

        # Physics
        self.physics = arcade.PhysicsEngineSimple(self.player, None)

        # Pause
        self.pause = False

        # things
        self.gravity = True
        self.wall = self.scene["Walls"]
        self.fps = 0
        self.count = 0

    def drawd(self, text, x, y):
        arcade.draw_text(text, x, self.height - y, arcade.color.WHITE, 30)


    def on_draw(self):
        """Render the screen."""

        # This command has to happen before we start drawing
        self.clear()

        # Draw the scene
        self.camera.use()
        self.scene.draw()
        arcade.draw_line(self.player.center_x, self.player.center_y, self.player.center_x + self.player.change_x * 3,
                         self.player.center_y + self.player.change_y * 3, (255, 255, 255), 3)

        self.GUI.use()
        self.drawd(f"speed x: {self.player.change_x}", 10, 30)
        self.drawd(f"speed y: {self.player.change_y}", 10, 60)
        self.drawd(f"fps: {self.fps}", 10, 90)


    def on_key_press(self, key, modifiers):
        """Key presses"""
        """movement keys"""
        if key == arcade.key.Z:
            self.z = True
        elif key == arcade.key.S:
            self.s = True
        elif key == arcade.key.D:
            self.d = True
        elif key == arcade.key.Q:
            self.q = True

        # Pause the game
        elif key == arcade.key.SPACE:
            self.pause = not self.pause

        """key to quit the game"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        """movement keys"""
        if key == arcade.key.Z:
            self.z = False
        elif key == arcade.key.S:
            self.s = False
        elif key == arcade.key.D:
            self.d = False
        elif key == arcade.key.Q:
            self.q = False

    def center_camera(self, sprite):
        self.camera_position = sprite.center_x - (self.width / 2), sprite.center_y - (self.height / 2)
        self.camera.move_to(self.camera_position)

    def on_update(self, delta_time: float):
        """ Movement and game logic """

        # move player
        if self.z:
            self.player.change_y += 0.6

        if self.q:
            self.player.change_x -= 0.6

        if self.s:
            self.player.change_y -= 0.6

        if self.d:
            self.player.change_x += 0.6

        self.player.speed = int(sqrt((self.player.change_x ** 2 + self.player.change_y ** 2)))

        if not self.pause:
            if abs(self.player.change_y) < 0.4:
                self.player.change_y = 0

            if abs(self.player.change_x) < 0.4:
                self.player.change_x = 0

            for i in range(STEP):
                # Gravity
                if self.gravity:
                    self.player.change_y -= 1 / STEP

                # check y collision
                self.player.center_y += self.player.change_y / STEP
                hit = arcade.check_for_collision_with_list(self.player, self.wall)
                if hit:
                    while arcade.check_for_collision_with_list(self.player, self.wall):
                        self.player.center_y -= sign(self.player.change_y)
                    self.player.change_y /= -1.2
                    self.player.change_x /= 1.15

                # check x collision
                self.player.center_x += self.player.change_x / STEP
                hit = arcade.check_for_collision_with_list(self.player, self.wall)
                if hit:
                    while arcade.check_for_collision_with_list(self.player, self.wall):
                        self.player.center_x -= sign(self.player.change_x)
                    self.player.change_x /= -1.01

            if self.player.center_x > self.size_x:
                self.player.center_x = 0
                self.player.center_y += 1

            if self.player.center_x < 0:
                self.player.center_x = self.size_x
                self.player.center_y += 1

        # center camera on player
        self.center_camera(self.player)

        self.count += 1
        if self.count == FPS // 3:
            self.fps = int(1 / delta_time)
            self.count = 0


def main():
    """ Main function """
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()
