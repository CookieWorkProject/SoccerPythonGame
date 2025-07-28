import pygame
from objects.BasicObject import BasicObject
class BlockUp(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        self.font = pygame.font.SysFont('Times New Roman', 16)
    
    
    def draw(self,surface):
        pygame.draw.rect(surface, (32, 196, 196), self.rect)
        self.drawText(surface,"v",(255, 255, 255),self.getCenterX(),self.getCenterY())
        
    def drawEditor(self,surface):
        pygame.draw.rect(surface, (32, 196, 196), self.rect)
        self.drawText(surface,"v",(255, 255, 255),self.getCenterX(),self.getCenterY())