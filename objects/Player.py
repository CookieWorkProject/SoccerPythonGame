import pygame
from objects.Solid import Solid
from objects.BlockLeft import BlockLeft
from objects.BlockRight import BlockRight
from objects.BlockUp import BlockUp
from objects.BlockDown import BlockDown
from objects.BasicObject import BasicObject
from objects.Coin import Coin
from objects.Enemy import Enemy
from objects.PickUp import PickUp
from objects.Buff import *
from util.Controller import Controller
import numpy
import copy
class Player(BasicObject):
    def __init__(self,*args):
        super().__init__(*args) 
        
        self.controller = Controller()
        self.hp = 3
        self.knockback = 0
        self.knockbackX = 0
        self.knockbackY = 0
        self.knockbackPower = 0
        self.experience = 0
        self.exp = 0
        self.font = pygame.font.SysFont('Times New Roman', 30)
        #value storing the minimum exp to reach a level
        self.levelReq = [0,3,9]
        self.inventoryOpen = False
        self.inventoryState = "Use" 
        
        
        
        self.inventory = {}
        self.buffs = {}
        self.equipment = list()
        
        self.itemLimit = 6
        
        
        
        
        self.inventorySelection = 0
        self.inventorySelectionMax = 1
        self.menuSelection = 0
        self.menuSelectionMax = 1
        
        
        
    def getAngleBonus(self):
        
        return self.buffs.get("angle",Buff(value = 0)).value
    def getSpeedBonus(self):
        return self.buffs.get("speed",Buff(value = 1)).value
    def getLevel(self):
        
        if self.exp>self.levelReq[2]:
            return 3
        if self.exp>self.levelReq[1]:
            return 2
        return 1
    def getHPMax(self):
        if self.exp>self.levelReq[2]:
            return 7
        if self.exp>self.levelReq[1]:
            return 5
        return 3
    def getPower(self):
        return self.getLevel()
    def gainExp(self,exp):
        if exp <0:
            self.exp += exp
            if self.hp > self.getHPMax():
                self.hp = self.getHPMax()
            return
        if self.getLevel()>=len(self.levelReq):
            self.exp += exp
        elif (self.exp +exp) >= self.levelReq[self.getLevel()]:
            self.exp += exp
            self.hp = self.getHPMax()
        else:
            self.exp += exp           
    def step(self):
        if self.inventoryOpen:
            self.pauseActions()
        elif self.inventoryOpen == False and self.knockback<1:#movement available
            self.stepMovement()
        #any state
        self.knockbackMovement()
        self.checkForPause()
        self.buffStep()
        
    def buffStep(self):
        for a in list(self.buffs.items()):
            a[1].time-=1
            
            if a[1].time<0:
                del self.buffs[a[0]]

        
    def pauseActions(self):
        if self.controller.up == True:
            self.inventorySelection-=1
        if self.controller.down == True:
            self.inventorySelection+=1
        if self.controller.right == True:
            self.menuSelection+=1
        if self.controller.left == True:
            self.menuSelection-=1
        
        if self.menuSelection == 0: #item menu loop
            if self.inventorySelection<0:
                self.inventorySelection = len(self.inventory)
            if self.inventorySelection>len(self.inventory):
                self.inventorySelection = 0
        else:#equip menu loop
            if self.inventorySelection<0:
                self.inventorySelection = len(self.equipment)
            if self.inventorySelection>=len(self.equipment):
                self.inventorySelection = 0
            if len(self.equipment)==0:
                self.menuSelection=0
        #loop menu        
        if self.menuSelection<0:
            self.menuSelection = self.menuSelectionMax
        if self.menuSelection>self.menuSelectionMax:
            self.menuSelection = 0
        #use item
        if self.controller.confirm == True:
            self.useItem()
    def useItem(self):
        
        
        # swap modes
        if self.inventorySelection==len(self.inventory) and self.menuSelection == 0:
            if self.inventoryState == "Use":
                self.inventoryState = "Drop"
                return
            else:
                self.inventoryState = "Use"
                return
        
        item =""
        if self.menuSelection == 1:
            if self.inventorySelection < len(self.equipment):
                item = self.equipment[self.inventorySelection]
        else:
            item = list(self.inventory.items())[self.inventorySelection][0]
        
        if self.inventoryState == "Use":
        
            if self.menuSelection == 0:
                if item ==("Blue Potion") and self.inventory[item]>0:
                    self.hp +=3
                    self.inventory[item] -=1
                    self.inventoryOpen = False
                elif item ==("Red Potion"):
                    self.hp = self.getHPMax()
                    self.inventory[item] -=1
                    self.inventoryOpen = False
                elif item ==("Green Potion"):
                    self.buffs["speed"] = GreenPotion()
                    self.inventory[item] -=1
                    self.inventoryOpen = False
                elif item ==("Yellow Potion"):
                    self.buffs["angle"] = YellowPotion()
                    self.inventory[item] -=1
                    self.inventoryOpen = False
                else:
                    if len(self.equipment)<self.itemLimit: #check for space
                        #move item
                        self.equipment.append(item)
                        self.inventory[item] -=1
                        self.inventorySelection = 0
                        
                        
                        
            else:
                #move equipment to inventory
                if item in self.inventory:
                    if item in self.equipment:
                        self.equipment.remove(item)
                        self.equipment[item] +=1
                elif len(self.inventory)<self.itemLimit:#make sure theres spece in inventory
                    if item in self.equipment:
                        self.inventory[item] = 1
                        self.equipment.remove(item)
                self.inventorySelection = 0
                self.menuSelection = 0
                    
        elif self.inventoryState == "Drop":
            if self.menuSelection == 0:
                obj = PickUp(self.gameObjects, copy.copy(self.rect),name=item) 
                self.createObject(obj)
                self.inventory[item] -=1
            else:
                obj = PickUp(self.gameObjects, copy.copy(self.rect),name=item) 
                self.createObject(obj)
                if item in self.equipment:
                    self.equipment.remove(item)
        #open space in inventory
        for k, v in list(self.inventory.items()):
            if v <= 0:
                del self.inventory[k]
        
        
    def checkForPause(self):
        if self.controller.pause == True:
            self.inventorySelection = 0
            self.menuSelection = 0
            self.inventoryState = "Use" 
            self.inventoryOpen = not self.inventoryOpen
            
    def knockbackMovement(self):
        xMove = 0
        yMove = 0
        if self.knockback>0:
            xMove+=self.knockbackX*self.knockbackPower
            yMove+=self.knockbackY*self.knockbackPower
            self.moveSelf(xMove,yMove)
            self.knockback-=1
            #stun eeffect
            if self.knockback<10:
                self.knockbackPower = 0
            
    def stepMovement(self):
        xMove = 0
        yMove = 0
        if self.controller.right:
            xMove+=1*self.getSpeedBonus()
        if self.controller.left:
            xMove-=1*self.getSpeedBonus()
        if self.controller.up:
            yMove-=1*self.getSpeedBonus()
        if self.controller.down:
            yMove+=1*self.getSpeedBonus()
            
        
        

        
        self.moveSelf(xMove,yMove)
            
    def moveSelf(self,xMove,yMove):
        solidList = self.getAllValidSolids(xMove,yMove)
        
        #push in X
        rect = self.getRectOffset(xMove,0)
        if self.meetingList(rect,solidList):
            #collision occured push in self
            while not self.meetingList(self.getRectOffset(numpy.sign(xMove),0),solidList):
                self.rect.left+=numpy.sign(xMove)
            xMove = 0
        #push in X
        rect = self.getRectOffset(0,yMove)
        if self.meetingList(rect,solidList):
            #collision occured push in self
            while not self.meetingList(self.getRectOffset(0,numpy.sign(yMove)),solidList):
                self.rect.top+=numpy.sign(yMove)
            yMove = 0
        #push in both
        rect = self.getRectOffset(xMove,yMove)
        if self.meetingList(rect,solidList):
            #collision occured push in self
            while not self.meetingList(self.getRectOffset(numpy.sign(xMove),numpy.sign(yMove)),solidList):
                self.rect.left+=numpy.sign(xMove)
                self.rect.top+=numpy.sign(yMove)
            xMove = 0
            yMove = 0
        
        
            
        self.rect.left+= xMove
        self.rect.top+= yMove
    def draw(self,surface):
        pygame.draw.ellipse(surface, (0, 255, 0), self.rect)
        if self.inventoryOpen:
            self.drawInventory(surface)
            self.drawStatus(surface)
        else:
            self.drawStatus(surface)
        
    def drawEditor(self,surface):
        pygame.draw.ellipse(surface, (0, 255, 0), self.rect)    
        
    def drawStatus(self,surface):
        status = "Level: "+str(self.getLevel())+"     HP: "+str(self.hp)
        self.drawText(surface,status,(255, 255, 255),0,0)
        
        
    def drawInventory(self,surface):
        
        #inventory
        textCol = (255, 255, 255)
        if self.inventoryState == "Drop":
            textCol = (255, 0, 0)
        pygame.draw.rect(surface, (128, 96, 96), pygame.Rect(0,60,300,400))
        self.drawText(surface,"ITEMS",textCol,0,60)
        
        spacing = 0
        for a in list(self.inventory.items()):
            self.drawText(surface,a[0]+" x"+str(a[1]),(255, 255, 255),30,90+spacing)
            spacing+=30
        if self.inventoryState == "Drop":
            self.drawText(surface,"Use",textCol,30,90+spacing)
        else:
            self.drawText(surface,"Drop",textCol,30,90+spacing)
        #equip
        
        textCol = (255, 255, 255)
        if self.inventoryState == "Drop":
            textCol = (255, 0, 0)
        pygame.draw.rect(surface, (96, 128, 96), pygame.Rect(400,60,300,400))
        self.drawText(surface,"EQUIPMENT",textCol,400,60)
        
        spacing = 0
        for a in list(self.equipment):
            self.drawText(surface,a,(255, 255, 255),430,90+spacing)
            spacing+=30
        
            
        self.drawText(surface,">",textCol,0+self.menuSelection*400,90+30*self.inventorySelection)
    
    
    
    
    
    def enemyCollision(self,gameObjects,a):
        #get vector from player to enemy
        x = self.getAxisDistToObjectX(a)
        y = self.getAxisDistToObjectY(a)
        #If the player isn't moving just take damage
        if self.controller.getMovementVectors() == (0,0):
            self.setKnockback(30,-numpy.sign(x),-numpy.sign(y),3)
            self.hp -=2
            return
        
        angle = abs(self.angle_between_vectors_degrees(self.controller.getMovementVectors(),(x,y)))+self.getAngleBonus()
        enemyDefeated = False
        if angle<15:
            self.setKnockback(30,-numpy.sign(x),-numpy.sign(y),3)
            self.hp -=1
            self.gainExp(-1)
            
        elif angle <30:
            self.setKnockback(20,-numpy.sign(x),-numpy.sign(y),2)
            self.hp -=1
            enemyDefeated = a.takeDamage(self.getPower())
            a.setKnockback(20,self.controller.getMovementVectors()[0],self.controller.getMovementVectors()[1],2)
        else:
            enemyDefeated = a.takeDamage(self.getPower()*2)
            a.setKnockback(30,self.controller.getMovementVectors()[0],self.controller.getMovementVectors()[1],3)
            
        if enemyDefeated:
            self.gainExp(a.exp)
        if self.hp <=0:
                    self.active = False
    
    def pickUpCollision(self,gameObjects,a):
        # if they are in pause mode just return
        if self.inventoryOpen:
            return
        if len(self.inventory)<self.itemLimit:
            #player doesnt have item
            if self.inventory.get(a.name,False)!=False:
                self.inventory[a.name] += 1
            else:
                self.inventory[a.name] = 1
            self.removeObject(a)
            
    #def get all the solid objects that could apply to this objects current movement
    def getAllValidSolids(self,xMove=0,yMove=0):
        
        objects = list()
        for a in self.gameObjects:
            if type(a) == Solid:
                objects.append(a)
            if type(a) == BlockLeft and xMove>=0 and self.getRightX()<a.rect.left+1:
                objects.append(a)
            if type(a) == BlockRight and xMove<=0 and self.rect.left>a.getRightX()-1:
                
                objects.append(a)
            if type(a) == BlockUp and yMove<=0 and self.rect.top>a.getBottomY()-1:
                objects.append(a)
            if type(a) == BlockDown and yMove>=0 and self.getBottomY()<a.rect.top+1:
                objects.append(a)    
        #print("getAllValidSolids: "+str(len(objects)))
        #print("xpos: "+str(self.rect.left))
        return objects
        
    
    def collision(self):
        for a in self.gameObjects:
            if a.active == False or self.rect.colliderect(a) == False or self.knockback>0:
                continue
            if type(a) == Coin:
                a.active = False
                
            elif type(a) == Enemy:
                self.enemyCollision(self.gameObjects,a)
            elif type(a) == PickUp:
                if self.controller.confirm:
                    self.pickUpCollision(self.gameObjects,a)
                
    def setKnockback(self,frames,x,y,power):
        self.knockback = frames
        self.knockbackX = x
        self.knockbackY = y
        self.knockbackPower = power