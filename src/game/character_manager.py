from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode, NodePath
import random
from src.utils.constants import *
from src.utils.data_manager import DataManager

class CharacterManager:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.current_character = None
        self.character_text = None
        self.meaning_text = None
        self.render = None
        self.loader = None
        self.meaning_displayed = False
        self.time_since_character = 0
        self.time_since_meaning = 0
        
        # Create text displays
        self.character_text = OnscreenText(
            text="",
            pos=(0, 0.6),
            scale=0.2,
            fg=TEXT_COLOR
        )
        
        self.meaning_text = OnscreenText(
            text="",
            pos=(0, 0.4),
            scale=0.15,
            fg=TEXT_COLOR
        )
        
    def update(self, dt):
        if self.current_character:
            self.time_since_character += dt
            
            # Show meaning after delay
            if not self.meaning_displayed and self.time_since_character >= MEANING_DISPLAY_DELAY:
                self.show_meaning()
                
            # Reset after display time
            if self.time_since_character >= CHARACTER_DISPLAY_TIME:
                self.reset()
                
    def show_new_character(self, mode):
        if not self.render or not self.loader:
            return
            
        # Clear previous character
        self.clear_character()
        
        # Select character based on mode
        if mode == "characters":
            character_data = random.choice(CHARACTERS)
        else:  # numbers mode
            character_data = random.choice(NUMBERS)
            
        self.current_character = character_data
        
        # Create character text
        self.character_text = OnscreenText(
            text=character_data["char"],
            pos=(0, 0.2),
            scale=0.2,
            fg=TEXT_COLOR,
            align=TextNode.ACenter
        )
        
        # Create meaning text
        self.meaning_text = OnscreenText(
            text=character_data["meaning"],
            pos=(0, -0.2),
            scale=0.1,
            fg=TEXT_COLOR,
            align=TextNode.ACenter
        )
        
        # Reset timers
        self.time_since_character = 0
        self.meaning_displayed = False
        self.time_since_meaning = 0
        
        # Add to data manager if new
        self.data_manager.add_character(
            character_data["char"],
            character_data["meaning"],
            character_data["lane"]
        )
        
    def clear_character(self):
        if self.character_text:
            self.character_text.destroy()
            self.character_text = None
            
        if self.meaning_text:
            self.meaning_text.destroy()
            self.meaning_text = None
            
        self.current_character = None
        
    def show_meaning(self):
        if self.current_character:
            self.meaning_text.setText(self.current_character["meaning"])
            self.meaning_displayed = True
            
    def check_correct_lane(self, player_position):
        if not self.current_character:
            return False
        is_correct = player_position == self.current_character["lane"]
        self.data_manager.update_srs(self.current_character["char"], is_correct)
        return is_correct
        
    def reset(self):
        self.clear_character()
        self.meaning_displayed = False
        self.time_since_character = 0
        self.time_since_meaning = 0 