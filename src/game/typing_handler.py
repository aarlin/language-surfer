from pynput import keyboard
from typing import Callable, Optional

class TypingHandler:
    def __init__(self, on_typing: Callable[[str], None], on_backspace: Callable[[], None]):
        self.on_typing = on_typing
        self.on_backspace = on_backspace
        self.listener: Optional[keyboard.Listener] = None
        
    def start(self):
        """Start the keyboard listener"""
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        
    def stop(self):
        """Stop the keyboard listener"""
        if self.listener:
            self.listener.stop()
            
    def _on_press(self, key):
        try:
            # Handle character keys
            if hasattr(key, 'char'):
                char = key.char.lower()  # Convert to lowercase
                if char == 'a':
                    self.on_typing('left')
                elif char == 'd':
                    self.on_typing('right')
                else:
                    self.on_typing(char)
        except Exception as e:
            print(f"Error handling key press: {e}")
            
    def _on_release(self, key):
        # Handle backspace
        if key == keyboard.Key.backspace:
            self.on_backspace()
            
        # Handle arrow keys
        elif key == keyboard.Key.left:
            self.on_typing('left')
        elif key == keyboard.Key.right:
            self.on_typing('right')
            
        # Stop listener on escape
        elif key == keyboard.Key.esc:
            return False 