'''
Created on Feb 22, 2014

@author: mack
'''

import os, sys,random
import pygame
from pygame.locals import *
from Helpers import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class Breakout:

    sprBlocks = []
    sprBall = None
    sprBat = None
    highScore =0
    def __init__(self, width=1024,height=768):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width
                                               , self.height))
        freq = 44100    # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2    # 1 is mono, 2 is stereo
        buffersize = 1024    # number of samples
        pygame.mixer.init(freq, bitsize, channels, buffersize)
        pygame.mixer.music.set_volume(0.5)

    def MainLoop(self):
        pygame.key.set_repeat(1, 1)
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0,0,0))
        self.PressSpace(True) 
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
            self.Gameloop()       
            self.PressSpace(False) 
            
    def PressSpace(self,clearscreen):
        if clearscreen==True:
            self.screen.fill((0,0,0))
        self.DrawText(72, "Press Space to Start",self.width/2,278,(255, 255, 255),True,True, True)                               
        exitloop =False
        while exitloop==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key==K_SPACE:
                        exitloop=True
                        
    def Gameloop(self):
        self.screen.fill((0,0,0))
        pygame.display.flip()
        #clock=pygame.time.Clock()
        self.LoadSprites()
        self.play_music()
        self.DrawFrame()
        score=0
        exitloop =False
        while exitloop==False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key==K_z:
                        self.sprBat.setDirection(-1)
                    elif event.key==K_x:
                        self.sprBat.setDirection(1)
                elif event.type == KEYUP:
                    self.sprBat.setDirection(0) 
            self.screen.fill((0,0,0), self.sprBall.rect)
            self.sprBall.move()
            self.screen.blit(self.sprBall.image, self.sprBall.rect)
            self.screen.fill((0,0,0), self.sprBat.rect)
            self.sprBat.move()
            self.screen.blit(self.sprBat.image, self.sprBat.rect)
            if check_collision(self.sprBall, self.sprBat) == True:
                self.sprBall.setYDirection(self.sprBall.ydirection * -1)
                self.sprBall.frameCountToMove =0
            for iLCa in xrange(len(self.sprBlocks)-1,0,-1):
                if check_collision(self.sprBall, self.sprBlocks[iLCa]) == True:
                    self.sprBall.setYDirection(self.sprBall.ydirection * -1)
                    self.sprBall.frameCountToMove =0
                    self.screen.fill((0,0,0), self.sprBlocks[iLCa].rect)
                    score=score+self.sprBlocks[iLCa].score
                    self.sprBlocks.remove(self.sprBlocks[iLCa])
            self.DrawText(24, "Score : " + str(score) + "    ",800,5,(255,255,255),False,False, False)
            if self.sprBall.rect.y>740:
                self.DrawText(72, "Game Over",self.width/2,278,(0,255,0),False,True, True)
                exitloop=True
            if pygame.mixer.music.get_busy()==False:
                self.play_music()
            pygame.display.flip()
    
    def DrawText(self,fontsize,msg,x,y,colour,overWrite,useCenterX,updatescreen):
        font = pygame.font.Font(None, fontsize) 
        text = font.render(msg, 1, colour)   
        if useCenterX==True:
            textpos = text.get_rect(centerx=x,centery=y)
        else:                            
            textpos = text.get_rect(x=x,y=y)
        if overWrite==True : self.screen.fill((0,0,0), textpos)   
        self.screen.blit(text, textpos)
        if updatescreen==True:
            pygame.display.flip()  
        
    def DrawFrame(self):
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(0,30), (1023,30)], 5)
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(0,30), (0,767)], 5)
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(1023,30), (1023,767)], 5)  
        for iLCa in range(0,len(self.sprBlocks)):
            self.screen.blit(self.sprBlocks[iLCa].image, self.sprBlocks[iLCa].rect)
            
    def LoadSprites(self):
        """Load the sprites that we need"""
        self.sprBat = Bat()
        self.sprBat.rect.centerx=512
        self.sprBat.rect.y=700
        self.sprBall = Ball()
        self.sprBall.rect.centerx=512
        self.sprBall.rect.y =683  
        for iLCa in xrange(0,5):
            colour=0
            score=40
            if iLCa<2:
                colour=1
                score=80
            for iLCb in xrange(0,30):
                sprBlock = Brick()
                sprBlock.rect.x=4+ iLCb *34
                sprBlock.rect.y =100+ iLCa *34
                sprBlock.score=score
                sprBlock.setBrickImageFrame(colour)
                self.sprBlocks.append(sprBlock)
   
    def play_music(self):
        filename = os.path.join("Sounds/tune.mid")
        #pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        

 
 
class Brick(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.images=[]
        self.images.append(load_image('Brick-red.png',-1))
        self.images.append(load_image('Brick-purple.png',-1))
        self.images.append(load_image('Brick-red.png',-1))
        self.image = self.images[0]
        self.rect=self.image.get_rect()
        self.hitmask=get_colorkey_hitmask(self.image, self.rect)
        self.currentFrame=0
        self.hitCountLeft=1
        self.score=120
        
    def setBrickImageFrame(self,frame):
        self.currentFrame=frame
        self.image=self.images[frame]
        self.hitmask=get_colorkey_hitmask(self.image, self.rect)


class Bat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.images=[]
        self.images.append(load_image('Bat1.png',-1))
        self.images.append(load_image('Bat1.png',-1))
        self.images.append(load_image('Bat1.png',-1))
        self.image = self.images[0]
        self.rect=self.image.get_rect()
        self.hitmask=get_colorkey_hitmask(self.image, self.rect)
        self.direction=0
        self.currentFrame=0
    def move(self):
        self.image = self.images[self.currentFrame]
        if (self.rect.x+self.direction) >5 and (self.rect.x+self.rect.width+self.direction) <1019: 
            self.rect.move_ip(self.direction*2,0); 
        
    def setDirection(self,direction):
        self.direction=direction
    def setBatImageFrame(self,frame):
        self.currentFrame=frame 
        self.image = self.images[frame]
        self.hitmask=get_colorkey_hitmask(self.image, self.rect) 
           
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.images=[]
        self.images.append(load_image('Ball.png',-1))
        self.image = self.images[0]
        self.rect=self.image.get_rect()
        self.hitmask=get_colorkey_hitmask(self.image, self.rect)
        self.frameCountToMove=1
        self.xdirection=1
        self.ydirection=-1
        self.speed=1
        self.movesbeforenewYdirchange=15
        
    def move(self):
        if self.frameCountToMove>0:
            self.frameCountToMove=self.frameCountToMove-1
            return
        else:
            self.frameCountToMove = self.speed
        if self.movesbeforenewYdirchange>0:
            self.movesbeforenewYdirchange=self.movesbeforenewYdirchange-1
            
        if (self.rect.x+self.xdirection) <5 or (self.rect.x+self.rect.width+self.xdirection) >1019: 
            self.xdirection=-self.xdirection
        if (self.rect.y+self.ydirection) <35 or (self.rect.y+self.rect.height+self.ydirection) >768: 
            self.ydirection=-self.ydirection            
        #self.rect = self.rect.move(xMove,yMove);
        self.rect.move_ip(1*self.xdirection,1*self.ydirection); 
        
    def setBallImageFrame(self,frame):
        self.currentFrame=frame
        self.image = self.images[frame]
        self.hitmask=get_colorkey_hitmask(self.image, self.rect)
 
    def setXDirection(self,direction):
        self.xdirection=direction
        
    def setYDirection(self,direction):
        if self.movesbeforenewYdirchange==0:
            self.ydirection=direction
            self.movesbeforenewYdirchange=15 
        
if __name__ == "__main__":
    MainWindow = Breakout()
    MainWindow.MainLoop()