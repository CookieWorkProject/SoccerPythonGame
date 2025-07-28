import pygame 
class Button:
    def __init__(self,rect,action,text = "Button"):
        self.text = text
        self.action = action
        self.rect = rect
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman', 12)
    
    def drawEditor(self,surface):
        pygame.draw.rect(surface, (32, 32, 32), self.rect)
        self.drawText(surface,self.text,(255, 255, 255),self.rect.left,self.rect.top)
    
    
    def action(self,*args):
        self.action(*args)
        
    def drawText(self,surface,text,color,x,y):
        text_surface = self.font.render(text, False, color)
        surface.blit(text_surface, (x,y))