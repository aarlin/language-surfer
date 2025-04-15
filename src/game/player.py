from panda3d.core import NodePath
from src.utils.constants import *

class Player:
    def __init__(self, render, loader):
        self.render = render
        self.loader = loader
        self.model = None
        self.position = 0  # -1: left, 0: center, 1: right
        self.create_player()
        
    def create_player(self):
        # Try to load the chair model
        try:
            # Load the glTF model
            self.model = self.loader.loadModel("models/gltf/vergils-chair.glb")
            print("Loaded chair model")
            
            # Scale and position the chair
            self.model.setScale(0.5)  # Adjust scale as needed
            self.model.setH(180)  # Rotate to face forward
            
        except Exception as e:
            print(f"Error loading chair model: {e}")
            print("Falling back to default box model")
            self.model = self.loader.loadModel("models/box")
            self.model.setScale(PLAYER_SCALE, PLAYER_SCALE, PLAYER_HEIGHT)
            self.model.setColor(*PLAYER_COLOR)
            
        self.model.setPos(0, PLAYER_START_Y, PLAYER_START_Z)
        self.model.reparentTo(self.render)
        
    def move_left(self):
        if self.position > -1:
            self.position -= 1
            self.update_position()
            
    def move_right(self):
        if self.position < 1:
            self.position += 1
            self.update_position()
            
    def update_position(self):
        # Smoothly move player to new lane with controlled speed
        target_x = self.position * LANE_WIDTH
        current_x = self.model.getX()
        new_x = current_x + (target_x - current_x) * PLAYER_MOVE_SPEED
        self.model.setX(new_x) 