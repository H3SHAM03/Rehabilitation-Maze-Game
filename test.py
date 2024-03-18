# Example file showing a circle moving on screen
import pygame
from pyvidplayer2 import Video
from Classes import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
# vid = Video("Images\\BackgroundVid.mp4")
# vid.set_size(1280,720)

def intro():
    while True:
        global running
        # vid.draw(screen,(0,0))
        # pygame.display.update()
        # running = True
        game()


def game():
    running = True
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        pygame.sprite.Sprite()
        pygame.draw.circle(screen,"red",player_pos,40)
        image = pygame.image.load('assets\\Play Rect.png')
        Start = Button(image,(1280/2,720/2),"Start",pygame.font.Font("assets\\Minecrafter.Alt.ttf",75),"White","Green")
        surf = pygame.surface.Surface((1280,720))
        Start.update(screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= 100 * dt
        if keys[pygame.K_s]:
            player_pos.y += 100 * dt
        if keys[pygame.K_a]:
            player_pos.x -= 100 * dt
        if keys[pygame.K_d]:
            player_pos.x += 100 * dt

        if player_pos.x > 1240:
            player_pos.x = 1240
        elif player_pos.x < 40:
            player_pos.x = 40
        if player_pos.y > 680:
            player_pos.y = 680
        elif player_pos.y < 40:
            player_pos.y = 40

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()

running = True
intro()