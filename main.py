import pygame
from pygame.locals import *
from Classes import *
import random
import time
import threading
import serial
import math

#Colors
red = (255 , 0 , 0) # RED
green = (0, 255, 0) # GREEN
blue = (10, 60, 225) # BLUE
white = (255, 255, 255) # WHITE
black = (0, 0, 0) # BLACK
Colors = [red,green,blue,white,black]

#Serial
serialPort = serial.Serial(port='COM9', baudrate=9600, timeout=0, parity=serial.PARITY_EVEN, stopbits=1)

#Screen
pygame.init()
screen = pygame.display.set_mode((1280, 720))
background = pygame.image.load("Images\\background.png")
clock = pygame.time.Clock()
running = True
xSpeed = 0
ySpeed = 0
isTouched = 0
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

P1 = Ball(player_pos.x,player_pos.y)
Balls = pygame.sprite.Group()
Balls.add(P1)

B1 = Barrier(1280/4,720/4)
B1.Rotate()
Barriers = pygame.sprite.Group()
Barriers.add(B1)
B2 = Barrier(1000,540)
B2.Rotate()
Barriers.add(B2)

def HolePosition():
    global H1
    global Holes
    H1 = Hole(random.randint(50,1230),random.randint(50,670))
    Holes = pygame.sprite.Group()
    Holes.add(H1)
    while pygame.sprite.spritecollide(H1,Barriers,False):
        H1.kill()
        H1 = Hole(random.randint(50,1230),random.randint(50,670))
        Holes = pygame.sprite.Group()
        Holes.add(H1)

HolePosition()

layers = pygame.sprite.LayeredUpdates()
layers.add(B1)
layers.add(B2)
layers.add(H1)
layers.add(P1)
isKilling = False

def Killing():
    global isKilling
    # for i in range(100):
    #     P1.Resize(100-i,100-i)
    #     time.sleep(0.01)
    P1.kill()
    isKilling = False

def Reset():
    global player_pos,P1,xSpeed,ySpeed
    H1.kill()
    HolePosition()
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    if bool(Balls) == True:
        P1.kill()
    P1 = Ball(player_pos.x,player_pos.y)
    Balls.add(P1)
    xSpeed = ySpeed = 0
    layers.add(H1)
    layers.add(P1)

    

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    dt = clock.tick(120) / 1000
    # fill the screen with a color to wipe away anything from last frame
    screen.blit(background,(0,0))

    Balls.update()
    Holes.update()
    layers.draw(screen)

    data = serialPort.readline(1024)
    data = str(data.decode('ascii'))
    data = data.replace('\r\n','')

    if data:
        print(data)
        if data != '':
            data = data.split('/')
            xRot = float(data[0])
            yRot = float(data[1])
            isTouched = int(data[2])

            if xRot>180:
                xRot = xRot - 360
            if yRot>180:
                yRot = yRot - 360
    
            xSpeed += 9.8 * math.sin(math.radians(xRot))
            ySpeed += 9.8 * math.sin(math.radians(yRot))

            print((xSpeed,ySpeed))
    
    if isTouched == 1:
        Reset()
        time.sleep(0.5)

    if isKilling == False:
        player_pos.y += ySpeed * dt
        player_pos.x += xSpeed * dt

        if player_pos.x > 1280 - P1.size[0]:
            player_pos.x = 1280 - P1.size[0]
            xSpeed = 0
        elif player_pos.x < P1.size[0]:
            player_pos.x = P1.size[0]
            xSpeed = 0
        if player_pos.y > 720 - P1.size[1]:
            player_pos.y = 720 - P1.size[1]
            ySpeed = 0
        elif player_pos.y < P1.size[1]:
            player_pos.y = P1.size[1]
            ySpeed = 0

        P1.BallUpdate(player_pos.x,player_pos.y)

        if player_pos.x > H1.rect.center[0]-10 and player_pos.x < H1.rect.center[0]+10 and player_pos.y > H1.rect.center[1]-10 and player_pos.y < H1.rect.center[1]+10:
            isKilling = True
            threading.Thread(target=Killing).start()

        if pygame.sprite.spritecollide(P1,Barriers,False):
            player_pos = pygame.Vector2(1280/2,720/2)
            xSpeed = ySpeed = 0


    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.

pygame.quit()