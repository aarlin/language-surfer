# Language Surfer

A typing-based subway surfer game where you type words to navigate and avoid obstacles.

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) To generate your own requirements.txt:
```bash
pip freeze > requirements.txt
```

## Running the Game

1. Make sure your virtual environment is activated
2. Run the game:
```bash
python main.py
```

## Game Controls
- Type the words that appear on screen to move and avoid obstacles
- The faster you type, the more points you earn
- Avoid obstacles by typing the correct words in time

## Features
- Dynamic word generation
- Increasing difficulty
- Score tracking
- Smooth 3D graphics using Panda3D 