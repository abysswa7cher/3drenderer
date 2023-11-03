import pygame
import numpy as np
from os.path import isfile
from math import sin, cos

class OBJ:
    def __init__(self, path):
        self.faces = list()
        self.scale = 100

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
            face.render(self.scale)

class Vertex:
    def __init__(self, coords:list):
        self.matrix = np.matrix([float(coords[0]), float(coords[1]), float(coords[2])])

    def __str__(self) -> str:
        return (f"Vertex{self.matrix}")  
    def __repr__(self) -> str:
        return (f"Vertex{self.matrix}")

    def get_projection_matrix(self):
        proj_matrix = [[1, 0, 0],
                       [0, 1, 0]]
        
        return np.dot(proj_matrix, self.matrix.reshape(3,1))
    
    def get_rotation_matrix(self, angle):
        Rx = np.matrix([[1, 0, 0],
                        [0, cos(angle), -sin(angle)],
                        [0, sin(angle), cos(angle)]])
        
        Ry = np.matrix([[cos(angle), 0, sin(angle)],
                        [0, 1, 0],
                        [-sin(angle), 0, cos(angle)]])
        
        Rz = np.matrix([[cos(angle), -sin(angle), 0],
                        [sin(angle), cos(angle), 0],
                        [0, 0, 1]])
        
        rotated2d = np.dot(Rz, self.matrix.reshape(3,1))
        rotated2d = np.dot(Ry, rotated2d)
        rotated2d = np.dot(Rx, rotated2d)

        projected2d = np.dot(Rz, rotated2d)

        self.matrix = projected2d

    def update(self, angle):
        self.get_rotation_matrix(angle)

class Face:
    def __init__(self, vertices : list):
        self.display = pygame.display.get_surface()
        self.vertices = [Vertex(v) for v in vertices]
        self.sides = [(self.vertices[i], self.vertices[i+1]) if i < (len(self.vertices)-1) else (self.vertices[i], self.vertices[0]) for i in range(len(self.vertices))]
        self.center_x = self.display.get_size()[0] // 2
        self.center_y = self.display.get_size()[1] // 2
    
    def update(self, angle):
        for v in self.vertices:
            v.update(angle)
    
    def side_verts_to_coords(self, side, scale):
        x1 = self.center_x - side[0].matrix[0, 0] * scale
        y1 = self.center_y - side[0].matrix[1, 0] * scale

        x2 = self.center_x - side[1].matrix[0, 0] * scale
        y2 = self.center_y - side[1].matrix[1, 0] * scale

        return ((x1, y1), (x2, y2))

    def render(self, scale):
        for side in self.sides:
            pygame.draw.line(self.display, "gold", *self.side_verts_to_coords(side, scale), 1)

    def __str__(self) -> str:
        v = tuple([v for v in self.vertices])
        return (f"Quad{v}")
    def __repr__(self) -> str:
        v = tuple([v for v in self.vertices])
        return (f"Quad{v}")