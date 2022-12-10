import timeit

from ursina import *
from ursina.prefabs.tilemap import Tilemap
from math import *
from random import *

# create a window
app = Ursina()

EditorCamera()
camera.orthographic = True
tilemap = Tilemap('map.png', tileset='tileset.png', tileset_size=(300,300), parent=scene)
camera.fov = tilemap.tilemap.height


class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model='quad'
        self.texture = "human2.png"
        self.speed = 3.2
        self.always_on_top = True
        self.shoot = 1 * 60
        self.shoot_timer = self.shoot
        self.shoot_number = 3
        self.spread = 1
        self.bullet_speed = 15
        self.damage = 0.5

        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):

        mouse_pos = LVector3f(mouse.x + camera.x, mouse.y + camera.y, 0)
        self.look_at_2d(mouse_pos)

        self.y += held_keys["w"] * time.dt * self.speed
        self.y -= held_keys["s"] * time.dt * self.speed
        self.x += held_keys["d"] * time.dt * self.speed
        self.x -= held_keys["a"] * time.dt * self.speed

        camera.x = self.x
        camera.y = self.y

        if mouse.left:
            if self.shoot_timer >= self.shoot:
                for i in range(self.shoot_number):
                    bullet = Bullet()
                self.shoot_timer = 0
            self.shoot_timer += 1


class Bullet(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'quad'
        self.texture = "bullet.png"
        self.x = player.x
        self.y = player.y
        self.rotation_z = player.rotation_z + uniform(-player.spread / 2, player.spread / 2)
        self.scale_y = 0.3
        self.scale_x = 0.1
        self.always_on_top = True
        self.lifespan = 3*60
        self.lifespan_timer = 0

    def update(self):
        self.position += LVector3f(sin(radians(self.rotation_z)),cos(radians(self.rotation_z)),0) * time.dt * player.bullet_speed
        if self.lifespan_timer >= self.lifespan:
            destroy(self)
        self.lifespan_timer += 1

player = Player()



# start running the game
app.run()