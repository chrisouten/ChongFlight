import pygame
from pygame.locals import *

class Player:
    def __init__(self, screen):
        self.killShot = False
        self.targeting = False
        self.screen = screen
        self.score = 0
        self.multiplier = 1
        self.font = pygame.font.Font('./data/GUNPLAY_.ttf', 36)

    def update(self):
        self.killShot = False
        if pygame.mouse.get_pressed()[0]:
            self.targeting = True
            self.killShot = False
        elif self.targeting:
            self.killShot = True
            self.targeting = False
        
    def addScore(self, score):
        self.score = self.score + score * self.multiplier
        
    def draw(self):
        #Draw the score
        scoreText = self.font.render("SCORE: %s" % self.score, 1, (255, 255, 255))
        scoreTextPos = scoreText.get_rect(centerx = self.screen.get_width()/2)
        self.screen.blit(scoreText, scoreTextPos)
      
