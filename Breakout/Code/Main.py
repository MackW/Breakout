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
    sprBallGroup=pygame.sprite.Group()
    sprBatGroup=pygame.sprite.Group()
    sprallgroup = pygame.sprite.Group()
    
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
        #clock=pygame.time.Clock()
        self.LoadSprites()
        self.play_music()
        self.DrawFrame()
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
            if self.sprBall.checkCollision(self.sprBall, self.sprBat) == True:
                self.sprBall.ydirection = self.sprBall.ydirection * -1
                self.sprBall.frameCountToMove =0
            if self.sprBall.rect.y>740:
                font = pygame.font.Font(None, 72)                                                                                        
                text = font.render("Game Over", 1, (0, 255, 0))                               
                textpos = text.get_rect(centerx=self.width/2,centery=278)
                self.screen.blit(text, textpos)   
                exitloop=True
            if pygame.mixer.music.get_busy()==False:
                self.play_music()
            pygame.display.flip()

    def DrawFrame(self):
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(0,0), (1023,0)], 5)
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(0,0), (0,767)], 5)
        pygame.draw.lines(self.screen, (255, 255, 255), False, [(1023,0), (1023,767)], 5)                
    def LoadSprites(self):
        """Load the sprites that we need"""
        self.sprBat = Bat()
        self.sprBat.rect.centerx=512
        self.sprBat.rect.y=700
        self.sprBat.groups = self.sprBatGroup,self.sprallgroup
        self.sprBall = Ball()
        #self.sprBall.rect.centerx=512
        #self.sprBall.rect.y =683
        self.sprBall.rect.centerx=450
        self.sprBall.rect.y =600
        self.sprBall.setYDirection(1)
        self.sprBall.groups=self.sprBallGroup,self.sprallgroup
        
    def play_music(self):
        filename = os.path.join("Sounds/tune.mid")
       # pygame.mixer.music.load(filename)
        #pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.5)
        
 
class Bat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.images=[]
        self.images.append(load_image('Bat1.png',-1))
        self.images.append(load_image('Bat1.png',-1))
        self.images.append(load_image('Bat1.png',-1))
        self.image = self.images[0]
        self.rect=self.image.get_rect()
        self.direction=0
        self.currentFrame=0
    def move(self):
        self.image = self.images[self.currentFrame]
        if (self.rect.x+self.direction) >5 and (self.rect.x+self.rect.width+self.direction) <1024: 
            self.rect.move_ip(self.direction*2,0); 
        
    def setDirection(self,direction):
        self.direction=direction
    def setBatImageFrame(self,frame):
        self.currentFrame=frame  
           
class Ball(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.images=[]
        self.images.append(load_image('Ball.png',-1))
        self.image = self.images[0]
        self.rect=self.image.get_rect()
        self.frameCountToMove=1
        self.xdirection=1
        self.ydirection=-1
        self.speed=1
        
    def move(self):
        if self.frameCountToMove>0:
            self.frameCountToMove=self.frameCountToMove-1
            return
        else:
            self.frameCountToMove = self.speed

        if (self.rect.x+self.xdirection) <5 or (self.rect.x+self.rect.width+self.xdirection) >1019: 
            self.xdirection=-self.xdirection
        if (self.rect.y+self.ydirection) <5 or (self.rect.y+self.rect.height+self.ydirection) >768: 
            self.ydirection=-self.ydirection            
        #self.rect = self.rect.move(xMove,yMove);
        self.rect.move_ip(1*self.xdirection,1*self.ydirection); 
        
    def setBallImageFrame(self,frame):
        self.currentFrame=frame
 
    def setXDirection(self,direction):
        self.xdirection=direction
        
    def setYDirection(self,direction):
        self.ydirection=direction
        
    def checkCollision(self,sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        return col    
        
if __name__ == "__main__":
    MainWindow = Breakout()
    MainWindow.MainLoop()