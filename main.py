import pygame, random
from pygame.locals import *

from baddie import Baddie
from spritesheet import SpriteSheet
from player import Player
from particle import ParticleManager

try:
    import android
except ImportError:
    android = None
    
SCREENRECT = Rect(0,0,480,800)



def main():
    pygame.init()
  
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    spritesheet = SpriteSheet('1945.bmp')
    
    Baddie.imagesets = [
        spritesheet.imgat((4, 466, 32, 32), -1),
        spritesheet.imgat((103, 466, 32, 32), -1),
        spritesheet.imgat((202, 466, 32, 32), -1),
        spritesheet.imgat((301, 466, 32, 32), -1),
        spritesheet.imgat((4, 499, 32, 32), -1)
        ]
    
    pygame.display.set_caption('Chong Flight')
    
    
    baddies = pygame.sprite.Group()
    all = pygame.sprite.RenderPlain()
    
    Baddie.containers = baddies, all
    player = Player(screen)
    
    particleManager = ParticleManager(screen)
    clock = pygame.time.Clock()        
    
    killShot = False
    targeting = False
    initial_target = None
    while 1:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            
        keystate = pygame.key.get_pressed()
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
        if len(baddies) == 0:
            for x in range(5):
                Baddie(player, random.randrange(20,80), SCREENRECT.width, SCREENRECT.height, particleManager)
               
        #Update
        all.update(player.killShot)
        player.update()
        particleManager.update()
        particleManager.draw()
        #Draw
        player.draw()
        all.draw(screen)
        pygame.display.flip()



if __name__ == '__main__': main()