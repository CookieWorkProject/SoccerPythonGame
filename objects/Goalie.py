import pygame
import random
import numpy
from objects.BasicObject import BasicObject
from objects.SoccerBall import SoccerBall
from objects.Goal import Goal
class Goalie(BasicObject):
    def __init__(self,*args):
        super().__init__(*args)
        self.hasBall = False
        self.team = 1
        
    def draw(self,surface):
        pygame.draw.ellipse(surface, (255, 0, 0), self.rect)
        
        
    def collision(self):
        collisionThisFrame = False
        for a in self.gameObjects:
            if a.active == False or self.rect.colliderect(a) == False :
                continue
            if type(a) == SoccerBall:
                if not self.hasBall:
                    self.kickBall(a)
                    self.hasBall = True
                collisionThisFrame = True
        self.hasBall = collisionThisFrame
    def kickBall(self,ball):
        
        targets = self.getTargetList()
        #failsafe for no targets
        if len(targets)<1:
            print("no targets found")
            return
        target = targets[random.randint(0, len(targets)-1)]
        
        vector = (self.getAxisDistToObjectX(target),self.getAxisDistToObjectY(target))
        
        normalVector = self.normalizeVector(vector)
        
        randSpeed = random.randint(3,6)
        ball.xVelo = normalVector[0] * randSpeed
        ball.yVelo = normalVector[1] * randSpeed
        
        
        
    def getTargetList(self):
        targets = list()
        selfVector = self.getCenterVector()
        
        for a in self.gameObjects:
            if a.active == False or a == self:
                continue
            otherVector = a.getCenterVector()
            if type(a) == Goalie:
                if a.team == self.team and numpy.linalg.norm(numpy.array(selfVector) - numpy.array(otherVector))<100:
                    targets.append(a)
            if type(a) == Goal:
                if a.team == self.team and numpy.linalg.norm(numpy.array(selfVector) - numpy.array(otherVector))<100:
                    targets.append(a)
        return targets