import arcade
#screen
screenW = 500
screenH = 500
screenTitle = "test"
#terrain
terrainxmax = 1000
terrainymax = 1000
#scaling
spriteScale = 1
spriteScale2 = 1
#player stat
playerspeed = 5
gravity = 0.7
jumppower = 14

class game(arcade.Window):
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(screenW, screenH, screenTitle)

        #map
        self.tile_map = None

        #scene
        self.scene = None
        #player
        self.player_sprite = None
        #physics engine
        self.physics_engine = None
        #camera
        self.camera = None

        arcade.set_background_color((0,0,127))

    def setup(self):

        #camera
        self.camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "resource/map.tmx"

        # Layer specific options are defined based on Layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layer
        # use spatial hashing for detection.
        layer_options = {
            "Terrain": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, spriteScale2, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Set up the player, specifically placing it at these coordinates.
        image_source = "resource/player.png"
        self.player_sprite = arcade.Sprite(image_source, spriteScale)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=gravity, walls=self.scene["Terrain"]
        )

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here

        # Activate our Camera
        self.camera.use()

        # Draw our sprites
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.Z:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = jumppower
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -playerspeed
        elif key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.change_x = -playerspeed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = playerspeed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.Z:
            self.player_sprite.change_y = self.player_sprite.change_y
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.Q:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Position the camera
        self.center_camera_to_player()

def main():
    window = game()
    window.setup()
    arcade.run()

main()