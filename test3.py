# import math
# import pygame

# def sine(speed: float, time: int, how_far: float, overall_y: int) -> int:
#     t = pygame.time.get_ticks() / 2 % time
#     y = math.sin(t / speed) * how_far + overall_y
#     return int(y)

# while True:
#     pygame.time.wait(100)
#     print(sine(200.0,1280,127,127))

from time import sleep
from threading import Thread
 
# custom thread
class CustomThread(Thread):
    # constructor
    def __init__(self):
        # execute the base constructor
        Thread.__init__(self)
        # set a default value
        self.value = None
 
    # function executed in a new thread
    def run(self):
        # store data in an instance variable
        self.value = x()
 

def x():
    return 3

# create a new thread
thread = CustomThread()
# start the thread
thread.start()
# wait for the thread to finish
thread.join()
# get the value returned from the thread
data = thread.value
print(data)