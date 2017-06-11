import pygame

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from time import sleep
import common
import random


# Create the channel to deal with our incoming requests from the client
# A new channel is created every time a client connects
class ClientChannel(Channel):
    # Create a function that will respond to a request to move a player
    def Network_move(self, data):
        # Fetch the data top help us identify which game needs to update
        gameID = data['gameID']
        player = data['player']
        x = data['x']
        y = data['y']

        # Call the move function of the server to update this game
        self._server.move_player(x, y, gameID, player)

# Create a new server for our game
class GameServer(Server):
    # Set the channel to deal with incoming requests
    channelClass = ClientChannel

    # Constructor to initialize the server objects
    def __init__(self, *args, **kwargs):

        # Call the super constructor
        Server.__init__(self, *args, **kwargs)

        # Create the objects to hold our game ID and list of running games
        self.games = []
        self.queue = None
        self.gameIndex = 0

        # Set the velocity of our player
        self.velocity = 10

    # Function to deal with new connections
    def Connected(self, channel, addr):

        print("New connection: {}".format(channel))

        # When we receive a new connection
        # Check whether there is a game waiting in the queue

        if self.queue == None:

            # If there isn't someone queueing
            # Set the game ID for the player channel
            # Add a new game to the queue
            channel.gameID = self.gameIndex
            self.queue = Game(channel, self.gameIndex)

        elif len(self.queue.player_channels) < common.MAX_PLAYERS - 1:
            # Set the game index for the currently connected channel
            channel.gameID = self.gameIndex

            # Set the second player channel
            self.queue.player_channels.append(channel)

        elif len(self.queue.player_channels) == common.MAX_PLAYERS - 1:

            # Set the game index for the currently connected channel
            channel.gameID = self.gameIndex

            # Set the 3rd and the 4th players channel
            self.queue.player_channels.append(channel)

            # Send a message to the clients that the game is starting
            for i in range(0, len(self.queue.player_channels)):
                self.queue.player_channels[i].Send(
                    {"action": "startgame", "player": i, "gameID": self.queue.gameID, "velocity": self.velocity})


            # Add the game to the end of the game list
            self.games.append(self.queue)

            # Empty the queue ready for the next connection
            self.queue = None

            # Increment the game index for the next game
            self.gameIndex += 1

            # Start Making Bullets
            self.game.start_making_bullets()

    # Create a function to move the players of a game
    def move_player(self, x, y, gameID, player):

        # Get the game
        g = self.games[gameID]

        # Update the correct player
        g.players[player].move(x, y)

        # For all the other players send a message to update their position
        for i in range(0, len(g.player_channels)):

            # If we aren't looking at the player that was updated
            if not i == player:
                # Send a message to update
                g.player_channels[i].Send(
                    {"action": "position", "player": player, "x": g.players[player].x, "y": g.players[player].y})

    # Create a function to move the bullets of a game
    def move_bullet(self, gameID, player):

        # Get the game
        g = self.games[gameID]

        # For all the other players send a message to update their position
        for i in range(0, len(g.player_channels)):
            # Send a message to update
            g.player_channels[i].Send(
                {"action": "bullets", "player": player, "data": g.bullets})

# Create the game class to hold information about any particular game
class Game(object):
    # Constructor
    def __init__(self, player, gameIndex):
        # Create a list of players
        self.players = []
        self.players.append(Player(common.PLAYER1_POSITION_X, common.PLAYER1_POSITION_Y))
        self.players.append(Player(common.PLAYER2_POSITION_X, common.PLAYER2_POSITION_Y))
        self.players.append(Player(common.PLAYER3_POSITION_X, common.PLAYER3_POSITION_Y))
        self.players.append(Player(common.PLAYER4_POSITION_X, common.PLAYER4_POSITION_Y))

        # Create a sprite group of bullets
        self.bullets = pygame.sprite.Group()
        self.min_bullet_speed = 5
        self.max_bullet_speed = 30
        self.bullets_per_gust = 1
        self.odds = 12

        # Store the network channel of the first client
        self.player_channels = [player]

        # Set the game id
        self.gameID = gameIndex

    def start_making_bullets(self):
        while True:
            sleep(0.0001)
            if random.randint(1, self.odds) == 1:
                for _ in range(0, self.bullets_per_gust):
                    self.bullets.add(random_bullet(random.randint(self.min_bullet_speed, self.max_bullet_speed)))
                    print("a bullet is made.")
            self.bullets.update()


# Create a player class to hold all of our information about a single player
class Player(object):
    # Constructor
    def __init__(self, x, y):
        # Set the x and y
        self.x = x
        self.y = y

    # Create a function to move this player
    def move(self, x, y):
        # Update the variables
        self.x += x
        self.y += y


# class Bullets(object):
#
#     bullets = pygame.sprite.Group()
#     min_bullet_speed = 5
#     max_bullet_speed = 30
#     bullets_per_gust = 1
#     odds = 12
#
#     while True:
#         sleep(0.0001)
#         if random.randint(1, odds) == 1:
#             for _ in range(0, bullets_per_gust):
#                 bullets.add(random_bullet(random.randint(min_bullet_speed, max_bullet_speed)))
#         bullets.update()

class Bullet(object):
    def __init__(self, x, y, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.hspeed = hspeed
        self.vspeed = vspeed

    def update(self):
        self.x += self.hspeed
        self.y += self.vspeed


def random_bullet(speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # Up -> Down
        return Bullet(random.randint(0, common.SCREEN_WIDTH), 0, 0, speed)
    elif random_or == 2:  # Right -> Left
        return Bullet(common.SCREEN_WIDTH, random.randint(0, common.SCREEN_HEIGHT), -speed, 0)
    elif random_or == 3:  # Down -> Up
        return Bullet(random.randint(0, common.SCREEN_WIDTH), common.SCREEN_HEIGHT, 0, -speed)
    elif random_or == 4:  # Left -> Right
        return Bullet(0, random.randint(0, common.SCREEN_HEIGHT), speed, 0)


# Start the server, but only if the file wasn't imported
if __name__ == "__main__":

    print("Server starting on ", common.SERVER_ADDRESS, "...\n")

    # Create a server
    s = GameServer()

    # Pump the server at regular intervals (check for new requests)
    while True:
        s.Pump()
        sleep(0.0001)
