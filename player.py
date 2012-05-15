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
        
    def addTarget(self, targetLocation):
        self.targets.append(targetLocation)
        self.crosshairs.append(Crosshair(targetLocation, self.crosshairImage))
        
    def draw(self):
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
