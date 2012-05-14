import pygame, math
from pygame.locals import *

class Particle:
    def __init__(self, position, angle, velocity):
        self.position = position
        self.angle = angle
        self.velocity = velocity
        
        self.color = (255,255,255)
        
        
    def draw(self, display):
        pygame.draw.circle(display, self.color, self.position, 5)
        
    def update(self):
        self.position = ((int)(self.position[0] + math.sin(self.angle) * self.velocity),  \
            int(self.position[1] + math.cos(self.angle) * self.velocity))
        