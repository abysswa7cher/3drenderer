from time import time
from classes.obj import OBJ
import cProfile
from math import sin, cos
import pygame
from pygame.locals import *
import sys
from debug import debug


pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
obj = OBJ("torus.obj")

start = time()
dtime = start - time()

def run():
    action = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
                keys = pygame.mouse.get_pressed()
                if keys[0] and not action:
                    action = True
                else: 
                    action = False
                # if event.type == pygame.MOUSEBUTTONUP:
                #     keys = pygame.mouse.get_pressed()
                #     if not keys[0] and action:
                #         action = False
        
        if time() - start > 10:
            end = time()
            print(f"runtime: {end-start}")
            pygame.quit()
            sys.exit()
        
        screen.fill("black")
        obj.update((time()-start)*0.01)
        obj.render()
        debug((action, clock.get_fps()))

        pygame.display.update()
        clock.tick()

if __name__ == "__main__":
    cProfile.run('run()', sort="tottime")