import pygame
import numpy as np
from os.path import isfile
from math import sin, cos

class OBJ:
    def __init__(self, path):
        self.faces = list()

        if isfile(path):
            with open(path) as file:
                data = file.readlines()
                vertices = list()

                for line in data:
                    if "o" in line[0]:
                        self.name = line.strip().split()[1]
                    if "v" in line[0]:
                        vertices.append(line[1:].strip().split())
                    if "f" in line[0]:
                        line = line[1:].strip().split()
                        self.faces.append(Face([vertices[int(v)-1] for v in line]))
        else:
            raise ValueError(f"File {path} not found.")
        
    def update(self, angle):
        for face in self.faces:
            face.update(angle)

    def render(self):
        for face in self.faces:
            face.render()

class Face:
    def __init__(self, vertices : list):
        self.display = pygame.display.get_surface()
        vertices = [[float(v[0]), float(v[1]), float(v[2])] for v in vertices]
        self.sides = [np.array([vertices[i], vertices[i+1]]) if i < (len(vertices)-1) 
                      else
                      np.array([vertices[i], vertices[0]]) for i in range(len(vertices))]
        
        self.screen_center = (self.display.get_size()[0] // 2, self.display.get_size()[1] // 2)

    def update(self, angle):
        for i, s in enumerate(self.sides):
            # print(f"before:\n{self.sides[i]}\n")
            self.sides[i][0] = self.get_rotation_matrix(s[0], angle).reshape(1,3)
            self.sides[i][1] = self.get_rotation_matrix(s[1], angle).reshape(1,3)
            # print(f"after:\n{self.sides[i]}\n\n\n")
    
    def side_verts_to_coords(self, side, scale):
        p1 = side.tolist()[0][:2]
        p2 = side.tolist()[1][:2]
        p1 = (self.screen_center[0] - p1[0] * scale, self.screen_center[1] - p1[1] * scale)
        p2 = (self.screen_center[0] - p2[0] * scale, self.screen_center[1] - p2[1] * scale)

        return p1, p2

    def translation_matrix(self, dx=0, dy=0, dz=0):
        return np.array([1,  0,  0,  0],
                        [0,  1,  0,  0],
                        [0,  0,  1,  0],
                        [dx, dy, dz, 1])
    
    def scale_matrix(s, cx=0, cy=0, cz=0):
        return np.array([[s,0,0,0],
                         [0,s,0,0],
                         [0,0,s,0],
                         [cx*(1-s), cy*(1-s), cz*(1-s), 1]])

    def get_rotate_x_matrix(self, angle):
        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([[1, 0,  0, 0],
                         [0, c, -s, 0],
                         [0, s,  c, 0],
                         [0, 0,  0, 1]])
    
    def get_rotate_y_matrix(self, angle):
        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([[ c, 0, s, 0],
                         [ 0, 1, 0, 0],
                         [-s, 0, c, 0],
                         [ 0, 0, 0, 1]])
    
    def get_rotate_z_matrix(self, angle):
        c = np.cos(angle)
        s = np.sin(angle)

        return np.array([[c, -s, 0, 0],
                         [s,  c, 0, 0],
                         [0,  0, 1, 0],
                         [0,  0, 0, 1]])

    def get_rotation_matrix(self, vertex, angle, rotation_axis="x"):
        if "x" in rotation_axis:
            rotation_matrix = self.get_rotate_x_matrix(angle)
            vertex = np.dot(rotation_matrix, vertex)

        return vertex
    
    def render(self):
        for side in self.sides:
            # print(*self.side_verts_to_coords(side, 100))
            print(self.get_rotation_matrix(side[0], 1))
            # pygame.draw.line(self.display, "gold", *self.side_verts_to_coords(side, 100), 1)#
            pass

    def __str__(self) -> str:
        v = tuple([v for v in self.vertices])
        return (f"Quad{v}")
    def __repr__(self) -> str:
        v = tuple([v for v in self.vertices])
        return (f"Quad{v}")