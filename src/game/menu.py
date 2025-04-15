from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode
from src.utils.constants import *

class Menu:
    def __init__(self, render, loader, on_mode_selected):
        self.render = render
        self.loader = loader
        self.on_mode_selected = on_mode_selected
        self.title = None
        self.buttons = []
        self.create_menu()
        
    def create_menu(self):
        # Create title
        self.title = OnscreenText(
            text=GAME_TITLE,
            pos=(0, 0.5),
            scale=0.2,
            fg=TEXT_COLOR,
            align=TextNode.ACenter
        )
        
        # Create mode selection buttons
        self.buttons.append(DirectButton(
            text="Characters",
            pos=(0, 0, 0.1),
            scale=0.1,
            command=self.select_characters,
            frameSize=(-4, 4, -0.5, 0.5),
            text_fg=TEXT_COLOR,
            frameColor=(0.2, 0.2, 0.2, 1)
        ))
        
        self.buttons.append(DirectButton(
            text="Numbers",
            pos=(0, 0, -0.1),
            scale=0.1,
            command=self.select_numbers,
            frameSize=(-4, 4, -0.5, 0.5),
            text_fg=TEXT_COLOR,
            frameColor=(0.2, 0.2, 0.2, 1)
        ))
        
    def select_characters(self):
        self.hide()
        self.on_mode_selected("characters")
        
    def select_numbers(self):
        self.hide()
        self.on_mode_selected("numbers")
        
    def hide(self):
        if self.title:
            self.title.destroy()
            self.title = None
            
        for button in self.buttons:
            button.destroy()
        self.buttons = []
        
    def show(self):
        self.create_menu() 