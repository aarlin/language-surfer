from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import random
from src.utils.constants import *
from src.utils.data_manager import DataManager

class CharacterManager:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.current_character = None
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
                
    def show_new_character(self):
        # Get a random character
        char_data = random.choice(CHARACTERS)
        self.current_character = char_data
        
        # Update display
        self.character_text.setText(char_data["char"])
        self.meaning_text.setText("")
        
        # Reset timers
        self.time_since_character = 0
        self.meaning_displayed = False
        self.time_since_meaning = 0
        
        # Add to data manager if new
        self.data_manager.add_character(
            char_data["char"],
            char_data["meaning"],
            char_data["lane"]
        )
        
    def show_meaning(self):
        if self.current_character:
            self.meaning_text.setText(self.current_character["meaning"])
            self.meaning_displayed = True
            
    def check_correct_lane(self, player_lane: int) -> bool:
        if self.current_character:
            is_correct = player_lane == self.current_character["lane"]
            self.data_manager.update_srs(self.current_character["char"], is_correct)
            return is_correct
        return False
        
    def reset(self):
        self.current_character = None
        self.character_text.setText("")
        self.meaning_text.setText("")
        self.meaning_displayed = False
        self.time_since_character = 0
        self.time_since_meaning = 0 