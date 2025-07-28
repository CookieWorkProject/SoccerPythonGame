import pygame
from objects.BasicObject import BasicObject
class Solid(BasicObject):
    def draw(self,surface):
        pygame.draw.rect(surface, (196, 196, 196), self.rect)
    def drawEditor(self,surface):
        pygame.draw.rect(surface, (196, 196, 196), self.rect)