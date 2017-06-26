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


# Create a new class to hold our game object
# This extends the connection listener so that we can pump the server for messages
class OnlineGame(ConnectionListener):
    # Constructor
    def __init__(self):

        # Game State
        self.game_state = "Ready"

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

        # Create the Bullets
        self.bullets = pygame.sprite.Group()

        # Create the Guided Bullets
        self.guided = pygame.sprite.Group()

        # Create the items
        self.items = pygame.sprite.Group()

        # Initialize the gameID and player ID
        self.gameID = None
        self.player = None

        # Rank
        self.rank = []

        # Connect to the server
        self.Connect()

        # Set running to false
        self.running = False


    # Create a function to tell the server what keys are being pressed
    def check_keys(self):

        # Get the keys that are being pressed
        keys = pygame.key.get_pressed()

        # Check which keys were pressed, update the position and notify the server of the update
        if keys[K_UP]:
            if self.players[self.player].rect.y >= 0:
                self.players[self.player].rect.y -= self.players[self.player].velocity
                self.Send({"action": "move", "x": 0, "y": -self.players[self.player].velocity, "player": self.player, "gameID": self.gameID})
        if keys[K_DOWN]:
            if self.players[self.player].rect.y <= common.SCREEN_HEIGHT - self.players[self.player].image.get_height():
                self.players[self.player].rect.y += self.players[self.player].velocity
                self.Send({"action": "move", "x": 0, "y": self.players[self.player].velocity, "player": self.player, "gameID": self.gameID})
        if keys[K_LEFT]:
            if self.players[self.player].rect.x >= 0:
                self.players[self.player].rect.x -= self.players[self.player].velocity
                self.Send({"action": "move", "x": -self.players[self.player].velocity, "y": 0, "player": self.player, "gameID": self.gameID})
        if keys[K_RIGHT]:
            if self.players[self.player].rect.x <= common.SCREEN_WIDTH - self.players[self.player].image.get_width():
                self.players[self.player].rect.x += self.players[self.player].velocity
                self.Send({"action": "move", "x": self.players[self.player].velocity, "y": 0, "player": self.player, "gameID": self.gameID})

    def check_collide(self):
        chkBulletCollide = self.players[self.player].collide(self.bullets)
        chkGuidedCollide = self.players[self.player].collide(self.guided)
        chkItemCollide = self.players[self.player].collide(self.items)

        if chkBulletCollide:
            for sprite in self.guided:
                if sprite.target == self.player:
                    self.Send({"action": "removeBullet", "gameID": self.gameID, "bullet": sprite.bulletNum})
            self.Send({"action": "detect", "gameID": self.gameID, "dead": self.player, "bullet": chkBulletCollide})
            self.players[self.player] = None
            self.game_state = "Watch"
        elif chkGuidedCollide:
            for sprite in self.guided:
                if sprite.target == self.player:
                    self.Send({"action": "removeBullet", "gameID": self.gameID, "bullet": sprite.bulletNum})
            self.Send({"action": "detect", "gameID": self.gameID, "dead": self.player, "bullet": chkGuidedCollide})
            self.players[self.player] = None
            self.game_state = "Watch"
        elif chkItemCollide:
            print("Send a message to server on item collide.")
            self.Send({"action": "removeItem", "gameID": self.gameID, "player": self.player, "item": chkItemCollide})
            for sprite in self.items:
                if sprite.bulletNum == chkItemCollide:
                    kind = sprite.kind
                    sprite.kill()
                    break
            self.Send({"action": "itemEffect", "gameID": self.gameID, "player": self.player, "kind": kind})

    def check_item(self):
        chkItemCollide = self.players[self.player].collide(self.items)
        if chkItemCollide:
            self.Send({"action": "removeItem", "gameID": self.gameID, "player": self.player, "item": chkItemCollide})
            for sprite in self.items:
                if sprite.bulletNum == chkItemCollide:
                    kind = sprite.kind
                    sprite.kill()
                    break
            self.Send({"action": "itemEffect", "gameID": self.gameID, "player": self.player, "kind": kind})

    # Create the function to update the game
    def update(self):

        # Pump the server to check for updates
        connection.Pump()
        self.Pump()

        # Check if the user exited
        self.check_exit()

        # Check if any keys were being pressed
        self.check_keys()

        # Draw the players
        for p in self.players:
            if p != None:
                screen.blit(p.image, p.rect)

        # Collide Detection
        if self.players[self.player].status[2] != 1:
            self.check_collide()
        else:
            self.check_item()

        # Draw the bullets
        self.bullets.update()
        self.bullets.draw(screen)

        # Draw the guided bullets
        self.guided.update(self.players)
        self.guided.draw(screen)

        # Draw the items
        self.items.draw(screen)

        # Update the display
        pygame.display.flip()

    def update_watch(self):

        # Pump the server to check for updates
        connection.Pump()
        self.Pump()

        # Check if the user exited
        self.check_exit()

        # Check if any keys were being pressed
        # self.check_keys()

        # Draw the players
        for p in self.players:
            if p != None:
                screen.blit(p.image, p.rect)

        # Draw the bullets
        self.bullets.update()
        self.bullets.draw(screen)

        # Draw the guided bullets
        self.guided.update(self.players)
        self.guided.draw(screen)

        # Update the display
        pygame.display.flip()

     # Create a function to receive the start game signal
    def Network_startgame(self, data):
        # Get the game ID and player number from the data
        self.gameID = data['gameID']
        self.player = data['player']

        # Set the velocity of our player
        self.velocity = data['velocity']
        for i in range(0, common.MAX_PLAYERS):
            self.players[i].velocity = data['velocity']

        # Set the game to running so that we enter the update loop
        self.running = True

        self.game_state = "OnGoing"


    # Create a function to update a player based on a message from the server
    def Network_position(self, data):

        # Get the player data from the request
        p = data['player']

        # Update the player data
        # self.players[p].rect.x = data['x']
        # self.players[p].rect.y = data['y']
        self.players[p].set_pos(data['x'], data['y'])

    # Create a function to update a player based on a message from the server
    def Network_bullets(self, data):
        # Get the player data from the request
        # self.bullets = data['bullets']
        # for i in range(0, len(self.bullets)):
        #     self.bullets[i].image = common.BULLET_IMG

        # print("x: ", data['x'], " / y: ", data['y'], " / hspeed: ", data['hspeed'], " / vspeed: ", data['vspeed'])
        self.bullets.add(Bullet(data['bulletNum'], data['x'], data['y'], data['hspeed'], data['vspeed']))

    def Network_guided(self, data):
        self.guided.add(Guided(data['bulletNum'], data['x'], data['y'], data['squarex'], data['squarey'], data['speed'], data['target']))

    def Network_deadguy(self, data):
        self.players[data['dead']] = None

    def Network_deadbullet(self, data):
        for sprite in self.guided:
            if sprite.bulletNum == data['bullet']:
                sprite.kill()

    def Network_item(self, data):
        self.items.add(Item(data['bulletNum'], data['kind'], data['x'], data['y']))

    def Network_deaditem(self, data):
        for sprite in self.items:
            if sprite.bulletNum == data['item']:
                sprite.kill()

    def Network_itemEffect(self, data):
        if data['kind'] == 0: # size down
            self.players[data['player']].status[0] = 1
            self.players[data['player']].status[1] = 0

            if self.players[data['player']].status[2] == 1:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_small_shield))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_small_shield))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_small_shield))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_small_shield))

            elif self.players[data['player']].status[3] == 1:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_small_trap))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_small_trap))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_small_trap))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_small_trap))

            else:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_small))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_small))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_small))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_small))

        elif data['kind'] == 1: # size up
            self.players[data['player']].status[0] = 0
            self.players[data['player']].status[1] = 1

            if self.players[data['player']].status[2] == 1:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_large_shield))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_large_shield))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_large_shield))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_large_shield))

            elif self.players[data['player']].status[3] == 1:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_large_trap))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_large_trap))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_large_trap))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_large_trap))

            else:
                if data['player'] == 0:
                    self.players[data['player']].set_item(pygame.image.load(common.p1_large))
                elif data['player'] == 1:
                    self.players[data['player']].set_item(pygame.image.load(common.p2_large))
                elif data['player'] == 2:
                    self.players[data['player']].set_item(pygame.image.load(common.p3_large))
                elif data['player'] == 3:
                    self.players[data['player']].set_item(pygame.image.load(common.p4_large))

        elif data['kind'] == 2: # invincible(shield)
            self.players[data['player']].velocity = self.velocity

            if self.players[data['player']].status[0] == 1:
                if self.players[data['player']].status[3] == 1:
                    self.players[data['player']].status[3] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_small))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_small))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_small))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_small))
                else:
                    self.players[data['player']].status[2] = 1
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_small_shield))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_small_shield))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_small_shield))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_small_shield))

            elif self.players[data['player']].status[1] == 1:
                if self.players[data['player']].status[3] == 1:
                    self.players[data['player']].status[3] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_large))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_large))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_large))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_large))
                else:
                    self.players[data['player']].status[2] = 1
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_large_shield))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_large_shield))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_large_shield))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_large_shield))

            else:
                if self.players[data['player']].status[3] == 1:
                    self.players[data['player']].status[3] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_img))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_img))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_img))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_img))
                else:
                    self.players[data['player']].status[2] = 1
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_img_shield))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_img_shield))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_img_shield))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_img_shield))

        elif data['kind'] == 3: # trap
            if self.players[data['player']].status[0] == 1:
                if self.players[data['player']].status[2] == 1:
                    self.players[data['player']].status[2] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_small))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_small))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_small))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_small))
                else:
                    self.players[data['player']].status[3] = 1
                    self.players[data['player']].velocity = self.players[data['player']].velocity * common.VELOCITY_DEPRECIATION
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_small_trap))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_small_trap))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_small_trap))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_small_trap))

            elif self.players[data['player']].status[1] == 1:
                if self.players[data['player']].status[2] == 1:
                    self.players[data['player']].status[2] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_large))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_large))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_large))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_large))
                else:
                    self.players[data['player']].status[3] = 1
                    self.players[data['player']].velocity = self.players[data['player']].velocity * common.VELOCITY_DEPRECIATION
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_large_trap))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_large_trap))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_large_trap))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_large_trap))

            else:
                if self.players[data['player']].status[2] == 1:
                    self.players[data['player']].status[2] = 0
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_img))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_img))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_img))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_img))
                else:
                    self.players[data['player']].status[3] = 1
                    self.players[data['player']].velocity = self.players[data['player']].velocity * common.VELOCITY_DEPRECIATION
                    if data['player'] == 0:
                        self.players[data['player']].set_item(pygame.image.load(common.p1_img_trap))
                    elif data['player'] == 1:
                        self.players[data['player']].set_item(pygame.image.load(common.p2_img_trap))
                    elif data['player'] == 2:
                        self.players[data['player']].set_item(pygame.image.load(common.p3_img_trap))
                    elif data['player'] == 3:
                        self.players[data['player']].set_item(pygame.image.load(common.p4_img_trap))

        elif data['kind'] == 4: # turret
            self.bullets.empty()
            self.guided.empty()

        print(self.players[data['player']].status)

    def Network_end(self, data):
        self.rank.append(data['player'])
        if len(self.rank) == common.MAX_PLAYERS:
            self.game_state = "End"

    # Create a function that lets us check whether the user has clicked to exit (required to avoid crash)
    def check_exit(self):
        # Check if the user exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # exit()


# Create a class to hold our character information
class Player(pygame.sprite.Sprite):
    # Constructor
    def __init__(self, img):
        # Set our object fields
        self.image = img
        self.rect = img.get_rect()

        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

        # Set a status of the player
        self.status = [0, 0, 0, 0] # [sizedown, sizeup, shield, trap]

    def set_pos(self, x, y):
        # 'Positions the block center in x and y location'
        self.rect.x = x - self.centerx
        self.rect.y = y - self.centery

    def set_item(self, img):
        self.image = img

    def collide(self, sprites):
        for sprite in sprites:
            if pygame.sprite.collide_mask(self, sprite):
                return sprite.bulletNum

class Bullet(pygame.sprite.Sprite):

    def __init__(self, bulletNum, x, y, hspeed, vspeed):
        super(Bullet, self).__init__()
        self.image = pygame.image.load(common.BULLET_IMG)
        self.rect = self.image.get_rect()
        self.bulletNum = bulletNum
        self.rect.x = x
        self.rect.y = y
        self.hspeed = hspeed
        self.vspeed = vspeed

        self.set_direction()

    def update(self):
        self.rect.x += self.hspeed
        self.rect.y += self.vspeed
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - self.rect.height or self.rect.x > common.SCREEN_WIDTH:
            return True
        elif self.rect.y < 0 - self.rect.height or self.rect.y > common.SCREEN_HEIGHT:
            return True

    def set_direction(self):
        if self.hspeed > 0:
            self.image = pygame.transform.rotate(self.image, 270)
        elif self.hspeed < 0:
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.vspeed > 0:
            self.image = pygame.transform.rotate(self.image, 180)


class Guided(pygame.sprite.Sprite):
    def __init__(self, bulletNum, x, y, squarex, squarey, speed, target):
        super(Guided, self).__init__()
        self.image = pygame.image.load(common.GUIDED_IMG)
        self.image0 = pygame.image.load(common.GUIDED_IMG)
        self.rect = self.image.get_rect()
        self.bulletNum = bulletNum
        self.rect.x = x
        self.rect.y = y
        self.targetx = squarex
        self.targety = squarey
        self.speed = speed
        self.target = target

        self.set_direction(self.targetx, self.targety)

    def update(self, players):
        if players[self.target] == None:
            return
        self.targetx = players[self.target].rect.x + players[self.target].centerx
        self.targety = players[self.target].rect.y + players[self.target].centery

        velx = math.cos((math.atan2((self.targety) - (self.rect.centery), (self.targetx) - (self.rect.centerx)))) * self.speed
        vely = math.sin((math.atan2((self.targety) - self.rect.centery, (self.targetx) - self.rect.centerx))) * self.speed
        self.rect.x += velx
        self.rect.y += vely

        prerect = self.rect.center
        self.set_direction(self.targetx, self.targety)
        self.rect = self.image.get_rect()
        self.rect.center = prerect
        if self.collide():
            self.kill()

    def collide(self):
        if self.rect.x < 0 - self.rect.height or self.rect.x > common.SCREEN_WIDTH:
            return True
        elif self.rect.y < 0 - self.rect.height or self.rect.y > common.SCREEN_HEIGHT:
            return True

    def set_direction(self, targetx, targety):
        self.image = pygame.transform.rotate(self.image0, (
        270 - (math.atan2((targety - self.rect.centery), (targetx - self.rect.centerx)) * (180 / math.pi))))
        self.oldimage = self.image


class Item(pygame.sprite.Sprite):
    def __init__(self, bulletNum, kind, x, y):
        super(Item, self).__init__()
        self.bulletNum = bulletNum
        self.kind = kind
        if self.kind == 0:
            self.image = pygame.image.load(common.SIZEDOWN)
        elif self.kind == 1:
            self.image = pygame.image.load(common.SIZEUP)
        elif self.kind == 2:
            self.image = pygame.image.load(common.SHIELD)
        elif self.kind == 3:
            self.image = pygame.image.load(common.TRAP)
        elif self.kind == 4:
            self.image = pygame.image.load(common.TURRET)
        else:
            self.image = pygame.image.load(common.RANDOM_BOX)

        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.centerx
        self.rect.y = y - self.rect.centery

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

def ready_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 55)
    big_font = pygame.font.Font(None, 36)
    default_font = pygame.font.Font(None, 28)
    draw_text("Waiting for other players", title_font, screen,
              common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 3, common.RED, common.BLACK)
    draw_text("This game is made for SKKU Data Structure Class", big_font, screen,
              common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 2, common.GREEN, common.BLACK)
    draw_text("(prof. SeungHyun Lee)",
              default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 1.7, common.GREEN, common.BLACK)
    draw_text("developed by KSK, YJH, YJH2, LKH in Jun 2017", default_font, screen,
              common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 1.1, common.GREEN, common.BLACK)
    pygame.display.update()



def game_over_screen(rank):
    default_font = pygame.font.Font(None, 28)
    # Transparent surface
    transp_surf = pygame.Surface((common.SCREEN_WIDTH, common.SCREEN_HEIGHT))
    transp_surf.set_alpha(200)
    screen.blit(transp_surf, transp_surf.get_rect())

    first = "1st: Player " + str(rank[len(rank) - 1])
    second = "2nd: Player " + str(rank[len(rank) - 2])
    draw_text("### RESULT ###", pygame.font.Font(None, 40), screen, common.SCREEN_WIDTH / 2,
              common.SCREEN_HEIGHT / 3, common.RED)
    draw_text(first, default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 2.5, common.GREEN)
    draw_text(second, default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 2.3, common.GREEN)

    if common.MAX_PLAYERS == 2:
        pass
    elif common.MAX_PLAYERS == 3:
        third = "3rd: Player " + str(rank[len(rank) - 3])
        draw_text(third, default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 2.1, common.GREEN)
    elif common.MAX_PLAYERS == 4:
        third = "3rd: Player " + str(rank[len(rank) - 3])
        fourth = "4th: Player " + str(rank[len(rank) - 4])
        draw_text(third, default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 2.1, common.GREEN)
        draw_text(fourth, default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 1.9, common.GREEN)

    draw_text("This windows will be closed in 5 secs.", default_font, screen, common.SCREEN_WIDTH / 2, common.SCREEN_HEIGHT / 1.5, common.GREEN)

    pygame.display.update()
    print(rank)
    sleep(5)
    return "Quit"

def draw_text(text, font, surface, x, y, main_color, background_color=None):
    textobj = font.render(text, True, main_color, background_color)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

# If the file was run and not imported
if __name__ == "__main__":

    # Create the game object
    og = OnlineGame()
    pygame.mixer.music.play(-1)

    # Every tick update the game
    while og.game_state != "Quit":
        if og.game_state == "Ready":
            ready_screen()

            # While the game isn't running pump the server
            while not og.running:
                # Check if the user exited the game
                og.check_exit()

                # Pump the server
                og.Pump()
                connection.Pump()
                sleep(0.01)

            # Update the caption
            pygame.display.set_caption("Game ID: {} - Player: {}".format(og.gameID, og.player))

        elif og.game_state == "OnGoing":
            og.update()
            fps_clock.tick(common.FPS)
            draw_repeating_background(common.BG_IMG)

        elif og.game_state == "Watch":
            og.update_watch()
            fps_clock.tick(common.FPS)
            draw_repeating_background(common.BG_IMG)

            transp_surf = pygame.Surface((common.SCREEN_WIDTH, common.SCREEN_HEIGHT))
            transp_surf.set_alpha(50)
            transp_surf.fill((0, 0, 0))
            screen.blit(transp_surf, transp_surf.get_rect())

        elif og.game_state == "End":
            og.game_state = game_over_screen(og.rank)