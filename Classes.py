import pygame
from pygame.locals import *
from threading import Thread

class Ball(pygame.sprite.Sprite):
    def __init__(self,x=45,y=45):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('assets\\Ball.png')
        self.image = pygame.transform.scale(temp,(100,100))
        self.rect = pygame.Rect(x-45, y-45, 45*2, 45*2)
        self.rect.center = (x,y)
        self.size = (45,45)

    def BallUpdate(self,x,y):
        self.rect.center = (x,y)

    def Resize(self,x,y):
        self.image = pygame.transform.scale(self.image,(x,y))

class Hole(pygame.sprite.Sprite):
    def __init__(self,x=50,y=50):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('assets\\Hole.png')
        self.image = pygame.transform.scale(temp,(120,120))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.size = (50,50)

class Barrier(pygame.sprite.Sprite):
    def __init__(self,x=0,y=0,isHorizontal=True):
        pygame.sprite.Sprite.__init__(self)
        temp = pygame.image.load('assets\\Barrier.png')
        self.image = pygame.transform.scale(temp,(1000,24))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = x
        self.y = y
        self.isHorizontal = isHorizontal

    def Rotate(self):
        self.image = pygame.transform.rotate(self.image,90)
        self.rect =self.image.get_rect()
        self.rect.center = (self.x,self.y)
        if self.isHorizontal == True:
            self.isHorizontal = False
        else:
            self.isHorizontal = True

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.isChosen = False

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            self.isChosen = True
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            self.isChosen = False
            
    def changeImage(self, image):
        self.image = image
            
class CustomThread(Thread):
    def __init__(self, Value=None, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self.returnValue = Value
        self.isRunning = False
 
    def run(self):
        self.isRunning = True
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
        self.isRunning = False
        self.returnValue = self._return