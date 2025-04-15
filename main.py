from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties, TextNode, loadPrcFileData, Point3
import sys
import random
from datetime import datetime
import math

from src.game.track import Track
from src.game.player import Player
from src.game.typing_handler import TypingHandler
from src.game.character_manager import CharacterManager
from src.utils.constants import *
from src.utils.data_manager import DataManager

# Configure window properties before creating the ShowBase instance
loadPrcFileData("", """
    window-title Language Surfer
    win-size 1200 800
    cursor-hidden 0
    show-frame-rate-meter 1
""")

# Common English words for typing practice
WORD_LIST = [
    "the", "be", "to", "of", "and", "run", "jump", "duck",
    "slide", "quick", "fast", "slow", "move", "dash", "sprint",
    "dodge", "left", "right", "up", "down", "forward", "back",
    "speed", "power", "boost", "super", "mega", "ultra", "hyper",
    "swift", "agile", "nimble", "quick", "rapid", "steady", "flow"
]

class LanguageSurfer(ShowBase):
    def __init__(self):
        print("Initializing Language Surfer...")
        ShowBase.__init__(self)
        
        # Set up window properties
        props = WindowProperties()
        props.setTitle(GAME_TITLE)
        props.setSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        props.setCursorHidden(False)
        self.win.requestProperties(props)
        
        # Disable camera control
        self.disableMouse()
        
        # Set up camera with proper angle calculation
        angle_rad = math.radians(CAMERA_ANGLE)
        distance = CAMERA_DISTANCE
        height = distance * math.sin(angle_rad)
        y_pos = -distance * math.cos(angle_rad)
        
        self.camera.setPos(0, y_pos, height)
        self.camera.lookAt(Point3(0, 0, 0))
        
        print("Window properties set")
        
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Game state
        self.score = 0
        self.level = 1
        self.hearts = MAX_HEARTS
        self.game_speed = INITIAL_SPEED
        self.game_over = False
        self.characters_seen = 0
        
        # Create game objects
        self.track = Track(self.render, self.loader)
        self.player = Player(self.render, self.loader)
        self.character_manager = CharacterManager(self.data_manager)
        
        # Create UI elements
        self.score_text = OnscreenText(
            text="Score: 0",
            pos=(-1.3, 0.9),
            scale=0.07,
            fg=TEXT_COLOR,
            align=TextNode.ALeft
        )
        
        self.level_text = OnscreenText(
            text="Level: 1",
            pos=(-1.3, 0.8),
            scale=0.07,
            fg=TEXT_COLOR,
            align=TextNode.ALeft
        )
        
        self.hearts_text = OnscreenText(
            text=HEART_SYMBOL * self.hearts,
            pos=(-1.3, 0.7),
            scale=0.07,
            fg=HEART_COLOR,
            align=TextNode.ALeft
        )
        
        self.game_over_text = OnscreenText(
            text="",
            pos=(0, 0),
            scale=0.2,
            fg=TEXT_COLOR
        )
        
        print("UI elements created")
        
        # Set up typing handler
        self.typing_handler = TypingHandler(
            on_typing=self.handle_typing,
            on_backspace=self.handle_backspace
        )
        self.typing_handler.start()
        
        # Start the game
        self.start_new_round()
        
        # Set up tasks
        self.taskMgr.add(self.update_game, "update_game")
        
        print("Game initialization complete")
        
    def start_new_round(self):
        if not self.game_over:
            self.character_manager.show_new_character()
            self.characters_seen += 1
            
    def handle_typing(self, char):
        if self.game_over:
            return
            
        if char == 'left':
            self.player.move_left()
            self.check_lane()
        elif char == 'right':
            self.player.move_right()
            self.check_lane()
            
    def check_lane(self):
        if self.character_manager.current_character:
            is_correct = self.character_manager.check_correct_lane(self.player.position)
            if is_correct:
                self.score += 10 * self.level
                self.score_text.setText(f"Score: {self.score}")
                
                # Update level based on score
                new_level = 1 + (self.score // 100)
                if new_level != self.level:
                    self.level = new_level
                    self.level_text.setText(f"Level: {self.level}")
                    self.game_speed += SPEED_INCREASE
            else:
                self.hearts -= 1
                self.hearts_text.setText(HEART_SYMBOL * self.hearts)
                
                if self.hearts <= 0:
                    self.game_over = True
                    self.show_game_over()
                    
            self.start_new_round()
            
    def show_game_over(self):
        self.game_over_text.setText("Game Over!\nPress R to restart")
        self.data_manager.add_score(self.score, self.level, self.characters_seen)
        
    def handle_backspace(self):
        pass  # Not used in this version
        
    def update_game(self, task):
        if self.game_over:
            return Task.cont
            
        # Update track and player
        self.track.update(self.game_speed)
        self.player.update_position()  # Update player position every frame
        
        # Update character manager
        self.character_manager.update(task.time)
        
        return Task.cont

if __name__ == "__main__":
    print("Starting Language Surfer...")
    try:
        game = LanguageSurfer()
        game.run()
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc() 