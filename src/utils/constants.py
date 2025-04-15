# Game settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GAME_TITLE = "Language Surfer"

# Camera settings
CAMERA_DISTANCE = 15  # How far back the camera is
CAMERA_HEIGHT = 15   # How high the camera is
CAMERA_ANGLE = 10    # Angle in degrees (for reference)

# Track settings
TRACK_WIDTH = 20
TRACK_LENGTH = 100
LANE_COUNT = 3
LANE_WIDTH = 2
TRACK_SPEED = 0.05  # Reduced from 0.1
TRACK_RESET_POSITION = 30  # Reduced from 50

# Player settings
PLAYER_SCALE = 0.5
PLAYER_HEIGHT = 1.0
PLAYER_START_Y = -10
PLAYER_START_Z = 0.5
PLAYER_MOVE_SPEED = 0.5  # Increased from 0.2 for more noticeable movement

# Game settings
INITIAL_SPEED = 0.5  # Reduced from 1.0
SPEED_INCREASE = 0.02  # Reduced from 0.1
MAX_HEARTS = 3
CHARACTER_DISPLAY_TIME = 3.0  # seconds
MEANING_DISPLAY_DELAY = 2.0  # seconds

# Character data (Japanese Kanji with meanings)
CHARACTERS = [
    {"char": "人", "meaning": "person", "lane": 0},
    {"char": "山", "meaning": "mountain", "lane": 1},
    {"char": "水", "meaning": "water", "lane": 2},
    {"char": "火", "meaning": "fire", "lane": 0},
    {"char": "木", "meaning": "tree", "lane": 1},
    {"char": "日", "meaning": "sun", "lane": 2},
    {"char": "月", "meaning": "moon", "lane": 0},
    {"char": "口", "meaning": "mouth", "lane": 1},
    {"char": "手", "meaning": "hand", "lane": 2},
    {"char": "目", "meaning": "eye", "lane": 0},
]

# Colors
TRACK_COLOR = (0.2, 0.2, 0.2, 1)
LANE_MARKER_COLOR = (1, 1, 1, 1)
PLAYER_COLOR = (0, 0.5, 1, 1)
HEART_COLOR = (1, 0, 0, 1)
TEXT_COLOR = (1, 1, 1, 1)
CORRECT_COLOR = (0, 1, 0, 1)
INCORRECT_COLOR = (1, 0, 0, 1)
HEART_SYMBOL = "<3"  # ASCII heart symbol

# Word list for typing
WORD_LIST = [
    "the", "be", "to", "of", "and", "run", "jump", "duck",
    "slide", "quick", "fast", "slow", "move", "dash", "sprint",
    "dodge", "left", "right", "up", "down", "forward", "back",
    "speed", "power", "boost", "super", "mega", "ultra", "hyper",
    "swift", "agile", "nimble", "quick", "rapid", "steady", "flow"
] 