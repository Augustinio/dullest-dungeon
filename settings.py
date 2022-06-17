# The board is a square, PLAY_DIM defines the length of that square
PLAY_DIM = 800
# The menu is the same height as the gameboard, its width can be customized
MENU_WIDTH = 400

SCREEN_HEIGHT = PLAY_DIM
SCREEN_WIDTH = PLAY_DIM + MENU_WIDTH

# Number of tiles on the board
NUM_TILES = 10
TILE_S = PLAY_DIM / NUM_TILES

# Number of NPCs on the board
NPC_NUMS = 2
# Max number of NPCs displayed in the menu
MAX_DISPLAYED_NPCS = 5
# Max health players start with
MAX_HEALTH = 100

# colors of the tiles
TILE_COLOR_ONE = (74, 38, 13)
TILE_COLOR_TWO = (130, 106, 90)

# colors of the NPCs and player character
NPC_COLOR = (0, 0, 0)
CHAR_COLOR = (200, 200, 200)

WEAPONS = [
    ('Double Edged Sword', 5, 1),
    ('Mallet', 4, 0),
    ('Warhammer', 8, 3),
]
