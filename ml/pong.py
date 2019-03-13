# Filip Munteanu 342C4
import random
import pygame, sys
from pygame.locals import *

from copy import copy
from random import choice

ACTIONS = ["UP", "STAY", "DOWN"]
ACTION_EFFECTS = {
    "UP": -1,
    "DOWN": 1,
    "STAY": 0
}

#HIT_REWARD = 1.0
WIN_REWARD = 1.0
LOSE_REWARD = -1.0

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)

DIV = 1
UNIT = 20
WIDTH_S = 3
HEIGHT_S = 2


class Game():
    def __init__(self, display_size, pal_size, learning_rate, discount, epsilon, player, adversary):
        self.WIDTH = display_size * WIDTH_S * UNIT
        self.HEIGHT = display_size * HEIGHT_S * UNIT
        self.PAD_WIDTH = UNIT/2
        self.PAD_HEIGHT = pal_size * UNIT
        self.HALF_PAD_WIDTH = self.PAD_WIDTH / 2
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT / 2
        self.BALL_L = UNIT
        self.HALF_BALL_L = self.BALL_L/2
        self.player_vel = 0
        self.advers_vel = 0

        self.learning_rate = learning_rate
        self.discount = discount
        self.epsilon = epsilon
        self.player = player
        self.adversary = adversary

        pygame.init()
    
        
        self.restart()

    def ball_init(self):
        global ball_pos, ball_vel # these are vectors stored as lists
        self.ball_pos = [self.WIDTH/2,self.HEIGHT/2]
        horz = 5
        vert = 5
        
        if random.randrange(0,2) == 0:
            horz = - horz
        if random.randrange(0,2) == 0:
            vert = - vert
        
        self.ball_vel = [horz,-vert]

    # define event handlers
    def restart(self):
        self.player_pos = [self.HALF_PAD_WIDTH,self.HEIGHT/2]
        self.advers_pos = [self.WIDTH - self.HALF_PAD_WIDTH,self.HEIGHT/2]
        self.counter = 0

        self.ball_init()

    def init_draw(self):
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption('Q-Learning')

    #draw function of canvas
    def draw(self):
               
        self.window.fill(BLACK)

        # print "pl_pos: " + str(self.player_pos[1]-self.HALF_PAD_HEIGHT) + "  adv_pos: " + str(self.advers_pos[1]-self.HALF_PAD_HEIGHT)
        #draw paddles and ball
        ball = pygame.Rect(self.ball_pos[0]-self.HALF_BALL_L, self.ball_pos[1]-self.HALF_BALL_L, self.BALL_L, self.BALL_L)
        player = pygame.Rect(self.player_pos[0]-self.HALF_PAD_WIDTH, self.player_pos[1]-self.HALF_PAD_HEIGHT, self.PAD_WIDTH, self.PAD_HEIGHT)
        advers = pygame.Rect(self.advers_pos[0]-self.HALF_PAD_WIDTH, self.advers_pos[1]-self.HALF_PAD_HEIGHT, self.PAD_WIDTH, self.PAD_HEIGHT)
        pygame.draw.rect(self.window, WHITE, ball, 0)
        pygame.draw.rect(self.window, WHITE, player, 0)
        pygame.draw.rect(self.window, WHITE, advers, 0)


        #update scores
        myfont1 = pygame.font.SysFont("Arial", 15)
        label1 = myfont1.render("learning rate "+str(self.learning_rate), 1, (255,255,0))
        self.window.blit(label1, (50,10))

        label2 = myfont1.render("discount "+str(self.discount), 1, (255,255,0))
        self.window.blit(label2, (50, 30))  

        label3 = myfont1.render("epsilon "+str(self.epsilon), 1, (255,255,0))
        self.window.blit(label3, (50, 50))  

        label4 = myfont1.render("player "+str(self.player), 1, (255,255,0))
        self.window.blit(label4, (180, 10))  

        label5 = myfont1.render("adversary "+str(self.adversary), 1, (255,255,0))
        self.window.blit(label5, (180, 30))  
        
        pygame.display.update()
        
    def get_state(self, who):
        if who == "player":
            return (self.player_pos[1]/(UNIT*DIV), self.advers_pos[1]/(UNIT*DIV), self.ball_pos[0]/(UNIT*DIV), self.ball_pos[1]/(UNIT*DIV))
        if who == "advers":
            return (self.advers_pos[1]/(UNIT*DIV), self.player_pos[1]/(UNIT*DIV), (self.WIDTH - self.ball_pos[0])/(UNIT*DIV), self.ball_pos[1]/(UNIT*DIV))

    def is_final_state(self):
        #ball collison check on paddles
        yes = False
        if int(self.ball_pos[0]) <= self.PAD_WIDTH + self.HALF_BALL_L:
            if not ((self.player_pos[1] - self.HALF_PAD_HEIGHT) < int(self.ball_pos[1] + self.HALF_BALL_L) and int(self.ball_pos[1] - self.HALF_BALL_L) < (self.player_pos[1] + self.HALF_PAD_HEIGHT)):
                yes = True
            
        if int(self.ball_pos[0]) >= self.WIDTH - self.HALF_BALL_L - self.PAD_WIDTH:
            if not ((self.advers_pos[1] - self.HALF_PAD_HEIGHT) < int(self.ball_pos[1] + self.HALF_BALL_L) and int(self.ball_pos[1] - self.HALF_BALL_L) < (self.advers_pos[1] + self.HALF_PAD_HEIGHT)):
                yes = True

        if self.counter >= 8:
            yes = True

        return yes

    def apply_action(self, pl_act, adv_act):

        if pl_act == "UP":
            self.player_vel = -5
        elif pl_act == "DOWN":
            self.player_vel = 5
        elif pl_act == "STAY":
            self.player_vel = 0

        if adv_act == "UP":
            self.advers_vel = -5
        elif adv_act == "DOWN":
            self.advers_vel = 5
        elif adv_act == "STAY":
            self.advers_vel = 0

        self.player_pos[1] += self.player_vel
        self.advers_pos[1] += self.advers_vel
        # print "pl: " + pl_act + "  adv: " + adv_act
        # print "pl_pos: " + str(self.player_pos[1]) + "  adv_pos: " + str(self.advers_pos[1]) + " ming: " + str(self.ball_pos[1])

        #ball collision check on top and bottom walls
        if int(self.ball_pos[1]) <= self.HALF_BALL_L:
            self.ball_vel[1] *= -1
        if int(self.ball_pos[1]) >= self.HEIGHT - self.HALF_BALL_L:
            self.ball_vel[1] *= -1

        #update ball
        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])

        reward = 0
        msg = "pl: " + pl_act + "  adv: " + adv_act + "  "
        msg = ""
        if int(self.ball_pos[0]) <= self.PAD_WIDTH + self.HALF_BALL_L:
            if (self.player_pos[1] - self.HALF_PAD_HEIGHT) < int(self.ball_pos[1] + self.HALF_BALL_L) and int(self.ball_pos[1] - self.HALF_BALL_L) < (self.player_pos[1] + self.HALF_PAD_HEIGHT):
                self.ball_vel[0] = -self.ball_vel[0]
                self.counter += 1
                #reward = HIT_REWARD
            else:
                reward = LOSE_REWARD
                msg += "player lost"
            
        if int(self.ball_pos[0]) >= self.WIDTH - self.HALF_BALL_L - self.PAD_WIDTH:
            if (self.advers_pos[1] - self.HALF_PAD_HEIGHT) < int(self.ball_pos[1] + self.HALF_BALL_L) and int(self.ball_pos[1] - self.HALF_BALL_L) < (self.advers_pos[1] + self.HALF_PAD_HEIGHT):
                self.ball_vel[0] = -self.ball_vel[0]
                self.counter += 1
            else:
                reward = WIN_REWARD
                msg += "player won"
        

        return reward, msg

    ## Return the available actions in a given state
    def get_legal_actions(self, who):
        if who == "player":
            if self.player_pos[1] > self.HALF_PAD_HEIGHT and self.player_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
                return ACTIONS
            elif self.player_pos[1] <= self.HALF_PAD_HEIGHT:
                return ["DOWN", "STAY"]
            elif self.player_pos[1] >= self.HEIGHT - self.HALF_PAD_HEIGHT:
                return ["UP", "STAY"]

        if who == "advers":
            if self.advers_pos[1] > self.HALF_PAD_HEIGHT and self.advers_pos[1] < self.HEIGHT - self.HALF_PAD_HEIGHT:
                return ACTIONS
            elif self.advers_pos[1] <= self.HALF_PAD_HEIGHT:
                return ["DOWN", "STAY"]
            elif self.advers_pos[1] >= self.HEIGHT - self.HALF_PAD_HEIGHT:
                return ["UP", "STAY"]

        return copy(ACTIONS)
    


## Return the initial state of the game
def get_initial_state(display_size, pal_size, learning_rate, discount, epsilon, player, adversary):
    global game
    game = Game(display_size, pal_size, learning_rate, discount, epsilon, player, adversary)

    return game
