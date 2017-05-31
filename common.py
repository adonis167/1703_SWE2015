import pygame

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SCREEN_BG_COLOR = (200, 200, 200)
SCREEN_CAPTION = "Online Game"

PLAYER1_IMG = pygame.image.load("1.png")
PLAYER2_IMG = pygame.image.load("2.png")
PLAYER3_IMG = pygame.image.load("3.png")
PLAYER4_IMG = pygame.image.load("4.png")

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






