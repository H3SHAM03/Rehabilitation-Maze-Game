import pygame
from pygame.locals import *

class Ball(pygame.sprite.Sprite):
    def __init__(self,x=45,y=45):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('Images\\Ball.png')
        self.image = pygame.transform.scale(temp,(100,100))
        self.rect = pygame.Rect(x-45, y-45, 45*2, 45*2)
        self.rect.center = (x,y)
        self.size = (55,45)

    def BallUpdate(self,x,y):
        self.rect.center = (x,y)

    def Resize(self,x,y):
        self.image = pygame.transform.scale(self.image,(x,y))

class Hole(pygame.sprite.Sprite):
    def __init__(self,x=50,y=50):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('Images\\Hole.png')
        self.image = pygame.transform.scale(temp,(120,120))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.size = (50,50)

class Barrier(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('Images\\Barrier.png')
        self.image = temp
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y

    def Rotate(self):
        self.image = pygame.transform.rotate(self.image,90)
        self.rect =self.image.get_rect()
        self.rect.center = (self.x,self.y)