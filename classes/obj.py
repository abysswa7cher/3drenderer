import pygame
from math import sin, cos

class OBJ:
    def __init__(self, path):
        self.vertices = dict()
        self.faces = list()
        self.sides = list()

        with open(path) as file:
            self.read_obj(path, file)

        self.generate_sides()

    def read_obj(self, path, file):
        data = file.readlines()

        i = 1
        for line in data:
            line = line.strip().split()
            self.name = path.split("/")[-1].split(".")[-2]
            if "v" in line[0]:
                self.vertices.update({i: [float(v) for v in line[1:]]})
                i += 1
            if "f" in line[0]:
                self.faces.append([int(v) for v in line[1:]])

    def generate_sides(self):
        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for face in self.faces:
            if len(face) == 4:
                for p in pairs_q:
                    self.sides.append((face[p[0]], face[p[1]]))
            if len(face) == 3:
                for p in pairs_t:
                    self.sides.append((face[p[0]], face[p[1]]))

    def translate(self):
        pass

    def __rotate_z__(self, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        
        x, y, z = self.vertices[vector_key]
        
        rotated_z = [(c*x) + (-s*y), (s*x) + (c*y), z]
        
        self.vertices.update({vector_key:rotated_z})

    def __rotate_x__(self, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = self.vertices[vector_key]

        rotated_x = [x, (c*y)+(-s*z), (s*y) + (c*z)]

        self.vertices.update({vector_key:rotated_x})

    def __rotate_y__(self, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = self.vertices[vector_key]

        rotated_y = [(c*x) + (s*z), y, (-s*x) + (c*z)]

        self.vertices.update({vector_key:rotated_y})

    def __self_rotate_x__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_x__(k, angle)
    
    def __self_rotate_y__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_y__(k, angle)
    
    def __self_rotate_z__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_z__(k, angle)

    def update(self, action, angle, mode, axis):
        if action:
            if mode[1]:
                if axis[0]:
                    self.__self_rotate_x__(angle)
                if axis[1]:
                    self.__self_rotate_y__(angle)
                if axis[2]:
                    self.__self_rotate_z__(angle)

    def draw_edges(self, display:pygame.display, center:tuple, scale:float):
        for i in self.sides:
            # print(i)
            v1 = (center[0] - self.vertices[i[0]][0] * scale,
                  center[1] - self.vertices[i[0]][1] * scale)
            v2 = (center[0] - self.vertices[i[1]][0] * scale,
                  center[1] - self.vertices[i[1]][1] * scale)

            pygame.draw.line(display, "gold", v1, v2, 1)

    def draw_faces(self, display:pygame.display, center:tuple, scale:float):
        for face in self.faces:
            final_coords = [(center[0] - self.vertices[i][0] * scale, 
                             center[1] - self.vertices[i][1] * scale) for i in face]
            
            pygame.draw.polygon(display, "white", final_coords)

    def render(self, display:pygame.display, wireframe:bool, scale:float):
            center = (display.get_width() // 2, display.get_height() // 2)
            
            if wireframe:
                self.draw_edges(display, center, scale)
            else:
                self.draw_faces(display, center, scale)
