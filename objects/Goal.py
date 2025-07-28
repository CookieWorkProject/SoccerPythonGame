import pygame
from objects.SoccerBall import SoccerBall
from objects.BasicObject import BasicObject
class Goal(BasicObject):
    def __init__(self,*args):
        super().__init__(*args)
        self.team = 0
        self.points = 0
    
    def collision(self):
        for a in self.gameObjects:
            if a.active == False or self.rect.colliderect(a) == False :
                continue
            if type(a) == SoccerBall:
                self.points +=1
                a.rect.top = 400
                a.rect.left = 400
                a.xVelo = 0
                a.yVelo = 0
    
    def draw(self,surface):
        pygame.draw.rect(surface, (64, 64, 64), self.rect)
        self.drawText(surface,str(self.points),(255,255,255),self.getCenterX(),self.getCenterY())
        