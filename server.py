from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

from time import sleep
import common
import random

import threading


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

            g = self.queue
            g.makingBullets.daemon = True
            g.makingBullets.start()

            # Add the game to the end of the game list
            self.games.append(self.queue)

            # Empty the queue ready for the next connection
            self.queue = None

            # Increment the game index for the next game
            self.gameIndex += 1

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

        # Store the network channel of the first client
        self.player_channels = [player]

        # Set the game id
        self.gameID = gameIndex

        # Set properties of bullets
        self.min_bullet_speed = 2
        self.max_bullet_speed = 10
        self.bullets_per_gust = 1
        self.odds = 10

        # Create a pygame.sprite.Group of bullets
        # self.bullets = []
        self.makingBullets = MakingBullets(self)

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

class MakingBullets(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        self.game = game

    def run(self):
        while True:
            sleep(0.167)

            if random.randint(1, self.game.odds) == 1:
                for _ in range(0, self.game.bullets_per_gust):
                    bullet = random_bullet(random.randint(self.game.min_bullet_speed, self.game.max_bullet_speed))

                # For all the other players send a message on bullets
                for i in range(0, len(self.game.player_channels)):
                    # Send a message to update
                    # for h in range(0, len(self.game.bullets)):
                        self.game.player_channels[i].Send(
                            # {"action": "bullets", "x": self.game.bullets[h].x, "y": self.game.bullets[h].y, "hspeed": self.game.bullets[h].hspeed, "vspeed": self.game.bullets[h].vspeed})
                        {"action": "bullets", "x": bullet.x, "y": bullet.y, "hspeed": bullet.hspeed, "vspeed": bullet.vspeed})

class Bullet(object):
    def __init__(self, x, y, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.hspeed = hspeed
        self.vspeed = vspeed

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
