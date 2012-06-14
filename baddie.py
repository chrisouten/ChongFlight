import pygame, random, math
from pygame.locals import *


#default Baddie Class
class Baddie(pygame.sprite.Sprite):
    def __init__(self, baddieManager, position):
        #Standard initing that all the baddies use
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.bm = baddieManager
        self.invulnerable = False
        self.lockon = False
        self.rect = self.image.get_rect()
        self.rect.center = position

##################################
#######    BLUE            #######
#######  BADDIES           #######
##################################
class BlueBaddie(Baddie):
    def __init__(self, baddieManager, position, value):
        Baddie.__init__(self, baddieManager, position)
        #Set our value and init our crosshair
        self.value = value
        self.crosshair = None
        
    def update(self, kill=None):
        #If we have a crosshair we need to update its center
        if (self.crosshair):
            self.crosshair.rect.center = self.rect.center
        
        #If the mouse is pressed and its on our baddie and we aren't already
        # locked on and they haven't locked onto more than 5 and we aren't invicible
        # we need to lock on ourself, make a crosshair, and let our manager know
        # that we have been targeted for destruction
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) \
            and not self.lockon \
            and not self.invulnerable \
            and len(self.bm.targets) < 5:
                self.lockon = True
                self.crosshair = Crosshair(self.rect.center)
                self.bm.addTarget(self)
                
        #If we got a kill message and we are locked on its bye bye birdie
        #  We need to update the player score, let the particleManager know
        # that we need to explode, kill ourselves and our crosshair, and
        # let the manager know to remove our target
        if kill and self.lockon:
            self.destroy()
            
    def destroy(self, explode=True):
        if explode:
            self.bm.particleManager.make_explosion(self.rect.center)
        self.bm.player.addScore(self.value)
        self.bm.removeTarget(self)
        if self.crosshair:
            self.crosshair.kill()
        self.kill()
        
class BackAndForthBlueBaddie(BlueBaddie):
    def __init__(self, baddieManager, position, value):
        BlueBaddie.__init__(self, baddieManager, position, value)
        #Some back and forth goodness
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
        
class ShieldedBaddie(BlueBaddie):
    def __init__(self, baddieManager, position, value):
        BlueBaddie.__init__(self, baddieManager, position, value)
        #Some back and forth goodness
        self.image = RedBaddie.image
        self.timer = 0
        self.shieldTime = 150
        self.invulnerable = True
        
    def update(self, kill=None):
        if (self.timer == self.shieldTime):
            self.invulnerable = False
            self.image = BlueBaddie.image
        if (self.timer <= self.shieldTime):
            self.timer = self.timer + 1
                    
        BlueBaddie.update(self, kill)
        
##################################
#######    RED             #######
#######  BADDIES           #######
##################################
class RedBaddie(Baddie):
    def __init__(self, baddieManager, position):
        Baddie.__init__(self, baddieManager, position)
        
    def update(self, kill=None):
        if (pygame.mouse.get_pressed()[0]):
            if self.rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                #TODO : Call player you dead function
                self.bm.getWave()
                self.bm.player.reset()
                
    def destroy(self, explode=False):
        self.kill()
        
class BackAndForthRedBaddie(RedBaddie):
    def __init__(self, baddieManager, position, max=50):
        RedBaddie.__init__(self, baddieManager, position)
        #Some back and forth goodness
        self.timer = 0
        self.max = max
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
            
        RedBaddie.update(self, kill)
        
class RotatingRedBaddie(RedBaddie):
    def __init__(self, baddieManager, position, rotateCenter):
        RedBaddie.__init__(self, baddieManager, position)
        self.rotateCenter = rotateCenter
        self.angle = 0
        self.angleStep = 50
        self.counter = 0
        
    def update(self, kill=None):
        self.counter = self.counter + 1
        if self.counter % self.angleStep == 0:
            self.angle = self.angle + 1
            self.counter = 0
        if self.angle > 360:
            self.angle = 0
        
        self.rect.center = self.rotatePoint(self.rotateCenter, self.angle)
        RedBaddie.update(self, kill)
        
    def rotatePoint(self, origin, angle):
        sinT = math.sin(math.radians(angle))
        cosT = math.cos(math.radians(angle))
        return (origin[0] + (cosT * (self.rect.centerx - origin[0]) - sinT * (self.rect.centery - origin[1])),
                      origin[1] + (sinT * (self.rect.centerx - origin[0]) + cosT * (self.rect.centery - origin[1])))
                
class BaddieManager():
    waves = [
        [
            (RedBaddie, ((100,100),)),
            (BlueBaddie, ((200,300), 200)),
            (ShieldedBaddie, ((250, 700), 200))
            
        ],
        [
            (BlueBaddie, ((250,500), 200)),
            (BlueBaddie, ((100,100), 200)),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (RotatingRedBaddie, ((100, 200), (110, 200)))
        ],
        [
            (RotatingRedBaddie, ((200,200), (200, 400))),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (BackAndForthBlueBaddie, ((200,400), 200)),
            (BackAndForthBlueBaddie, ((200,200), 200)),
        ],
        [
            (BackAndForthRedBaddie, ((200,600), 25)),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (BackAndForthRedBaddie, ((200,400), 75)),
            (BackAndForthBlueBaddie, ((200,400), 200)),
            (BackAndForthRedBaddie, ((200,200), 25)),
            (BackAndForthBlueBaddie, ((200,200), 200)),
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
        self.player.multiplier = 1
        for b in self.currentBaddies:
            b.destroy(explode=False)
        wave = random.choice(self.waves)
        for info in wave:
            self.currentBaddies.append(info[0](self, *info[1]))
            
    def addTarget(self, baddie):
        self.targets.append(baddie)
        self.player.multiplier = len(self.targets)
        
    def removeTarget(self, baddie):
        try:
            self.targets.remove(baddie)
        except ValueError:
            pass
        
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
        
        
        
        
        
        
        
        
        
        
#################################
#######                    ######
#######   Waves            ######
#######                    ######
#################################

WAVES = {
    0: [
        [
            (RedBaddie, ((100,100),)),
            (BlueBaddie, ((200,300), 200)),
            (ShieldedBaddie, ((250, 700), 200))
            
        ],
        [
            (BlueBaddie, ((250,500), 200)),
            (BlueBaddie, ((100,100), 200)),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (RotatingRedBaddie, ((100, 200), (110, 200)))
        ],
        [
            (RotatingRedBaddie, ((200,200), (200, 400))),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (BackAndForthBlueBaddie, ((200,400), 200)),
            (BackAndForthBlueBaddie, ((200,200), 200)),
        ],
        [
            (BackAndForthRedBaddie, ((200,600), 25)),
            (BackAndForthBlueBaddie, ((200,600), 200)),
            (BackAndForthRedBaddie, ((200,400), 75)),
            (BackAndForthBlueBaddie, ((200,400), 200)),
            (BackAndForthRedBaddie, ((200,200), 25)),
            (BackAndForthBlueBaddie, ((200,200), 200)),
        ]
    ],
    15: [
    ],
    30: [
        
    ]
}
