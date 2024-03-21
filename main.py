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


isLoaded = False

def playing(Difficulty):

	global P1,H1,Balls,Holes
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

	if Difficulty == 2:
		B1 = Barrier(1280/4,90)
		B1.Rotate()
		Barriers = pygame.sprite.Group()
		Barriers.add(B1)
		B2 = Barrier(1000,630)
		B2.Rotate()
		Barriers.add(B2)
	elif Difficulty == 3:
		B1 = Barrier(500,130)
		B2 = Barrier(1280-500,300)
		B3 = Barrier(500,450)
		B4 = Barrier(1280-500,600)
		Barriers = pygame.sprite.Group()
		Barriers.add(B1)
		Barriers.add(B2)
		Barriers.add(B3)
		Barriers.add(B4)

	def HolePosition():
		global H1
		global Holes
		H1 = Hole(random.randint(50,1230),random.randint(50,670))
		Holes = pygame.sprite.Group()
		Holes.add(H1)
		if Difficulty == 2:
			while pygame.sprite.spritecollide(H1,Barriers,False) or (H1.rect.centerx < 1000 and H1.rect.centerx > 320):
				H1.kill()
				H1 = Hole(random.randint(50,1230),random.randint(50,670))
				Holes = pygame.sprite.Group()
				Holes.add(H1)
		elif Difficulty == 3:
			while pygame.sprite.spritecollide(H1,Barriers,False) or (H1.rect.centery < 420 and H1.rect.centery >220):
				H1.kill()
				H1 = Hole(random.randint(50,1230),random.randint(50,670))
				Holes = pygame.sprite.Group()
				Holes.add(H1)

	HolePosition()

	layers = pygame.sprite.LayeredUpdates()
	if Difficulty != 1:
		layers.add(B1)
		layers.add(B2)
	if Difficulty == 3:
		layers.add(B3)
		layers.add(B4)
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
		if bool(Balls) == True:
			P1.kill()
		H1.kill()
		HolePosition()
		player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
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
			elif event.type == pygame.KEYDOWN:
				key = pygame.key.name(event.key)
				if key == "m":
					isKilling = True
					running = False
					threading.Thread(target=Killing).start()
					serialPort.close()
					menu()
				if key == "f":
					pygame.display.toggle_fullscreen()

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
		
				xSpeed = 300 * math.sin(math.radians(xRot)) * dt
				ySpeed = 300 * math.sin(math.radians(yRot)) * dt

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
				running = False
				threading.Thread(target=Killing).start()
				serialPort.close()
				menu()
			
			if Difficulty != 1:
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

def gradientTransparency(time: int,r=0,g=0,b=0):
	t = pygame.time.get_ticks() / 2 % time

def BLEConnection() -> bool:
	global serialPort
	try:
		serialPort = serial.Serial(port='COM9', baudrate=9600)
	except:
		return False
	else:
		return True
	
def BLEDisconnect():
	serialPort.close()

def menu():
	def Reading():
		while isConnected == True and isLoaded == False:
			data = serialPort.readline(1024)
			data = str(data.decode('ascii'))
			data = data.replace('\r\n','')
			if data:
				# print(data)
				if data != '':
					data = data.split('/')
					ReadThread.returnValue = data
				else:
					return None

	vid = Video("assets\\BackgroundVidGame.mp4")
	screen = pygame.display.set_mode((1280,720))
	pygame.display.set_caption("Rehabilitation Maze Game")
	pygame.display.toggle_fullscreen()
	MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
	LEADERBOARDS_TEXT = get_font(65).render("LEADERBOARDS COMING SOON",True,(255,255,255))
	pygame.mixer.init()
	pygame.mixer.music.load("assets\\click sound.mp3")

	surf = pygame.Surface((1280,720), pygame.SRCALPHA, 32)
	surf = surf.convert_alpha()
	Start = Button(pygame.image.load("assets\\menu button.png"),(1280/2,280),"Start",get_font(45),"White","Green")
	Start.update(surf)
	Settings = Button(pygame.image.load("assets\\menu button.png"),(1280/5,550),"Settings",get_font(45),"White","Green")
	Settings.update(surf)
	Quit = Button(pygame.image.load("assets\\menu button.png"),(1280 - 1280/5,550),"Quit",get_font(45),"White","Green")
	Quit.update(surf)
	Music = Button(pygame.image.load("assets\\Music On.png"),(50,50),"",get_font(45),"White","Green")
	Music.update(surf)
	BLE = Button(pygame.image.load("assets\\Bluetooth Off.png"),(1230,50),"",get_font(45),"White","Green")
	BLE.update(surf)
	arrows = pygame.image.load("assets\\arrows.png")

	settingsSurf = pygame.Surface((1280,720), pygame.SRCALPHA,32)
	settingsSurf = settingsSurf.convert_alpha()
	SETTINGS_TEXT = get_font(100).render("DIFFICULTY", True, "#b68f40")
	SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(640, 100))
	Easy = Button(pygame.image.load("assets\\menu button.png"),(640,250),"EAsy",get_font(45),"White","Green")
	Medium = Button(pygame.image.load("assets\\menu button.png"),(640,400),"Medium",get_font(45),"White","Green")
	Extreme = Button(pygame.image.load("assets\\menu button.png"),(640,550),"Extreme",get_font(45),"White","Green")
	Easy.update(settingsSurf)
	Medium.update(settingsSurf)
	Extreme.update(settingsSurf)

	loadingSurf = pygame.Surface((1280,720),masks="2e2f30")
	loadingSurf.set_alpha(200)
	LOADING_TEXT = get_font(100).render("LOADING",True,(255,255,255))

	sw = Stopwatch()
	ResetingSW = Stopwatch()
	DelaySW = Stopwatch()
	ResetingSW.start()
	sw.start()
	global isMuted
	isMuted = False
	isSettings = False
	isLoading = False
	isLoaded = False
	isConnected = False
	isPlaying = False
	isTouched = 0
	Difficulty = 1
	LoadThread = CustomThread(target=BLEConnection)
	ReadThread = CustomThread(target=Reading)
	while vid.active:
		key = None
		if isTouched == 1:
			WIRELESS = USEREVENT+1
			my_event = pygame.event.Event(WIRELESS,message = "test")
			pygame.event.post(my_event)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				serialPort.close()
				isConnected = False
				vid.stop()
			elif event.type == pygame.KEYDOWN:
				key = pygame.key.name(event.key)
			if event.type == pygame.MOUSEBUTTONDOWN or isConnected == True:
				if sw.secondsPassed() >= 7 and isLoading == False:
					if isSettings == False:
						if Start.checkForInput(pygame.mouse.get_pos()) or (Start.isChosen == True and isTouched == 1):
							if DelaySW.EndTime == 0:
								pygame.mixer.music.play()
								isLoading = True
								isPlaying = True
								isTouched = 0
								if isConnected == False:
									LoadThread.start()
								else:
									LoadThread.returnValue = True
							elif DelaySW.secondsPassed() >= 1 or isConnected == False:
								pygame.mixer.music.play()
								isLoading = True
								isPlaying = True
								isTouched = 0
								if isConnected == False:
									LoadThread.start()
								else:
									LoadThread.returnValue = True
								DelaySW.start()
							# try:
							#     global serialPort
							#     pygame.mixer.music.play()
							#     serialPort = serial.Serial(port='COM9', baudrate=9600)
							# except:
							#     print("Couldn't connect to HC-05")
							# else:
							#     vid.stop()
							#     playing()
						elif Music.checkForInput(pygame.mouse.get_pos()):
							vid.toggle_mute()
							pygame.mixer.music.play()
							if isMuted == False:
								isMuted = True  
								Music.changeImage(pygame.image.load("assets\\Music Off.png"))
								Music.update(surf)
							else:
								isMuted = False
								Music.changeImage(pygame.image.load("assets\\Music On.png"))
								Music.update(surf)
						elif BLE.checkForInput(pygame.mouse.get_pos()):
							pygame.mixer.music.play()
							if isConnected == False:
								isLoading = True
								isPlaying = False
								LoadThread.start()
							if isConnected == True:
								serialPort.close()
								isConnected = False
								isLoading = True
								LoadThread.returnValue = False
								isPlaying = False							
						elif Settings.checkForInput(pygame.mouse.get_pos()) or (Settings.isChosen == True and isTouched == 1):
							if DelaySW.EndTime != 0 and DelaySW.secondsPassed() >= 1 or isConnected == False:
								isSettings = True
								isTouched = 0
								pygame.mixer.music.play()
								DelaySW.start()
							elif DelaySW.EndTime == 0:
								DelaySW.start()
								isSettings = True
								isTouched = 0
								pygame.mixer.music.play()
						elif Quit.checkForInput(pygame.mouse.get_pos()) or (Quit.isChosen == True and isTouched == 1):
							if DelaySW.EndTime == 0:
								pygame.mixer.music.play()
								isTouched = 0
								if isConnected == True:
									serialPort.close()
								isConnected = False
								vid.stop()
							elif DelaySW.secondsPassed() >= 1 or isConnected == False:
								pygame.mixer.music.play()
								isTouched = 0
								if isConnected == True:
									serialPort.close()
								isConnected = False
								vid.stop()
								DelaySW.start()
					else:
						if Easy.checkForInput(pygame.mouse.get_pos()) or (Easy.isChosen == True and isTouched == 1):
							if DelaySW.secondsPassed() >= 1 or isConnected == False:
								pygame.mixer.music.play()
								isTouched = 0
								Difficulty = 1
								isSettings = False
								DelaySW.start()
						elif Medium.checkForInput(pygame.mouse.get_pos()) or (Medium.isChosen == True and isTouched == 1):
							if DelaySW.secondsPassed() >= 1 or isConnected == False:
								pygame.mixer.music.play()
								isTouched = 0
								Difficulty = 2
								isSettings = False
								DelaySW.start()
						elif Extreme.checkForInput(pygame.mouse.get_pos()) or (Extreme.isChosen == True and isTouched == 1):
							if DelaySW.secondsPassed() >= 1 or isConnected == False:	
								pygame.mixer.music.play()
								isTouched = 0
								Difficulty = 3
								isSettings = False
								DelaySW.start()
		if key == "f":
			pygame.display.toggle_fullscreen()
		if LoadThread.is_alive() == False and isLoading == True and isPlaying == False:
			if LoadThread.returnValue == True:
				LoadThread = CustomThread(target=BLEConnection)
				isConnected = True
				isLoading = False
				BLE.changeImage(pygame.image.load("assets\\Bluetooth On.png"))
				BLE.update(surf)
			elif LoadThread.returnValue == False:
				LoadThread = CustomThread(target=BLEConnection)
				isConnected = False
				isLoading = False
				BLE.changeImage(pygame.image.load("assets\\Bluetooth Off.png"))
				BLE.update(surf)
				ReadThread = CustomThread(target=Reading)
		elif LoadThread.is_alive() == False and isLoading == True and isPlaying == True:
			if LoadThread.returnValue == True:
				vid.stop()
				LoadThread = CustomThread(target=BLEConnection)
				isLoaded = True
				isPlaying = False
				isLoading = False
				playing(Difficulty)
			elif LoadThread.returnValue == False:
				isPlaying = False
				isLoading = False
				LoadThread = CustomThread(target=BLEConnection)
				

		if vid.draw(screen, (0, 0), force_draw=False) and sw.secondsPassed() >= 5:
			if ResetingSW.secondsPassed() >= 89:
				vid.restart()
				ResetingSW.start()
				# another stopwatch
			#pygame.display.update()
			if isSettings == False:
				y = sine(200.0,1280,10.0,50)
				screen.blit(MENU_TEXT,(340,y))
			else:
				y = sine(200.0,1280,10.0,50)
				screen.blit(SETTINGS_TEXT,(340,y))

			if sw.secondsPassed() >= 7:
				if isSettings == False:
					screen.blit(surf,(0,0))
					screen.blit(arrows,(445,330))
					t = sine(200.0,1280,127,127)
					LEADERBOARDS_TEXT.set_alpha(t)
					screen.blit(LEADERBOARDS_TEXT,(110,635))
					for button in [Start, Settings, Quit]:
						if isConnected == True:
							mousePos = (0,0)
							xRot = yRot = 0
							if ReadThread.is_alive() == False:
								ReadThread.start()
							if ReadThread.returnValue is not None:
								xRot = float(ReadThread.returnValue[0])
								yRot = float(ReadThread.returnValue[1])
								isTouched = int(ReadThread.returnValue[2])
							if yRot > 30 and yRot <= 180:
								mousePos = (Start.x_pos,Start.y_pos)
							elif xRot > 30 and xRot < 180:
								mousePos = (Quit.x_pos,Quit.y_pos)
							elif xRot > 180 and xRot < 320:
								mousePos = (Settings.x_pos,Settings.y_pos)
							button.changeColor(mousePos)
							button.update(surf)
						else:
							button.changeColor(pygame.mouse.get_pos())
							button.update(surf)
				else:
					screen.blit(settingsSurf,(0,0))
					for button in [Easy, Medium, Extreme]:
						if isConnected == True:
							mousePos = (0,0)
							xRot = yRot = 0
							if ReadThread.is_alive() == False:
								ReadThread.start()
							if ReadThread.returnValue is not None:
								yRot = float(ReadThread.returnValue[1])
								isTouched = int(ReadThread.returnValue[2])
								if yRot > 30 and yRot <= 180:
									mousePos = (Easy.x_pos,Easy.y_pos)
								elif yRot > 320 or yRot <= 30:
									mousePos = (Medium.x_pos,Medium.y_pos)
								elif yRot > 180 and yRot <= 320:
									mousePos = (Extreme.x_pos,Extreme.y_pos)
								button.changeColor(mousePos)
								button.update(settingsSurf)
						else:
							button.changeColor(pygame.mouse.get_pos())
							button.update(settingsSurf)
				if isLoading == True:
					t = sine(200.0,1280,127,127)
					y = sine(200.0,1280,10.0,330)
					screen.blit(surf,(0,0))
					screen.blit(arrows,(445,330))
					screen.blit(loadingSurf,(0,0))
					LOADING_TEXT.set_alpha(t)
					screen.blit(LOADING_TEXT,(400,y))
	
		pygame.time.wait(16) # around 60 fps
		pygame.display.flip()

	vid.close()
	pygame.quit()

menu()