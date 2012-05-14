import pygame, random
from pygame.locals import *

from baddie import Baddie
from spritesheet import SpriteSheet

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
    
    Baddie(100, SCREENRECT.width, SCREENRECT.height)
    Baddie(50, SCREENRECT.width, SCREENRECT.height)
    
    clock = pygame.time.Clock()        
    
    killShot = False
    targeting = False
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            
        keystate = pygame.key.get_pressed()
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
        if pygame.mouse.get_pressed()[0]:
            targeting = True
            killShot = False
        elif targeting:
            killShot = True
            targeting = False
        #Update
        all.update(killShot)
        #Draw
        screen.fill((0,0,0))
        all.draw(screen)
        pygame.display.flip()



if __name__ == '__main__': main()