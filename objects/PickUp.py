import pygame
from objects.BasicObject import BasicObject
class PickUp(BasicObject):
    def __init__(self,*args,name):
        super().__init__(*args)
        self.name = name
    def draw(self,surface):
        pygame.draw.ellipse(surface, (196, 64, 64), self.rect)
        
        