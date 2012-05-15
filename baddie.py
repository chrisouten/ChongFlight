import pygame, random
from pygame.locals import *

class Baddie(pygame.sprite.Sprite):
    bombprob = 350
    def __init__(self, player, distance, screenwidth, screenheight, pm):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.player = player
        self.pm = pm
        self.lockon = False
        self.image = random.choice(self.imagesets)
        self.distance = distance
        self.value = 200
        self.image = pygame.transform.scale(self.image, (distance, distance))
        self.rect = self.image.get_rect()
        self.rect.left = random.randrange(self.rect.width * 2, screenwidth - self.rect.width - distance * 2)
        self.rect.bottom = random.randrange(self.rect.height * 2, screenheight - self.rect.height - distance * 2)

        self.bullet = None
        
    def update(self, kill=None):
        #if not random.randrange(self.bombprob) and self.bullet is None:
        #    self.bullet = Bullet(self)
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
            and not self.lockon \
            and len(self.player.targets) < 5:
                self.lockon = True
                self.player.addTarget(self.rect.center)
        if kill and self.lockon:
            self.pm.make_explosion(self.rect.center)
            self.player.addScore(self.value)
            if self.bullet:
                self.bullet.kill()
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, baddie):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.baddie = baddie
        self.rect = self.image.get_rect()
        self.rect.center = baddie.rect.center
        self.distance = 30
        self.counter = 0
        print dir(self.image)
        

    def update(self, kill=None):
        self.counter = self.counter + 1
        if self.counter % 10 == 0:
            self.distance = self.distance + 10
            self.image = pygame.transform.smoothscale(self.image, (self.distance, self.distance))
            self.rect = self.image.get_rect()
            self.rect.center = self.baddie.rect.center
            #self.rect.x = self.rect.x - 10
            #self.rect.y = self.rect.y + 10
            #self.rect = self.image.get_rect()
            #self.rect.center = self.baddie.rect.center