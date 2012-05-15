import pygame, random
from pygame.locals import *

#Need to set value and image

class Baddie(pygame.sprite.Sprite):
    def __init__(self, player, position, pm):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.pm = pm
        self.lockon = False
        self.rect = self.image.get_rect()
        self.rect.center = position

class BlueBaddie(Baddie):
    def __init__(self, player, position, pm, value):
        Baddie.__init__(self, player, position, pm)
        self.value = value
        
    def update(self, kill=None):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
            and not self.lockon \
            and len(self.player.targets) < 5:
                self.lockon = True
                self.player.addTarget(self.rect.center)
        if kill and self.lockon:
            self.pm.make_explosion(self.rect.center)
            self.player.addScore(self.value)
            self.kill()
            
class RedBaddie(Baddie):
    def __init__(self, player, position, pm):
        Baddie.__init__(self, player, position, pm)
        
    def update(self, kill=None):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                #TODO : Call player you dead function
                print 'you died'