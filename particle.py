import pygame, math
from pygame.locals import *

class Particle:
    def __init__(self, position, angle, velocity):
        self.position = position
        self.angle = angle
        self.velocity = velocity
        self.color = (255,255,255)
        self.lifespan = 25
        self.remove = False
        
    def draw(self, display):
        pygame.draw.circle(display, self.color, self.position, 1)
        
    def update(self):
        self.position = ((int)(self.position[0] + math.sin(self.angle) * self.velocity),  \
            int(self.position[1] + math.cos(self.angle) * self.velocity))
        self.lifespan = self.lifespan - 1
        if (self.lifespan <= 0):
            self.remove = True

class ParticleManager:
    def __init__(self, screen):
        self.particles = []
        self.screen = screen

    def make_explosion(self, position):
        for x in range(20):
            self.particles.append(Particle(position, 1.4 * x, 20))
        

    def update(self):
        for p in self.particles:
            p.update()
            if p.remove:
                self.particles.remove(p)
            

    def draw(self):
        for p in self.particles:
            p.draw(self.screen)

        