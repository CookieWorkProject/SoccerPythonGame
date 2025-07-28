import pygame 
class CheckBox:
    def __init__(self,rect,text = "O",altText = "X",bool = True):
        self.text = text
        self.altText = altText
        self.displayText = text
        self.bool = bool
        self.rect = rect
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman', 12)
    
    def drawEditor(self,surface):
        pygame.draw.rect(surface, (32, 32, 32), self.rect)
        self.drawText(surface,self.displayText,(255, 255, 255),self.rect.left,self.rect.top)
    
    
    def action(self,*args):
        self.bool = not self.bool
        print(str(self.displayText))
        if self.bool:
            self.displayText = self.text
        else:
            self.displayText = self.altText
    
        
    def drawText(self,surface,text,color,x,y):
        text_surface = self.font.render(text, False, color)
        surface.blit(text_surface, (x,y))