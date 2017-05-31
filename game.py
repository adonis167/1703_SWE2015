import pygame

from PodSixNet.Connection import ConnectionListener, connection

from time import sleep

from pygame.locals import *

import common
import math


# Initialize the game
pygame.init()
size = width, height = common.SCREEN_WIDTH, common.SCREEN_HEIGHT
screen = pygame.display.set_mode(size)

pygame.display.set_caption(common.SCREEN_CAPTION)
pygame.display.set_icon(pygame.image.load(common.GAME_ICON))

pygame.mixer.music.load(common.GAME_MUSIC)

fps_clock = pygame.time.Clock()

# Fill the screen with our background colour
# screen.fill(common.SCREEN_BG_COLOR)th our background colour




# Create a new class to hold our game object
# This extends the connection listener so that we can pump the server for messages
class OnlineGame(ConnectionListener):
    # Constructor
    def __init__(self):

        # Create the players
        self.players = []
        self.players.append(Player(common.PLAYER1_IMG))
        self.players.append(Player(common.PLAYER2_IMG))
        self.players.append(Player(common.PLAYER3_IMG))
        self.players.append(Player(common.PLAYER4_IMG))

        self.players[0].rect.x = common.PLAYER1_POSITION_X
        self.players[0].rect.y = common.PLAYER1_POSITION_Y

        self.players[1].rect.x = common.PLAYER2_POSITION_X
        self.players[1].rect.y = common.PLAYER2_POSITION_Y

        self.players[2].rect.x = common.PLAYER3_POSITION_X
        self.players[2].rect.y = common.PLAYER3_POSITION_Y

        self.players[3].rect.x = common.PLAYER4_POSITION_X
        self.players[3].rect.y = common.PLAYER4_POSITION_Y

        # Initialize the gameID and player ID
        self.gameID = None
        self.player = None

        # Connect to the server
        self.Connect()

        # Set running to false
        self.running = False

        # While the game isn't running pump the server
        while not self.running:
            # Check if the user exited the game
            self.check_exit()

            # Pump the server
            self.Pump()
            connection.Pump()
            sleep(0.01)

        # Update the caption
        pygame.display.set_caption("Game ID: {} - Player: {}".format(self.gameID, self.player))

    # Create a function to tell the server what keys are being pressed
    def check_keys(self):

        # Get the keys that are being pressed
        keys = pygame.key.get_pressed()

        # Check which keys were pressed, update the position and notify the server of the update
        if keys[K_UP]:
            self.players[self.player].rect.y -= self.velocity
            self.Send({"action": "move", "x": 0, "y": -self.velocity, "player": self.player, "gameID": self.gameID})
        if keys[K_DOWN]:
            self.players[self.player].rect.y += self.velocity
            self.Send({"action": "move", "x": 0, "y": self.velocity, "player": self.player, "gameID": self.gameID})
        if keys[K_LEFT]:
            self.players[self.player].rect.x -= self.velocity
            self.Send({"action": "move", "x": -self.velocity, "y": 0, "player": self.player, "gameID": self.gameID})
        if keys[K_RIGHT]:
            self.players[self.player].rect.x += self.velocity
            self.Send({"action": "move", "x": self.velocity, "y": 0, "player": self.player, "gameID": self.gameID})

    # Create the function to update the game
    def update(self):

        # Pump the server to check for updates
        connection.Pump()
        self.Pump()

        # Check if the user exited
        self.check_exit()

        # Check if any keys were being pressed
        self.check_keys()

        # Fill the background
        # screen.fill(common.SCREEN_BG_COLOR)

        # Draw the players
        for p in self.players:
            screen.blit(p.img, p.rect)

        # Update the display
        pygame.display.flip()

    # Create a function to receive the start game signal
    def Network_startgame(self, data):
        # Get the game ID and player number from the data
        self.gameID = data['gameID']
        self.player = data['player']
        # Set the game to running so that we enter the update loop
        self.running = True
        # Set the velocity of our player
        self.velocity = data['velocity']

    # Create a function to update a player based on a message from the server
    def Network_position(self, data):

        # Get the player data from the request
        p = data['player']

        # Update the player data
        self.players[p].rect.x = data['x']
        self.players[p].rect.y = data['y']

    # Create a function that lets us check whether the user has clicked to exit (required to avoid crash)
    def check_exit(self):
        # Check if the user exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # exit()


# Create a class to hold our character information
class Player(object):
    # Constructor
    def __init__(self, img):
        # Set our object fields
        self.img = img
        self.rect = img.get_rect()

def draw_repeating_background(background_img):
    background_rect = background_img.get_rect()
    background_rect_width = background_rect.width
    background_rect_height = background_rect.height
    for i in range(int(math.ceil(common.SCREEN_WIDTH / background_rect.width))):
        for j in range(int(math.ceil(common.SCREEN_HEIGHT / background_rect.height))):
            screen.blit(background_img, Rect(i * background_rect_width,
                                             j * background_rect_height,
                                             background_rect_width,
                                             background_rect_height))








# If the file was run and not imported
if __name__ == "__main__":

    # Create the game object
    og = OnlineGame()

    # Every tick update the game
    while True:
        og.update()
        fps_clock.tick(common.FPS)
        draw_repeating_background(common.BG_IMG)
