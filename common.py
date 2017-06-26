import pygame
import os

SERVER_ADDRESS ="localhost"

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')
ASSETS_UNIT = os.path.join(os.path.dirname(__file__), 'assets/Unit')
ASSETS_BGIMG = os.path.join(os.path.dirname(__file__), 'assets/Background_img')
ASSETS_SOUND = os.path.join(os.path.dirname(__file__), 'assets/Sound')
ASSETS_MISSILE = os.path.join(os.path.dirname(__file__), 'assets/Missile')
ASSETS_ITEM = os.path.join(os.path.dirname(__file__), 'assets/Items')

MAX_PLAYERS = 2

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_BG_COLOR = (200, 200, 200)
SCREEN_CAPTION = "Online Game"

p1_img = os.path.join(ASSETS_UNIT, 'China_medium.png')
p2_img = os.path.join(ASSETS_UNIT, 'Japan_medium.png')
p3_img = os.path.join(ASSETS_UNIT, 'Korea_medium.png')
p4_img = os.path.join(ASSETS_UNIT, 'USA_medium.png')

p1_img_trap = os.path.join(ASSETS_UNIT, 'China_medium_trap.png')
p2_img_trap = os.path.join(ASSETS_UNIT, 'Japan_medium_trap.png')
p3_img_trap = os.path.join(ASSETS_UNIT, 'Korea_medium_trap.png')
p4_img_trap = os.path.join(ASSETS_UNIT, 'USA_medium_trap.png')

p1_img_shield = os.path.join(ASSETS_UNIT, 'China_medium_shield.png')
p2_img_shield = os.path.join(ASSETS_UNIT, 'Japan_medium_shield.png')
p3_img_shield = os.path.join(ASSETS_UNIT, 'Korea_medium_shield.png')
p4_img_shield = os.path.join(ASSETS_UNIT, 'USA_medium_shield.png')

p1_large = os.path.join(ASSETS_UNIT, 'China_large.png')
p2_large = os.path.join(ASSETS_UNIT, 'Japan_large.png')
p3_large = os.path.join(ASSETS_UNIT, 'Korea_large.png')
p4_large = os.path.join(ASSETS_UNIT, 'USA_large.png')

p1_large_trap = os.path.join(ASSETS_UNIT, 'China_large_trap.png')
p2_large_trap = os.path.join(ASSETS_UNIT, 'Japan_large_trap.png')
p3_large_trap = os.path.join(ASSETS_UNIT, 'Korea_large_trap.png')
p4_large_trap = os.path.join(ASSETS_UNIT, 'USA_large_trap.png')

p1_large_shield = os.path.join(ASSETS_UNIT, 'China_large_shield.png')
p2_large_shield = os.path.join(ASSETS_UNIT, 'Japan_large_shield.png')
p3_large_shield = os.path.join(ASSETS_UNIT, 'Korea_large_shield.png')
p4_large_shield = os.path.join(ASSETS_UNIT, 'USA_large_shield.png')

p1_small = os.path.join(ASSETS_UNIT, 'China_small.png')
p2_small = os.path.join(ASSETS_UNIT, 'Japan_small.png')
p3_small = os.path.join(ASSETS_UNIT, 'Korea_small.png')
p4_small = os.path.join(ASSETS_UNIT, 'USA_small.png')

p1_small_trap = os.path.join(ASSETS_UNIT, 'China_small_trap.png')
p2_small_trap = os.path.join(ASSETS_UNIT, 'Japan_small_trap.png')
p3_small_trap = os.path.join(ASSETS_UNIT, 'Korea_small_trap.png')
p4_small_trap = os.path.join(ASSETS_UNIT, 'USA_small_trap.png')

p1_small_shield = os.path.join(ASSETS_UNIT, 'China_small_shield.png')
p2_small_shield = os.path.join(ASSETS_UNIT, 'Japan_small_shield.png')
p3_small_shield = os.path.join(ASSETS_UNIT, 'Korea_small_shield.png')
p4_small_shield = os.path.join(ASSETS_UNIT, 'USA_small_shield.png')

GAME_ICON = os.path.join(ASSETS_MISSILE, 'guided_missile.png')
BULLET_IMG = os.path.join(ASSETS_MISSILE, 'basic_missile.png')
GUIDED_IMG = os.path.join(ASSETS_MISSILE, 'guided_missile.png')

SIZEDOWN = os.path.join(ASSETS_ITEM, 'sizedown.png')
SIZEUP = os.path.join(ASSETS_ITEM, 'sizeup.png')
SHIELD = os.path.join(ASSETS_ITEM, 'shield.png')
TRAP = os.path.join(ASSETS_ITEM, 'trap.png')
TURRET = os.path.join(ASSETS_ITEM, 'turret.png')
RANDOM_BOX = os.path.join(ASSETS_ITEM, 'random_box.png')


ground_texture = os.path.join(ASSETS_BGIMG, 'map.png')
BG_IMG = pygame.image.load(ground_texture)

FPS = 60

BULLET_FIRE_SOUND = os.path.join(ASSETS_SOUND, 'gun_fire.ogg')
# GAME_MUSIC = os.path.join(ASSETS_SOUND, 'Hitman.ogg')
GAME_MUSIC = os.path.join(ASSETS_SOUND, 'bgm.wav')

PLAYER1_IMG = pygame.image.load(p1_img)
PLAYER2_IMG = pygame.image.load(p2_img)
PLAYER3_IMG = pygame.image.load(p3_img)
PLAYER4_IMG = pygame.image.load(p4_img)

DISTANCE_BT_PLAYERS = 10

PLAYER1_WIDTH = PLAYER1_IMG.get_width()
PLAYER1_HEIGHT = PLAYER1_IMG.get_height()
PLAYER1_POSITION_X = SCREEN_WIDTH/2 - PLAYER1_IMG.get_width() - DISTANCE_BT_PLAYERS
PLAYER1_POSITION_Y = SCREEN_HEIGHT/2 - PLAYER1_IMG.get_height() - DISTANCE_BT_PLAYERS
PLAYER1_POSITION = (PLAYER1_POSITION_X, PLAYER1_POSITION_Y)

PLAYER2_WIDTH = PLAYER2_IMG.get_width()
PLAYER2_HEIGHT = PLAYER2_IMG.get_height()
PLAYER2_POSITION_X = SCREEN_WIDTH/2 + DISTANCE_BT_PLAYERS
PLAYER2_POSITION_Y = SCREEN_HEIGHT/2 - PLAYER2_IMG.get_height() - DISTANCE_BT_PLAYERS
PLAYER2_POSITION = (PLAYER2_POSITION_X, PLAYER2_POSITION_Y)

PLAYER3_WIDTH = PLAYER3_IMG.get_width()
PLAYER3_HEIGHT = PLAYER3_IMG.get_height()
PLAYER3_POSITION_X = SCREEN_WIDTH/2 - PLAYER3_IMG.get_width() - DISTANCE_BT_PLAYERS
PLAYER3_POSITION_Y = SCREEN_HEIGHT/2 + DISTANCE_BT_PLAYERS
PLAYER3_POSITION = (PLAYER3_POSITION_X, PLAYER3_POSITION_Y)

PLAYER4_WIDTH = PLAYER4_IMG.get_width()
PLAYER4_HEIGHT = PLAYER4_IMG.get_height()
PLAYER4_POSITION_X = SCREEN_WIDTH/2 + DISTANCE_BT_PLAYERS
PLAYER4_POSITION_Y = SCREEN_HEIGHT/2 + DISTANCE_BT_PLAYERS
PLAYER4_POSITION = (PLAYER4_POSITION_X, PLAYER4_POSITION_Y)


# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_ALLOY_ORANGE = (196, 121, 67)
RED = (255, 0, 0)
YELLOW = (255, 255, 12)

# depreciation of velocity
VELOCITY_DEPRECIATION = 0.6