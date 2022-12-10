import arcade
import math
import random



SPRITE_SCALING = 0.3
TILE_SCALING = 1
IMAGE_SIZE = 30
GLOBAL_SCALE = 2
SPRITE_SCALING *= GLOBAL_SCALE
TILE_SCALING *= GLOBAL_SCALE
SPRITE_SIZE = 45

SCREEN_HEIGHT = 720
SCREEN_WIDTH = round(SCREEN_HEIGHT * (16/9))
SCREEN_TITLE = "shooter"

#stats
HP_MAX = 20
HP_REGEN = 0.01
HP_REGEN_KILL = 1
SPEED_F = 3
FRICTION = 0.15
MAX_SPEED = 999
MIN_SPEED = 1E-2
BULLET_SPEED = 9
BULLET_SHOOT_SPEED = 0.02
BULLET_NUMBER = 1
BULLET_SPREAD = 10
BULLET_DMG = 0.7
ENEMY_SPEED = 0.15
ENEMY_HP = 20
ENEMY_DMG = 0.05
ENEMY_SPAWN_TIME = 5
ENEMY_SPAWN_TIME_DIFFICULTY = 0.01
ENEMY_DMG_DIFFICULTY = 0.03
ENEMY_HP_DIFFICULTY = 0.02
ENEMY_SPEED_DIFFICULTY = 0.03
ENEMY_WAVE = 0

# color
WHITE = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

class Enemy(arcade.Sprite):
    def __init__(self,img,scale,hp,speed,dmg):
        super().__init__(img, scale)
        self.hp = hp
        self.speed = speed
        self.dmg = dmg


class Shooter(arcade.Window):
    """
        Main application class.
        """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height, title, fullscreen=True, vsync=True, resizable=True, update_rate=1 / 60)

        width = 10
        height = 10
        self.set_viewport(0, width, 0, height)

        # Our Scene Object and map info
        self.sizex = None
        self.scene = None
        self.sizey = None
        self.physics_engine = None
        self.tile_map = None

        # GUI
        self.GUI = None

        # camera
        self.camera = None
        self.camerapos = None

        #player
        self.player = None
        self.speed = None
        self.player_hp = None
        self.hp_max = None

        #key press
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.mouse_pressed = None

        #bullet
        self.bullet_list = None
        self.bullet = None
        self.shoot = None

        #mouse pos
        self.x = None
        self.y = None



        #physics engine
        self.physics_engine = None
        self.enemy_engine = None

        #enemy
        self.enemy = None
        self.enemy_list = None
        self.enemy_hp = None
        self.spawn_time = None


    def setup(self):
        """ Set up the game and initialize the variables. """
        # setup GUI
        self.GUI = arcade.Camera(self.width, self.height)

        # setup camera
        self.camera = arcade.Camera(self.width, self.height)

        #map
        map_name = "assets/shooter map.tmj"

        layer_options = {"Terrain": {"use_spatial_hash": True},
                         "Water": {"use_spatial_hash": True}}

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        self.sizex = self.tile_map.width * self.tile_map.tile_width * TILE_SCALING
        self.sizey = self.tile_map.height * self.tile_map.tile_height * TILE_SCALING

        #player
        self.player = arcade.Sprite("assets/human2.png", SPRITE_SCALING)
        self.player.angle = 0
        self.player.center_x = random.randint(20, self.sizex - 20)
        self.player.center_y = random.randint(20, self.sizey - 20)
        self.speed = 0
        self.hp_max = HP_MAX
        self.player_hp = self.hp_max
        self.kill = False
        self.scene.add_sprite("Player", self.player)

        #bullet
        self.bullet = arcade.Sprite("assets/bullet.png")
        self.bullet.center_y = 59839
        self.bullet.center_x = 8378734
        self.bullet.angle = 0
        self.shoot = 0
        self.hit_sprite = []
        self.bullet_list = arcade.SpriteList()
        self.bullet_list.append(self.bullet)

        #key press
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.mouse_pressed = False

        #mousepos
        self.x = 0
        self.y = 0

        #physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, walls=(self.scene["Terrain"], self.scene["Water"]))

        #enemy
        self.enemy = Enemy("assets/zombie"+f"{random.randint(1,4)}"+".png", SPRITE_SCALING,ENEMY_HP, ENEMY_SPEED, ENEMY_DMG)
        self.enemy.center_x = random.randint(20,self.sizex - 20)
        self.enemy.center_y = random.randint(20,self.sizey - 20)
        self.enemy.angle = 0
        self.spawn_time = 0
        self.time = ENEMY_SPAWN_TIME * 60
        self.enemy.hp = ENEMY_HP
        self.enemy.speed = ENEMY_SPEED
        self.enemy.dmg = ENEMY_DMG
        self.enemy_list = arcade.SpriteList()
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        #draw map and sprites
        self.camera.use()
        self.scene.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()

        self.GUI.use()
        HP = f"{round(self.player_hp)} / {self.hp_max} HP"
        HP = arcade.Text(HP, self.width / 2 - 85, 10, GREEN, 30)
        HP.draw()





    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.x = x
        self.y = y
        start_x = self.player.center_x
        start_y = self.player.center_y

        dest_x = x + self.camerapos[0]
        dest_y = y + self.camerapos[1]

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        angle = math.atan2(y_diff, x_diff)

        self.player.angle = math.degrees(angle)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_pressed = True

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_pressed = False




    def on_update(self, delta_time):
        """ Movement and game logic """
        self.physics_engine.update()
        self.scroll_to_player()
        self.bullet_list.update()
        self.enemy_list.update()

        self.player_hp += HP_REGEN / 60

        if self.player_hp <= 0:
            self.setup()
        if self.kill:
            self.kill = False
            self.player_hp += HP_REGEN_KILL

        if  self.player_hp > 20:
            self.player_hp = 20

        self.spawn_time += 1
        if self.spawn_time >= self.time:
            new_enemy = Enemy("assets/zombie"+f"{random.randint(1,4)}"+".png", SPRITE_SCALING,self.enemy.hp, self.enemy.speed, self.enemy.dmg)
            new_enemy.center_x = random.randint(20,self.sizex - 20)
            new_enemy.center_y = random.randint(20,self.sizey - 20)
            self.time /= ENEMY_SPAWN_TIME_DIFFICULTY + 1
            self.enemy.hp *= ENEMY_HP_DIFFICULTY + 1
            self.enemy.speed *= ENEMY_SPEED_DIFFICULTY + 1
            self.enemy.dmg *= ENEMY_DMG_DIFFICULTY + 1
            self.spawn_time = 0
            self.enemy_list.append(new_enemy)

        for enemy in self.enemy_list:
            if len(self.enemy_list) > 10:
                enemy.remove_from_sprite_lists
            self.enemy_engine = arcade.PhysicsEngineSimple(enemy, self.scene["Terrain"])

            start_x = enemy.center_x
            start_y = enemy.center_y
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            diff_x = dest_x - start_x
            diff_y = dest_y - start_y

            angle = math.atan2(diff_y, diff_x)
            enemy.angle = math.degrees(angle)

            enemy.forward(enemy.speed)
            enemy.change_x /= FRICTION + 1
            enemy.change_y /= FRICTION + 1

            hit = arcade.check_for_collision_with_list(enemy, self.bullet_list)
            player = arcade.check_for_collision(enemy, self.player)
            if len(hit) > 0:
                enemy.hp -= BULLET_DMG
            if enemy.hp <= 0:
                self.kill = True
                enemy.remove_from_sprite_lists()
            if player:
                self.player_hp -= enemy.dmg
                enemy.hp += enemy.dmg

            if enemy.center_x < 0 or enemy.center_x > self.sizex or enemy.center_y < 0 or enemy.center_y > self.sizey:
                enemy.remove_from_sprite_lists()

            self.enemy_engine.update()


        for bullet in self.bullet_list:
            hit = arcade.check_for_collision_with_list(bullet, self.scene["Terrain"])
            if len(hit) > 0:
                bullet.remove_from_sprite_lists()
            self.hit_sprite = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if len(self.hit_sprite) > 0:
                bullet.remove_from_sprite_lists()

        if self.shoot <= 0:
            self.shoot = 0
        else:
            self.shoot -= 1

        if self.up and not self.down:
                self.player.change_y = (SPEED_F)
        elif self.down and not self.up:
                self.player.change_y = (-SPEED_F)

        if self.left and not self.right:
            self.player.change_x = (-SPEED_F)
        elif self.right and not self.left:
            self.player.change_x = (SPEED_F)

        self.player.change_x /= FRICTION + 1
        self.player.change_y /= FRICTION + 1

        if MIN_SPEED > self.speed > 0:
            self.player.change_x = 0
            self.player.change_y = 0

        if self.mouse_pressed and self.shoot <= 0:
            for i in range(BULLET_NUMBER):
                bullet = arcade.Sprite("assets/bullet.png", SPRITE_SCALING * 3)
                start_x = self.player.center_x
                start_y = self.player.center_y
                bullet.center_x = start_x
                bullet.center_y = start_y

                dest_x =  self.x + self.camerapos[0]
                dest_y = self.y + self.camerapos[1]

                diff_x = dest_x - start_x
                diff_y = dest_y - start_y

                angle = math.atan2(diff_y, diff_x)

                bullet.angle = math.degrees(angle) + random.uniform(BULLET_SPREAD / -2, BULLET_SPREAD / 2)
                bullet.forward(BULLET_SPEED)

                self.bullet_list.append(bullet)
            self.shoot = 60 * BULLET_SHOOT_SPEED


    def scroll_to_player(self):
        self.camerapos = self.player.center_x - (self.width / 2), self.player.center_y - (self.height / 2)
        self.camera.move_to(self.camerapos)

    def on_key_press(self, key, modifiers):
        """Key presses"""
        #move key
        if key == arcade.key.Z:
            self.up = True
        elif key == arcade.key.S:
            self.down = True
        elif key == arcade.key.D:
            self.right = True
        elif key == arcade.key.Q:
            self.left = True

        # quit game
        if key == arcade.key.ESCAPE:
            arcade.close_window()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.Z:
            self.up = False
        elif key == arcade.key.S:
            self.down = False
        elif key == arcade.key.D:
            self.right = False
        elif key == arcade.key.Q:
            self.left = False


def main():
    """ Main function """
    window = Shooter(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


main()