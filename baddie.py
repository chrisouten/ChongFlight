import pygame, random
from pygame.locals import *

class Baddie(pygame.sprite.Sprite):
    def __init__(self, player, distance, screenwidth, screenheight):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.lockon = False
        self.image = random.choice(self.imagesets)
        self.distance = distance
        self.image = pygame.transform.scale(self.image, (distance, distance))
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(screenwidth - self.rect.width)
        self.rect.bottom = random.randrange(screenheight - self.rect.height)
        
    def update(self, kill=None):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
            and not self.lockon \
            and len(self.player.targets) < 5:
                self.lockon = True
                self.player.addTarget(self.rect.center)
        if kill and self.lockon:
            self.kill()
