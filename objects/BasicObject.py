import pygame
import math
import numpy
class BasicObject:
    def __init__(self,gameObjects,rect):
        pygame.font.init()
        self.rect = rect
        self.active = True
        self.gameObjects = gameObjects
        self.font = pygame.font.SysFont('Times New Roman', 8)
    def step(self):
        pass
    def draw(self,surface):
        pass
    def drawEditor(self,surface):
        pass
    def collision(self):
        pass
    def getCenterX(self):
        return self.rect.left+self.rect.width/2
    def getCenterY(self):
        return self.rect.top+self.rect.height/2
    
    def getBottomY(self):
        return self.rect.top+self.rect.height
    def getRightX(self):
        return self.rect.left+self.rect.width
    def angle_between_vectors_degrees(self,u, v):
        dot_product = sum(i*j for i, j in zip(u, v))
        norm_u = math.sqrt(sum(i**2 for i in u))
        norm_v = math.sqrt(sum(i**2 for i in v))
        cos_theta = dot_product / (norm_u * norm_v)
        angle_rad = math.acos(cos_theta)
        angle_deg = math.degrees(angle_rad)
        return angle_deg
    def getAxisDistToObjectX(self,other):
        return other.getCenterX()-self.getCenterX()
    def getAxisDistToObjectY(self,other):
        return other.getCenterY()-self.getCenterY()
    def getCenterVector(self):
        return (self.getCenterX(),self.getCenterY())
    def createObject(self,obj):
        self.gameObjects.append(obj)
        
    def removeObject(self,obj):
        if obj in self.gameObjects:
            self.gameObjects.remove(obj)
        
    def drawText(self,surface,text,color,x,y):
        text_surface = self.font.render(text, False, color)
        surface.blit(text_surface, (x,y))
    
        
        #check if there is a collision between self and an object of the given type    
    def meetingObjects(self,rect,objectType):
        objects = list()
        for a in self.gameObjects:
            if type(a) == objectType and a.active == True and rect.colliderect(a):
                objects.append(a)
                
        return objects
        
    def meetingObjectType(self,rect,objectType):
        
        for a in self.gameObjects:
            if type(a) == objectType and a.active == True and rect.colliderect(a):
                return True
    #check if meeting a group of objects in a list
    def meetingList(self,rect,objects):
        
        for a in objects:
            if a.active == True and rect.colliderect(a):
                return True            
        return False
    
                
    #returns a rect with the same values as this one off set by a certain amount
    def getRectOffset(self,x = 0,y = 0):
        return pygame.Rect(self.rect.left+x,self.rect.top+y,self.rect.width,self.rect.height)
        
    def normalizeVector(self,vector):
        length = numpy.linalg.norm(numpy.array(vector))
        if length == 0:
            return (0,0)
        return (vector[0]/length,vector[1]/length)