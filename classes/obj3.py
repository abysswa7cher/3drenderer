import pygame
import numpy as np
import os
from os.path import isfile
from math import sin, cos

DIR = os.getcwd()

class OBJ:
    def __init__(self, path):
        self.vertices = dict()
        self.faces = list()
        self.sides = list()

        with open(path) as file:
            data = file.readlines()
            i = 1
            j = 0

            for line in data:
                line = line.strip().split()
                self.name = path.split("/")[-1].split(".")[-2]
                if "v" in line[0]:
                    self.vertices.update({i: [float(v) for v in line[1:]]})
                    i += 1
                if "f" in line[0]:
                    self.faces.append([int(v) for i,v in enumerate(line[1:])])
                    j += 1

        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for face in self.faces:
            if len(face) == 4:
                for p in pairs_q:
                    self.sides.append((face[p[0]], face[p[1]]))
            if len(face) == 3:
                for p in pairs_t:
                    self.sides.append((face[p[0]], face[p[1]]))
    
    def translate(self, vector_key, dxdydz):
        self.vertices[vector_key] = np.add(self.vertices[vector_key], np.matrix([[c] for c in dxdydz]))

    def __rotate_z__(self, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        
        vector = self.vertices[vector_key]
        x, y, z = vector[0], vector[1], vector[2]
        # print(vector)
        
        rotated_z = [(c*x) + (-s*y), (s*x) + (c*y), z]
        rotated = np.dot(vector, rotated_z)
        
        self.vertices.update({vector_key:rotated})

    def __self_rotate_z__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_z__(k, angle)

    def update(self, angle, dxdydz):
        self.__self_rotate_z__(angle)

    def render(self, scale):
        # display = pygame.display.get_surface()
        # center = (display.get_width() // 2, display.get_height() // 2)
        
        for i in self.sides:
            print(self.vertices[i[0]])
        #     v1 = (center[0] - self.vertices[i[0]][0] * scale, 
        #           center[1] - self.vertices[i[0]][1] * scale)
        #     v2 = (center[0] - self.vertices[i[1]][0] * scale, 
        #           center[1] - self.vertices[i[1]][1] * scale)

        #     pygame.draw.line(display, "gold", v1, v2, 1)

# obj = OBJ("cube.obj")
# # obj.update(10, ())
# obj.render(1)