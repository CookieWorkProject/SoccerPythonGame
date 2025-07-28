import pygame
from objects.BasicObject import BasicObject
from objects.Player import Player
from objects.Enemy import Enemy
from objects.Coin import Coin
from util.Controller import Controller
from util.Button import Button
from util.CheckBox import CheckBox
import copy
import math


def startGame(gameObjects,replay,player,draw):
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    # Set up the game window
    if draw:
        screen = pygame.display.set_mode((800, 600))

    # Game loop
    running = True
    FramesSinceStart = 0
    FPS = 60
    clock = pygame.time.Clock()
    while running:
        pygame.event.get()
        if draw:
            screen.fill((0,0,0))
        if FramesSinceStart < len(replay):
            player.controller = replay[FramesSinceStart]
        else:
            running = False
            break
        for a in gameObjects:
            if a.active:
                a.step()
                a.collision()
                if draw:
                    a.draw(screen)
                
        
        if draw:
            pygame.display.update()
            pygame.display.set_caption(str(FramesSinceStart))
       
            
        FramesSinceStart +=1
        clock.tick(60)
    # Quit Pygame
    pygame.quit()
    return gameObjects
    
def testFunc():
    print("Hello world")
def quitGame():
         quit()
        

def addPlayer(gameObjects,pos):
    gameObjects.append(Player(gameObjects,pygame.Rect(pos[0],pos[1],10,10)))
def removeObject(gameObjects,pos):
    removeList = list()
    for a in gameObjects:
        if a.rect.collidepoint(pos):
            removeList.append(a)
    for a in removeList:
        if a in gameObjects:
            gameObjects.remove(a)
            
def alignToGrid(x,roundto):
    return math.floor(x/roundto)*roundto
def LevelDesigner(gameObjects = list()):
    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    # Set up the game window
    screen = pygame.display.set_mode((800 , 700))
    running = True
    FPS = 60
    clock = pygame.time.Clock()
    
    mouse0Release = True
    mouse1Release = True
    #place mode If true places an object if False Deletes
    placeMode = CheckBox(pygame.Rect(0,620,80,20),"Place","Delete")
    #snaps objects to grid
    gridMode = CheckBox(pygame.Rect(0,640,80,20),"Grid Mode","Free Mode")
    
    #ui Objects
    uiObjects = list()
    
    
    uiObjects.append(placeMode)
    uiObjects.append(gridMode)
    
    #gameloop
    while running:
        pygame.event.get()
        screen.fill((0,0,0))
        for a in gameObjects:
            a.drawEditor(screen)
            
            
            
        #draw game dev ui
        pygame.draw.rect(screen, (222, 222, 222), pygame.Rect(0,600,800,100))
        for a in uiObjects:
            a.drawEditor(screen)
            
        if pygame.mouse.get_pressed()[0] and mouse0Release:
            pos = pygame.mouse.get_pos()
            #handle pressing buttons
            mouse0Release = False
            for a in uiObjects:
                if a.rect.collidepoint(pos):
                    a.action()
            #handle placement
            if placeMode.bool:
                if gridMode.bool:
                    newPos = (alignToGrid(pos[0],10),alignToGrid(pos[1],10))
                    
                    addPlayer(gameObjects,newPos)
                else:
                    addPlayer(gameObjects,pos)
            else:
                # handle deletions
                removeObject(gameObjects,pos)
        elif not pygame.mouse.get_pressed()[0]:
            mouse0Release = True
        pygame.display.update()
        
        
        
        
        clock.tick(60)
    pygame.quit()
        


