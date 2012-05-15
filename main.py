import pygame, random
from pygame.locals import *

from baddie import BlueBaddie, RedBaddie
from spritesheet import SpriteSheet
from player import Player, Crosshair
from particle import ParticleManager

try:
    import android
except ImportError:
    android = None
    
SCREENRECT = Rect(0,0,480,800)



def main():
    pygame.init()
    pygame.font.init()
  
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    spritesheet = SpriteSheet('spriteSheet.png')
    
    BlueBaddie.image = spritesheet.imgat((0, 32, 32, 32), -1)
    RedBaddie.image = spritesheet.imgat((0,64, 32, 32), -1)
        
    pygame.display.set_caption('Chong Flight')
    
    
    blueBaddieGroup = pygame.sprite.Group()
    redBaddieGroup = pygame.sprite.Group()
    crosshairsGroup = pygame.sprite.Group()
    all = pygame.sprite.RenderPlain()
    blueBaddieRender = pygame.sprite.RenderPlain()
    redBaddieRender = pygame.sprite.RenderPlain()
    crosshairRender = pygame.sprite.RenderPlain()
    
    BlueBaddie.containers = blueBaddieGroup, blueBaddieRender, all
    RedBaddie.containers = redBaddieGroup, redBaddieRender, all
    Crosshair.containers = crosshairsGroup, crosshairRender, all
    player = Player(screen, spritesheet.imgat((0, 0, 32, 32), -1))
    
    particleManager = ParticleManager(screen)
    clock = pygame.time.Clock()        
    
    killShot = False
    targeting = False
    initial_target = None
    while 1:
        clock.tick(60)
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            
        keystate = pygame.key.get_pressed()
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
        if len(blueBaddieGroup) == 0:
            for x in range(5):
                position = (x * 50, x * 100)
                BlueBaddie(player, position, particleManager, 200)
            position = (200,500)
            RedBaddie(player, position, particleManager)
            
        #Update
        all.update(player.killShot)
        player.update()
        particleManager.update()
        particleManager.draw()
        
        #Draw
        player.draw()
        blueBaddieRender.draw(screen)
        redBaddieRender.draw(screen)
        crosshairRender.draw(screen)
        pygame.display.flip()



if __name__ == '__main__': main()