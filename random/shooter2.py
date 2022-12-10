import decimal

import arcade
from math import *
import random
from decimal import Decimal as Dec

decimal.getcontext().prec = 4

SPRITE_SCALING = 0.3
TILE_SCALING = 1
IMAGE_SIZE = 30
GLOBAL_SCALE = 2
SPRITE_SCALING *= GLOBAL_SCALE
TILE_SCALING *= GLOBAL_SCALE
SPRITE_SIZE = 45

SCREEN_HEIGHT = 720
SCREEN_WIDTH = round(SCREEN_HEIGHT * (16 / 9))
SCREEN_TITLE = "Shooter 2"


class Player(arcade.Sprite):
    """Player initializer"""

    def __init__(self, image, scale):
        """Call the parent initializer and setup info related to parent"""
        super().__init__(image, scale)
        self.angle = 0
        self.center_x = 0
        self.center_y = 0
        """Setup custom info"""
        self.damage = Dec("0.5")
        self.move_speed = 3
        self.health = Dec("20")
        self.max_health = 20
        self.shoot = 0.1
        self.shoot_timer = 0
        self.shoot_spread = 7.5
        self.shoot_amount = 1
        self.money = 0


class Bullet(arcade.Sprite):
    """Bullet initializer"""

    def __init__(self, image, scale):
        """Call the parent initializer and setup info related to parent"""
        super().__init__(image, scale)
        self.angle = 0
        self.x = 0
        self.y = 0
        """Setup custom info"""
        self.speed = 10


class Enemy(arcade.Sprite):
    """Enemy initializer"""

    def __init__(self, image, scale):
        """Call the parent initializer and setup info related to parent"""
        super().__init__(image, scale)
        self.angle = 0
        self.x = 0
        self.y = 0
        """Setup custom info"""
        self.health = None
        self.spawn_heath = None
        self.damage = None
        self.speed = None
        self.friction = 0.5


class Game(arcade.Window):
    """Main application class"""

    def __init__(self, width, height, title):
        """Initialize the game"""

        """Call the parent initializer function"""
        super().__init__(width, height, title, fullscreen=True, vsync=True, resizable=True, update_rate=1 / 60)
        width = 10
        height = 10
        self.set_viewport(0, width, 0, height)

        """Scene object and scene info"""
        self.size_x = None
        self.size_y = None
        self.scene = None
        self.tilemap = None

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
        self.mouse_press = None

        """Bullet info"""
        self.bullet = None
        self.bullet_list = None
        self.hit_sprite = None

        """Mouse position"""
        self.mouse_position = None

        """Physics engines"""
        self.physics_engine = None
        self.enemy_physics_engine = None

        """Enemy related things"""
        self.enemy = None
        self.enemy_list = None
        self.spawn_time = None
        self.spawn_time_timer = None
        self.spawn_time_add = None
        self.enemy_damage = None
        self.enemy_speed = None
        self.enemy_health = None
        self.enemy_spawn_health = None
        self.enemy_damage_increase = None
        self.enemy_speed_increase = None
        self.enemy_spawn_health_increase = None
        self.spawn_time_add_add = None
        self.money_drop = None

        """Pause flag"""
        self.pause = None

    def setup(self):
        """Set up the game and initialize the variables"""

        """Set up the GUI"""
        self.GUI = arcade.Camera(self.width, self.height)

        """Set up the main camera"""
        self.camera = arcade.Camera(self.width, self.height)

        """Set up the camera"""
        map_name = "assets/shooter map.tmj"

        layer_options = {
            "Terrain": {"use_spatial_hash": True},
            "Water": {"use_spatial_hash": True}
        }

        self.tilemap = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

        self.size_x = self.tilemap.width * self.tilemap.tile_width * TILE_SCALING
        self.size_y = self.tilemap.height * self.tilemap.tile_height * TILE_SCALING

        """Set up the player"""
        self.player = Player("assets/human2.png", SPRITE_SCALING)
        self.player.center_x = random.randint(20, round(self.size_x - 20))
        self.player.center_y = random.randint(20, round(self.size_y - 20))
        self.scene.add_sprite("Player", self.player)

        """Set up the enemy spawn timer"""
        self.spawn_time = 5 * 60
        self.spawn_time_timer = 0

        """Set up the enemy info"""
        self.enemy_damage = Dec("0.025")
        self.enemy_speed = 1.2
        self.enemy_spawn_health = Dec("20")
        self.spawn_time_add = 1
        self.enemy_health = self.enemy_spawn_health
        self.enemy_spawn_health_increase = 0.05
        self.enemy_damage_increase = 0.005
        self.enemy_speed_increase = 0.05
        self.spawn_time_add_add = 0.01

        """Key presses and mouse presses"""
        self.z = False
        self.s = False
        self.q = False
        self.d = False
        self.mouse_press = False

        """Mouse position"""
        self.mouse_position = [0, 0]

        """Player's physics engine and enemy's physics engine"""
        self.physics_engine = arcade.PhysicsEngineSimple(self.player,
                                                         walls=(self.scene["Terrain"], self.scene["Water"]))
        self.enemy_physics_engine = arcade.PhysicsEngineSimple(Enemy("assets/zombie1.png", SPRITE_SCALING),
                                                               self.scene["Terrain"])

        """Sprite lists"""
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        """Set up pause flag"""
        self.pause = False

    def on_draw(self):
        """Render the screen."""

        # This command has to happen before we start drawing
        self.clear()

        """Draw the map and sprites"""
        self.camera.use()
        self.scene.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        """Draw the GUI"""
        self.GUI.use()
        """draw health"""
        arcade.Text(f"{self.player.health} / {self.player.max_health}", self.width / 2 - 85, 10, (0, 255, 0),
                    30).draw()
        """draw money"""
        arcade.Text(f"{self.player.money}€", self.width / 2 - 85, 45, (255, 255, 0), 30).draw()

        """tell the player if the game is paused or not"""
        if self.pause:
            arcade.Text("PAUSED", self.width / 2 - 85, self.height - 30, (255, 255, 255), 30).draw()

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

        """key to quit the game"""
        if key == arcade.key.ESCAPE:
            arcade.close_window()

        """Pause the game"""
        if key == arcade.key.SPACE:
            self.pause = not self.pause

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

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_press = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_press = False

    def on_update(self, delta_time: float):
        """ Movement and game logic """
        """is the game paused ?"""
        if not self.pause:
            """move the player"""
            if self.z:
                self.player.center_y += self.player.move_speed
            if self.s:
                self.player.center_y -= self.player.move_speed
            if self.q:
                self.player.center_x -= self.player.move_speed
            if self.d:
                self.player.center_x += self.player.move_speed

            """reset if the player is dead"""
            if self.player.health <= 0:
                self.setup()
            """make sure the player never has more than 20 HP"""
            if self.player.health > 20:
                self.player.health = 20

            """"spawn a new enemy every so-often, update the spawn timer and increase the difficulty"""
            self.spawn_time_timer += self.spawn_time_add
            if self.spawn_time_timer >= self.spawn_time:
                new_enemy = Enemy(f"assets/zombie{random.randint(1, 4)}.png", SPRITE_SCALING)
                new_enemy.center_x = random.uniform(20, self.size_x - 20)
                new_enemy.center_y = random.uniform(20, self.size_y - 20)
                new_enemy.health = self.enemy_spawn_health
                new_enemy.speed = self.enemy_speed
                new_enemy.damage = self.enemy_damage
                new_enemy.money_drop = self.enemy_damage * 5 + Dec(self.enemy_speed) * 3 + self.enemy_spawn_health / 15

                self.enemy_spawn_health += Dec(self.enemy_spawn_health_increase + random.uniform(
                    -self.enemy_spawn_health_increase, self.enemy_spawn_health_increase))

                self.enemy_speed += self.enemy_speed_increase + random.uniform(-self.enemy_speed_increase,
                                                                               self.enemy_speed_increase)
                self.enemy_damage += Dec(self.enemy_damage_increase + random.uniform(-self.enemy_damage_increase,
                                                                                     self.enemy_damage_increase))
                self.spawn_time_add += self.spawn_time_add_add
                self.spawn_time_timer = 0

                self.enemy_list.append(new_enemy)

            """handle the enemy logic"""
            for enemy in self.enemy_list:
                self.enemy_physics_engine = arcade.PhysicsEngineSimple(enemy, self.scene["Terrain"])

                if enemy.health <= 0:
                    self.player.money += enemy.money_drop
                    enemy.remove_from_sprite_lists()

                diff_x = self.player.center_x - enemy.center_x
                diff_y = self.player.center_y - enemy.center_y

                target_angle = atan2(diff_y, diff_x)
                enemy.angle = degrees(target_angle)

                enemy.forward(enemy.speed)
                enemy.change_x /= enemy.friction + 1
                enemy.change_y /= enemy.friction + 1
                if arcade.check_for_collision(enemy, self.player):
                    self.player.health -= enemy.damage

                self.enemy_physics_engine.update()

                hit_sprite = arcade.check_for_collision_with_list(enemy, self.bullet_list)
                if len(hit_sprite) > 0:
                    enemy.health -= self.player.damage

            """update the shooting timer"""
            if self.player.shoot_timer <= 0:
                self.player.shoot_timer = 0
            else:
                self.player.shoot_timer -= 1

            """handle the gun logic"""
            if self.mouse_press and self.player.shoot_timer <= 0:
                for i in range(self.player.shoot_amount):
                    bullet = Bullet("assets/bullet.png", SPRITE_SCALING * 1.3)

                    bullet.center_x, bullet.center_y = self.player.center_x, self.player.center_y
                    bullet.angle = self.player.angle + random.uniform(self.player.shoot_spread / -2,
                                                                      self.player.shoot_spread / 2)
                    bullet.forward(bullet.speed)

                    self.bullet_list.append(bullet)
                self.player.shoot_timer = 60 * self.player.shoot

            """check if the bullet hit something"""
            for bullet in self.bullet_list:
                hit = arcade.check_for_collision_with_list(bullet, self.scene["Terrain"])
                if len(hit) > 0:
                    bullet.remove_from_sprite_lists()

                hit_sprite = arcade.check_for_collision_with_list(bullet, self.enemy_list)
                if len(hit_sprite) > 0:
                    bullet.remove_from_sprite_lists()

            self.physics_engine.update()
            self.bullet_list.update()

            """center the camera on the player"""
            self.scroll_to_player()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        """This code makes the player sprite always face the cursor"""
        if not self.pause:
            self.mouse_position[0] = x
            self.mouse_position[1] = y
            start_x = self.player.center_x
            start_y = self.player.center_y

            dest_x = self.mouse_position[0] + self.camera_position[0]
            dest_y = self.mouse_position[1] + self.camera_position[1]

            x_diff = dest_x - start_x
            y_diff = dest_y - start_y

            angle = atan2(y_diff, x_diff)

            self.player.angle = degrees(angle)

    def scroll_to_player(self):
        """set the camera's so that the player is in the middle of its POV"""
        self.camera_position = self.player.center_x - (self.width / 2), self.player.center_y - (self.height / 2)
        self.camera.move_to(self.camera_position)


def main():
    """ Main function """
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()
