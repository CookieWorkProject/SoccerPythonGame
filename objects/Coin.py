import pygame
from objects.BasicObject import BasicObject
class Coin(BasicObject):
    def draw(self,surface):
        pygame.draw.ellipse(surface, (255, 255, 0), self.rect)
