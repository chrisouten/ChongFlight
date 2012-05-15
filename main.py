import pygame, random
from pygame.locals import *

from baddie import BlueBaddie, RedBaddie, BaddieManager, Crosshair
from spritesheet import SpriteSheet
from player import Player
from particle import ParticleManager

try:
    import android
except ImportError:
    android = None
    
#Screen size
SCREENRECT = Rect(0,0,480,800)



def main():
    #Get our pygame up and running
    pygame.init()
    pygame.font.init()
  
    #Are we on the phone?
    # If so, map the back key to the escape key
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        
    #Setting up the screen
    winstyle = 0
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    pygame.display.set_caption('Chong Flight')

    #Load our spritesheet
    spritesheet = SpriteSheet('spriteSheet.png')
    
    #Setup the images for the sprites 
    BlueBaddie.image = spritesheet.imgat((0, 32, 32, 32), -1)
    RedBaddie.image = spritesheet.imgat((0,64, 32, 32), -1)
    Crosshair.image = spritesheet.imgat((0,0,32,32), -1)
        
    #Set up our sprite groups    
    blueBaddieGroup = pygame.sprite.Group()
    redBaddieGroup = pygame.sprite.Group()
    crosshairsGroup = pygame.sprite.Group()
    
    #Set up all our renderPlains
    all = pygame.sprite.RenderPlain()
    blueBaddieRender = pygame.sprite.RenderPlain()
    redBaddieRender = pygame.sprite.RenderPlain()
    crosshairRender = pygame.sprite.RenderPlain()
    
    #Finally set up our containers for our sprites
    BlueBaddie.containers = blueBaddieGroup, blueBaddieRender, all
    RedBaddie.containers = redBaddieGroup, redBaddieRender, all
    Crosshair.containers = crosshairsGroup, crosshairRender, all
    
    #Make a new player and particle Manager
    player = Player(screen)
    particleManager = ParticleManager(screen)
    
    #Make us a baddie manager
    bm = BaddieManager(player, particleManager, screen)
    
    #Start your clocks!
    clock = pygame.time.Clock()        
    
    #GAME LOOP!!!!!!!!!!
    while 1:
        #60 fps and fill our screen with black death space
        elapsedTime = clock.tick(60)
        screen.fill((0,0,0))
        
        #Check for quiting
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            
        #Check for android pausing
        keystate = pygame.key.get_pressed()
        if android:
            if android.check_pause():
                android.wait_for_resume()
                
        #If all our blue baddies are deaded, we need another wave!
        if len(blueBaddieGroup) == 0:
            bm.getWave()
            
        #Update
        all.update(player.killShot)
        player.update()
        particleManager.update()
        particleManager.draw()
        
        #Draw
        player.draw()
        bm.draw()
        blueBaddieRender.draw(screen)
        redBaddieRender.draw(screen)
        crosshairRender.draw(screen)
        
        #Flip it
        pygame.display.flip()



if __name__ == '__main__': main()