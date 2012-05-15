import pygame, random
from pygame.locals import *

#Need to set value and image

class Baddie(pygame.sprite.Sprite):
    def __init__(self, baddieManager, position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.bm = baddieManager
        self.lockon = False
        self.rect = self.image.get_rect()
        self.rect.center = position

class BlueBaddie(Baddie):
    def __init__(self, baddieManager, position, value):
        Baddie.__init__(self, baddieManager, position)
        self.value = value
        self.crosshair = None
        
    def update(self, kill=None):
        if (self.crosshair):
            self.crosshair.rect.center = self.rect.center
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
            and not self.lockon \
            and len(self.bm.targets) < 5:
                self.lockon = True
                self.crosshair = Crosshair(self.rect.center)
                self.bm.addTarget(self)
        if kill and self.lockon:
            self.bm.particleManager.make_explosion(self.rect.center)
            self.bm.player.addScore(self.value)
            self.crosshair.kill()
            self.kill()
            
class BackAndForthBlueBaddie(BlueBaddie):
    def __init__(self, baddieManager, position, value):
        BlueBaddie.__init__(self, baddieManager, position, value)
        self.timer = 0
        self.max = 50
        self.goRight = True
        
    def update(self, kill=None):
        if (self.timer == self.max):
            self.goRight = False
        if (self.timer == 0):
            self.goRight = True
        
        if (self.goRight):
            self.timer = self.timer + 1
            self.rect.move_ip(2, 0)
        else:
            self.timer = self.timer - 1
            self.rect.move_ip(-2, 0)
            
        BlueBaddie.update(self, kill)
            
class RedBaddie(Baddie):
    def __init__(self, baddieManager, position, value):
        Baddie.__init__(self, baddieManager, position)
        
    def update(self, kill=None):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                #TODO : Call player you dead function
                print 'you died'
                
class BaddieManager():
    waves = [
        [
            ((100,100), RedBaddie, 500),
            ((200,300), BlueBaddie, 200)
            
        ],
        [
            ((250,500), BlueBaddie, 200),
            ((100,100), BlueBaddie, 200),
            ((200,600), BackAndForthBlueBaddie, 200)
        ]
    ]
    def __init__(self, player, particleManager, screen):
        self.player = player
        self.particleManager = particleManager
        self.screen = screen
        self.currentBaddies = []
        self.targets = []
        
        
    def getWave(self):
        self.targets = []
        for b in self.currentBaddies:
            b.kill()
        wave = random.choice(self.waves)
        for info in wave:
            self.currentBaddies.append(info[1](self, info[0], info[2]))
            
    def addTarget(self, baddie):
        self.targets.append(baddie)
        self.player.multiplier = len(self.targets)
        
    def draw(self):
        #Draw the targeting system
        if self.player.targeting:
            for x in range(len(self.targets)):
                try:
                    pygame.draw.line(self.screen, (255,255,255, 50), self.targets[x].rect.center, self.targets[x+1].rect.center, 10)
                except IndexError:
                    pygame.draw.line(self.screen, (255,255,255, 50), self.targets[x].rect.center, pygame.mouse.get_pos(), 10)
            
    

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = position
        