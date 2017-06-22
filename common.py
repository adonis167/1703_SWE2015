import pygame
import os

SERVER_ADDRESS ="wesame.co.kr"

ASSETS = os.path.join(os.path.dirname(__file__), 'assets')

MAX_PLAYERS = 4

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_BG_COLOR = (200, 200, 200)
SCREEN_CAPTION = "Online Game"

p1_img = os.path.join(ASSETS, '1.png')
p2_img = os.path.join(ASSETS, '2.png')
p3_img = os.path.join(ASSETS, '3.png')
p4_img = os.path.join(ASSETS, '4.png')

GAME_ICON = os.path.join(ASSETS, 'bullet.png')
BULLET_IMG = os.path.join(ASSETS, 'bullet.png')

ground_texture = os.path.join(ASSETS, 'ground.png')
BG_IMG = pygame.image.load(ground_texture)

FPS = 60

BULLET_FIRE_SOUND = os.path.join(ASSETS, 'gun_fire.ogg')
GAME_MUSIC = os.path.join(ASSETS, 'Hitman.ogg')
# GAME_MUSIC = os.path.join(ASSETS, 'bgm.wav')



PLAYER1_IMG = pygame.image.load(p1_img)
PLAYER2_IMG = pygame.image.load(p2_img)
PLAYER3_IMG = pygame.image.load(p3_img)
PLAYER4_IMG = pygame.image.load(p4_img)

DISTANCE_BT_PLAYERS = 10

PLAYER1_POSITION_X = SCREEN_WIDTH/2 - PLAYER1_IMG.get_width() - DISTANCE_BT_PLAYERS
PLAYER1_POSITION_Y = SCREEN_HEIGHT/2 - PLAYER1_IMG.get_height() - DISTANCE_BT_PLAYERS
PLAYER1_POSITION = (PLAYER1_POSITION_X, PLAYER1_POSITION_Y)

PLAYER2_POSITION_X = SCREEN_WIDTH/2 + DISTANCE_BT_PLAYERS
PLAYER2_POSITION_Y = SCREEN_HEIGHT/2 - PLAYER2_IMG.get_height() - DISTANCE_BT_PLAYERS
PLAYER2_POSITION = (PLAYER2_POSITION_X, PLAYER2_POSITION_Y)

PLAYER3_POSITION_X = SCREEN_WIDTH/2 - PLAYER3_IMG.get_width() - DISTANCE_BT_PLAYERS
PLAYER3_POSITION_Y = SCREEN_HEIGHT/2 + DISTANCE_BT_PLAYERS
PLAYER3_POSITION = (PLAYER3_POSITION_X, PLAYER3_POSITION_Y)

PLAYER4_POSITION_X = SCREEN_WIDTH/2 + DISTANCE_BT_PLAYERS
PLAYER4_POSITION_Y = SCREEN_HEIGHT/2 + DISTANCE_BT_PLAYERS
PLAYER4_POSITION = (PLAYER4_POSITION_X, PLAYER4_POSITION_Y)







