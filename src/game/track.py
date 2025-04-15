from panda3d.core import NodePath
from src.utils.constants import *

class Track:
    def __init__(self, render, loader):
        self.render = render
        self.loader = loader
        self.track = None
        self.lanes = []
        self.create_track()
        
    def create_track(self):
        # Create the track base
        self.track = self.loader.loadModel("models/box")
        self.track.setScale(TRACK_WIDTH, TRACK_LENGTH, 0.1)
        self.track.setPos(0, 0, -0.1)
        self.track.setColor(*TRACK_COLOR)
        self.track.reparentTo(self.render)
        
        # Create lane markers
        for i in range(-1, 2):
            lane = self.loader.loadModel("models/box")
            lane.setScale(0.1, TRACK_LENGTH, 0.1)
            lane.setPos(i * LANE_WIDTH, 0, 0)
            lane.setColor(*LANE_MARKER_COLOR)
            lane.reparentTo(self.render)
            self.lanes.append(lane)
            
    def update(self, speed):
        # Move track forward at a controlled speed
        movement = -TRACK_SPEED * speed  # Negative to move toward player
        self.track.setY(self.track.getY() + movement)
        
        # Move lane markers
        for lane in self.lanes:
            lane.setY(lane.getY() + movement)
            
        # Reset track position when it goes too far
        if self.track.getY() < -TRACK_RESET_POSITION:  # Changed to negative
            self.track.setY(0)
            for lane in self.lanes:
                lane.setY(0) 