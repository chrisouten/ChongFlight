import pygame, random
from pygame.locals import *

class Baddie(pygame.sprite.Sprite):
    def __init__(self, distance, screenwidth, screenheight):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = random.choice(self.imagesets)
        self.distance = distance
        self.image = pygame.transform.scale(self.image, (distance, distance))
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(screenwidth - self.rect.width)
        self.rect.bottom = random.randrange(screenheight - self.rect.height)
        
    def update(self):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                self.kill()
