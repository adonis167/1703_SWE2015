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
    def Network_detect(self, data):
        gameID = data['gameID']
        dead = data['dead']
        bullet = data['bullet']
        self._server.remove_dead_guy(gameID, dead)
        self._server.remove_dead_bullet(gameID, bullet)
    def Network_removeBullet(self, data):
        gameID = data['gameID']
        bullet = data['bullet']
        self._server.remove_dead_bullet(gameID, bullet)
    def Network_removeItem(self, data):
        gameID = data['gameID']
        item = data['item']
        player = data['player']
        self._server.remove_item(gameID, player, item)
    def Network_itemEffect(self, data):
        gameID = data['gameID']
        player = data['player']
        kind = data['kind']
        self._server.item_effect(gameID, player, kind)

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
        self.velocity = 15

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

    def remove_dead_guy(self, gameID, dead):
        g = self.games[gameID]
        # del g.players[dead]
        g.players[dead] = None
        g.deadguys.append(dead)

        # If all the players in game are killed
        if len(g.deadguys) == common.MAX_PLAYERS:
            for i in range(0, len(g.player_channels)):
                # Send a message to update
                for h in range(0, len(g.deadguys)):
                    g.player_channels[i].Send({"action": "end", "player": g.deadguys[h]})
        else:
            # For all the other players send a message to update their position
            for i in range(0, len(g.player_channels)):

                # If we aren't looking at the player that was updated
                if not i == dead:
                    # Send a message to update
                    g.player_channels[i].Send(
                        {"action": "deadguy", "dead": dead})

    def remove_dead_bullet(self, gameID, bullet):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            # Send a message to update
            g.player_channels[i].Send({"action": "deadbullet", "bullet": bullet})

    def remove_item(self, gameID, player, item):
        g = self.games[gameID]
        for i in range(0, len(g.player_channels)):
            # If we aren't looking at the player that was updated
            if not i == player:
                # Send a message to update
                g.player_channels[i].Send({"action": "deaditem", "item": item})

    def item_effect(self, gameID, player, kind):
        g = self.games[gameID]
        if kind == 5:
            newKind = random.randint(0, 4)
        else:
            newKind = kind
        for i in range(0, len(g.player_channels)):
            # Send a message to update
            g.player_channels[i].Send({"action": "itemEffect", "player": player, "kind": newKind})

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

        # Set bullet number
        self.bulletNum = 1

        # Set properties of bullets
        self.min_bullet_speed = 3
        self.max_bullet_speed = 20
        self.odds = 10

        # Set properties of guided bullets
        self.guided_min_speed = 3
        self.guided_max_speed = 10
        self.guided_odds = 30

        # Set properties of items
        self.item_odds = 20

        # Create a pygame.sprite.Group of bullets
        # self.bullets = []
        self.makingBullets = MakingBullets(self)

        # The number of dead players
        self.deadguys = []


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
            if len(self.game.deadguys) == common.MAX_PLAYERS:
                print("The process of making bullets ends.")
                return

            # Basic missile
            if random.randint(1, self.game.odds) == 1:
                print(self.game.bulletNum, " : A basic missile is made.")
                bullet = random_bullet(self.game.bulletNum, random.randint(self.game.min_bullet_speed, self.game.max_bullet_speed))
                self.game.bulletNum += 1

                # For all the other players send a message on bullets
                for i in range(0, len(self.game.player_channels)):
                    # Send a message to update
                    # for h in range(0, len(self.game.bullets)):
                    self.game.player_channels[i].Send(
                        # {"action": "bullets", "x": self.game.bullets[h].x, "y": self.game.bullets[h].y, "hspeed": self.game.bullets[h].hspeed, "vspeed": self.game.bullets[h].vspeed})
                        {"action": "bullets", "bulletNum": bullet.bulletNum, "x": bullet.x, "y": bullet.y, "hspeed": bullet.hspeed,
                         "vspeed": bullet.vspeed})

            # Guided missile
            if random.randint(1, self.game.guided_odds) == 1:
                print(self.game.bulletNum, " : A guided missile is made.")
                guided_bullet = random_guided(self.game.bulletNum, self.game.players, self.game.deadguys, random.randint(self.game.guided_min_speed, self.game.guided_max_speed))
                self.game.bulletNum += 1

                # For all the other players send a message on bullets
                for i in range(0, len(self.game.player_channels)):
                    # Send a message to update
                    self.game.player_channels[i].Send(
                        {"action": "guided", "bulletNum": guided_bullet.bulletNum, "x": guided_bullet.x, "y": guided_bullet.y, "squarex": guided_bullet.squarex,
                         "squarey": guided_bullet.squarey, "speed": guided_bullet.speed, "target": guided_bullet.target})

            # Item
            if random.randint(1, self.game.item_odds) == 1:
                print("An item is made.")
                item = Item(self.game.bulletNum, random.randint(0, 5), random.randint(30, common.SCREEN_WIDTH - 30), random.randint(30, common.SCREEN_HEIGHT - 30))
                self.game.bulletNum += 1
                # For all the other players send a message on bullets
                for i in range(0, len(self.game.player_channels)):
                    # Send a message to update
                    self.game.player_channels[i].Send({"action": "item", "bulletNum": item.bulletNum, "kind": item.kind, "x": item.x, "y": item.y})

class Guided(object):
    def __init__(self, bulletNum, x, y, squarex, squarey, speed, target):
        super(Guided, self).__init__()
        self.x = x
        self.y = y
        self.squarex = squarex
        self.squarey = squarey
        self.speed = speed
        self.target = target
        self.bulletNum = bulletNum

def random_guided(bulletNum, players, deadguys, speed):
    random_or = random.randint(1, 4)
    while True:
        tmpChk = False
        random_target = random.randint(0, common.MAX_PLAYERS-1)
        for deadguy in deadguys:
            if random_target == deadguy:
                tmpChk = True
                break
        if tmpChk == False:
            break

    squarex = players[random_target].x
    squarey = players[random_target].y

    if random_or == 1:  # Up -> Down
        return Guided(bulletNum, random.randint(0, common.SCREEN_WIDTH), 0, squarex, squarey, speed, random_target)
    elif random_or == 2:  # Right -> Left
        return Guided(bulletNum, common.SCREEN_WIDTH, random.randint(0, common.SCREEN_HEIGHT), squarex, squarey, speed, random_target)
    elif random_or == 3:  # Down -> Up
        return Guided(bulletNum, random.randint(0, common.SCREEN_WIDTH), common.SCREEN_HEIGHT, squarex, squarey, speed, random_target)
    elif random_or == 4:  # Left -> Right
        return Guided(bulletNum, 0, random.randint(0, common.SCREEN_HEIGHT), squarex, squarey, speed, random_target)


class Bullet(object):
    def __init__(self, bulletNum, x, y, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.hspeed = hspeed
        self.vspeed = vspeed
        self.bulletNum = bulletNum

def random_bullet(bulletNum, speed):
    random_or = random.randint(1, 4)
    if random_or == 1:  # Up -> Down
        return Bullet(bulletNum, random.randint(0, common.SCREEN_WIDTH), 0, 0, speed)
    elif random_or == 2:  # Right -> Left
        return Bullet(bulletNum, common.SCREEN_WIDTH, random.randint(0, common.SCREEN_HEIGHT), -speed, 0)
    elif random_or == 3:  # Down -> Up
        return Bullet(bulletNum, random.randint(0, common.SCREEN_WIDTH), common.SCREEN_HEIGHT, 0, -speed)
    elif random_or == 4:  # Left -> Right
        return Bullet(bulletNum, 0, random.randint(0, common.SCREEN_HEIGHT), speed, 0)

class Item(object):
    def __init__(self, bulletNum, kind, x, y):
        super(Item, self).__init__()
        self.bulletNum = bulletNum
        self.kind = kind
        self.x = x
        self.y = y

# Start the server, but only if the file wasn't imported
if __name__ == "__main__":

    print("Server starting on ", common.SERVER_ADDRESS, "...\n")

    # Create a server
    s = GameServer()

    # Pump the server at regular intervals (check for new requests)
    while True:
        s.Pump()
        sleep(0.00001)
