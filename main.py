import pygame
from pygame.locals import *
from Classes import *
import random
import time
import threading
import serial
import math
from pyvidplayer2 import Video
from Stopwatch import *

#Colors
red = (255 , 0 , 0) # RED
green = (0, 255, 0) # GREEN
blue = (10, 60, 225) # BLUE
white = (255, 255, 255) # WHITE
black = (0, 0, 0) # BLACK
Colors = [red,green,blue,white,black]

Difficulty = 1

def playing():

    #Screen
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.toggle_fullscreen()
    background = pygame.image.load("assets\\background.png")
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

    pygame.mixer.init()
    pygame.mixer.music.load("assets\\Game Music.mp3")
    pygame.mixer.music.play()

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        dt = clock.tick(60) / 1000
        # fill the screen with background to wipe away anything from last frame
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
        
                xSpeed = 100 * math.sin(math.radians(xRot)) * dt
                ySpeed = 100 * math.sin(math.radians(yRot)) * dt

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
    pygame.mixer.quit()

def get_font(size):
    return pygame.font.Font("assets\\Minecrafter.Alt.ttf",size)

def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
    t = pygame.time.get_ticks() / 2 % time
    y = math.sin(t / speed) * how_far + overall_y
    return int(y)

def menu():
    vid = Video("assets\\BackgroundVidGame.mp4")
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Rehabilitation Maze Game")
    pygame.display.toggle_fullscreen()
    MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
    

    surf = pygame.Surface((1280,720), pygame.SRCALPHA, 32)
    surf = surf.convert_alpha()
    Start = Button(pygame.image.load("assets\\Play Rect.png"),(1280/2,280),"Start",get_font(75),"White","Green")
    Start.update(surf)
    Settings = Button(pygame.image.load("assets\\Play Rect.png"),(1280/5,550),"Settings",get_font(65),"White","Green")
    Settings.update(surf)
    Quit = Button(pygame.image.load("assets\\Play Rect.png"),(1280 - 1280/5,550),"Quit",get_font(75),"White","Green")
    Quit.update(surf)
    Music = Button(pygame.image.load("assets\\Music On.png"),(50,50),"",get_font(75),"White","Green")
    Music.update(surf)
    arrows = pygame.image.load("assets\\arrows.png")

    settingsSurf = pygame.Surface((1280,720), pygame.SRCALPHA, 32)
    settingsSurf = settingsSurf.convert_alpha()
    SETTINGS_TEXT = get_font(100).render("DIFFICULTY", True, "#b68f40")
    SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(640, 100))
    Easy = Button(pygame.image.load("assets\\Play Rect.png"),(640,250),"Easy",get_font(75),"White","Green")
    Medium = Button(pygame.image.load("assets\\Play Rect.png"),(640,400),"Medium",get_font(75),"White","Green")
    Extreme = Button(pygame.image.load("assets\\Play Rect.png"),(640,550),"Extreme",get_font(65),"White","Green")
    Easy.update(settingsSurf)
    Medium.update(settingsSurf)
    Extreme.update(settingsSurf)

    sw = Stopwatch()
    sw.start()
    global isMuted
    isMuted = False
    isSettings = False
    while vid.active:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if isSettings == False:
                    if Start.checkForInput(pygame.mouse.get_pos()):
                        try:
                            global serialPort
                            serialPort = serial.Serial(port='COM9', baudrate=9600)
                        except:
                            print("Couldn't connect to HC-05")
                        else:
                            vid.stop()
                            playing()
                    elif Music.checkForInput(pygame.mouse.get_pos()):
                        vid.toggle_mute()
                        if isMuted == False:
                            isMuted = True  
                            Music.changeImage(pygame.image.load("assets\\Music Off.png"))
                            Music.update(surf)
                        else:
                            isMuted = False
                            Music.changeImage(pygame.image.load("assets\\Music On.png"))
                            Music.update(surf)
                    elif Settings.checkForInput(pygame.mouse.get_pos()):
                        isSettings = True
                    elif Quit.checkForInput(pygame.mouse.get_pos()):
                        vid.stop()
                else:
                    if Easy.checkForInput(pygame.mouse.get_pos()):
                        Difficulty = 1
                        isSettings = False
                    elif Medium.checkForInput(pygame.mouse.get_pos()):
                        Difficulty = 2
                        isSettings = False
                    elif Extreme.checkForInput(pygame.mouse.get_pos()):
                        Difficulty = 3
                        isSettings = False
        if key == "f":
            pygame.display.toggle_fullscreen()

        if vid.draw(screen, (0, 0), force_draw=False) and sw.secondsPassed() >= 5:
            #pygame.display.update()
            if sw.secondsPassed() > 7:
                if isSettings == False:
                    screen.blit(surf,(0,0))
                    screen.blit(arrows,(445,330))
                    for button in [Start, Settings, Quit]:
                        button.changeColor(pygame.mouse.get_pos())
                        button.update(screen)
                else:
                    screen.blit(settingsSurf,(0,0))
                    for button in [Easy, Medium, Extreme]:
                        button.changeColor(pygame.mouse.get_pos())
                        button.update(screen)
            if isSettings == False:
                y = sine(200.0,1280,10.0,50)
                screen.blit(MENU_TEXT,(340,y))
            else:
                y = sine(200.0,1280,10.0,50)
                screen.blit(SETTINGS_TEXT,(340,y))
    
        pygame.time.wait(16) # around 60 fps
        # screen.blit(surf,(0,0))
        pygame.display.flip()

    vid.close()
    pygame.quit()

menu()