from time import time
from classes.obj3 import OBJ
import cProfile, dis
from pyinstrument import Profiler
from math import sin, cos
import pygame
from pygame.locals import *
import sys
from debug import debug


pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
obj = OBJ("sword.obj")

start = time()
dtime = start - time()


class Program:
    def __init__(self):
        self.action = False
        self.last_mouse_pos = pygame.mouse.get_pos()
        self.translation = False
        self.rotation = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_q]:
                        if self.rotation: 
                            self.rotation = False
                        if self.translation:
                            self.translation = False
                        else:
                            self.translation = True
                    if keys[pygame.K_r]:
                        if self.translation:
                            self.translation = False
                        if self.rotation:
                            self.rotation = False
                        else:
                            self.rotation = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                        keys = pygame.mouse.get_pressed()
                        if keys[0] and not self.action:
                            self.action = True

                if event.type == pygame.MOUSEBUTTONUP:
                    keys = pygame.mouse.get_pressed()
                    if not keys[0] and self.action:
                        self.action = False

                if event.type == pygame.MOUSEWHEEL:
                    if event.y < 0:
                        obj.scale += 0.5
                    if event.y > 0:
                        obj.scale -= 0.5
            
            
            screen.fill("black")

            obj.update(0.001, pygame.mouse.get_pos(), self.action, [self.translation, self.rotation])
            obj.render()
            # obj.faces[0].update((time()-start)*0.01)
            # obj.faces[0].render()
            debug(f"action: {self.action}, translation: {self.translation}, rotation: {self.rotation} FPS:{clock.get_fps()}")

            pygame.display.update()
            clock.tick()

            # if time() - start > 10:
            #     end = time()
            #     print(f"runtime: {end-start}")
            #     break

        # pygame.quit()
        # sys.exit()


if __name__ == "__main__":
    # with Profiler(interval=0.1) as pr:
    Program().run()
    # pr.open_in_browser()
    # cProfile.run('Program().run()', sort="tottime")

    # Program().run()
    # print(*obj.faces[0].get_rotation_matrix(obj.faces[0].sides[0][0], 1))
    # print(obj.faces[0].update(1))
    # print(obj.faces[0].sides)
    pass