import pygame
import copy
from objects.Player import Player
from objects.BasicObject import BasicObject
import numpy
class SoccerBall(BasicObject):
    def __init__(self,*args):
        super().__init__(*args)
        self.xVelo = 0
        self.yVelo = 0
        
    def step(self):
        
        self.rect.left+=self.xVelo
        self.rect.top+=self.yVelo
        self.xVelo-=.05*numpy.sign(self.xVelo)
        self.yVelo-=.05*numpy.sign(self.yVelo)
        if abs(self.xVelo)<.075:
            self.xVelo = 0
        
        if abs(self.yVelo)<.075:
            self.yVelo = 0
        
    def collision(self):
        for a in self.gameObjects:
            if a.active == False or self.rect.colliderect(a) == False :
                continue
            if type(a) == Player:
                
                self.xVelo +=a.controller.getMovementVectors()[0]*3
                self.yVelo +=a.controller.getMovementVectors()[1]*3
                
    
    def draw(self,surface):
        
        pygame.draw.ellipse(surface, (255, 255, 255), self.rect)
        
        
        
        
        
