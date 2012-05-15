import pygame
from pygame.locals import *

class Player:
    def __init__(self, screen, crosshair):
        self.killShot = False
        self.targeting = False
        self.targets = []
        self.screen = screen
        self.crosshairImage = crosshair
        self.crosshairs = []
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
            self.targets = []
            for ch in self.crosshairs:
                ch.kill()
            self.crosshairs = []
        
    def addTarget(self, targetLocation):
        self.targets.append(targetLocation)
        self.crosshairs.append(Crosshair(targetLocation, self.crosshairImage))
        self.multiplier = len(self.targets)
    
    def addScore(self, score):
        self.score = self.score + score * self.multiplier
        
    def draw(self):
        #Draw the score
        scoreText = self.font.render("SCORE: %s" % self.score, 1, (255, 255, 255))
        scoreTextPos = scoreText.get_rect(centerx = self.screen.get_width()/2)
        self.screen.blit(scoreText, scoreTextPos)
        
        #Draw the targeting system
        if self.targeting:
            for x in range(len(self.targets)):
                try:
                    pygame.draw.line(self.screen, (255,255,255, 50), self.targets[x], self.targets[x+1], 10)
                except IndexError:
                    pygame.draw.line(self.screen, (255,255,255, 50), self.targets[x], pygame.mouse.get_pos(), 10)


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, position, image):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
