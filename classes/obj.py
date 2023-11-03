import pygame
from math import sin, cos, radians
from numpy import cross
from utils.math import norm, extend
from operator import sub

class OBJ:
    def __init__(self, path):
        self.vertices = dict()
        self.normals = dict()
        self.faces = list()
        self.sides = list()

        with open(path) as file:
            self.read_obj(path, file)

        self.generate_sides()

    def read_obj(self, path, file):
        data = file.readlines()

        i = 1
        j = 1
        for line in data:
            line = line.strip().split()
            self.name = path.split("/")[-1].split(".")[-2]
            if "v" in line[0]:
                self.vertices.update({i: [float(v) for v in line[1:]]})
                i += 1
            if "vn" in line[0]:
                self.normals.update({j:[float(v) for v in line[1:]]})
                j += 1
            if "f" in line[0]:
                normal_index = int(line[1:][0].split("//")[1])
                verts = [int(v.split("//")[0]) for v in line[1:]]

                self.faces.append([verts, normal_index])

    def generate_sides(self):
        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for face in self.faces:
            face = face[0]
            if len(face) == 4:
                for p in pairs_q:
                    self.sides.append((face[p[0]], face[p[1]]))
            if len(face) == 3:
                for p in pairs_t:
                    self.sides.append((face[p[0]], face[p[1]]))

    def translate(self):
        pass

    def __rotate_z__(self, v_dict, vector_key, angle):
        c = cos(angle)
        s = sin(angle)
        
        x, y, z = v_dict[vector_key]
        
        rotated_z = [(c*x) + (-s*y), (s*x) + (c*y), z]
        
        v_dict.update({vector_key:rotated_z})

    def __rotate_x__(self, v_dict, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = v_dict[vector_key]

        rotated_x = [x, (c*y)+(-s*z), (s*y) + (c*z)]

        v_dict.update({vector_key:rotated_x})

    def __rotate_y__(self, v_dict, vector_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = v_dict[vector_key]

        rotated_y = [(c*x) + (s*z), y, (-s*x) + (c*z)]

        v_dict.update({vector_key:rotated_y})

    def __self_rotate_x__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_x__(self.vertices, k, angle)
        for k in self.normals.keys():
            self.__rotate_x__(self.normals, k, angle)
    
    def __self_rotate_y__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_y__(self.vertices, k, angle)
        for k in self.normals.keys():
            self.__rotate_y__(self.normals, k, angle)
    
    def __self_rotate_z__(self, angle):
        for k in self.vertices.keys():
            self.__rotate_z__(self.vertices, k, angle)
        for k in self.normals.keys():
            self.__rotate_z__(self.normals, k, angle)

    def update(self, action, angle, mode, axis):
        if action:
            angle = radians(angle)
            # mode represents activated
            # translation (mode[0]) or rotation (mode[1])
            if mode[1]:
                # rotation along x 
                # when user presses LMB
                if axis[0] and action[0]:
                    self.__self_rotate_x__(angle)

                # reverse rotation along x 
                # when user presses LMB
                if axis[0] and action[1]:
                    self.__self_rotate_x__(-angle)
                
                # rotation along y 
                # when user presses LMB
                if axis[1] and action[0]:
                    self.__self_rotate_y__(angle)
                
                # reverse rotation along y
                # when user presses LMB
                if axis[1] and action[1]:
                    self.__self_rotate_y__(-angle)
                
                # rotation along z 
                # when user presses LMB
                if axis[2] and action[0]:
                    self.__self_rotate_z__(angle)
                
                # reverse rotation along z 
                # when user presses LMB
                if axis[2] and action[1]:
                    self.__self_rotate_z__(-angle)

    def draw_edges(self, display:pygame.display, center:tuple, scale:float):
        for i in self.sides:
            # print(i)
            v1 = (center[0] - self.vertices[i[0]][0] * scale,
                  center[1] - self.vertices[i[0]][1] * scale)
            v2 = (center[0] - self.vertices[i[1]][0] * scale,
                  center[1] - self.vertices[i[1]][1] * scale)

            print(v1, v2)
            pygame.draw.line(display, "gold", v1, v2, 1)

    def draw_faces(self, display:pygame.display, center:tuple, scale:float):
        for face in self.faces:
            final_coords = [(center[0] - self.vertices[i][0] * scale, 
                             center[1] - self.vertices[i][1] * scale) for i in face[0]]
            
            pygame.draw.polygon(display, "white", final_coords)

    def render(self, display:pygame.display, wireframe:bool, normals:bool, scale:float):
            screen_center = (display.get_width() // 2, display.get_height() // 2)
            
            if wireframe:
                self.draw_edges(display, screen_center, scale)
                if normals:
                    self.draw_normals(display, screen_center, scale)
            else:
                self.draw_faces(display, screen_center, scale)
                if normals:
                    self.draw_normals(display, screen_center, scale)

    def draw_normals(self, display, screen_center, scale):
        for face in self.faces:
            face_center = self.get_face_center(face)
            face_center = (screen_center[0] - face_center[0] * scale, 
                           screen_center[1] - face_center[1] * scale)
            
            face_normal = extend(self.get_face_normal(face), 1.25)
            face_normal = (screen_center[0] - face_normal[0] * scale, 
                           screen_center[1] - face_normal[1] * scale)
            
            pygame.draw.line(display, "blue", face_center, face_normal)
            pygame.draw.circle(display, "red", (face_normal), 2)
            pygame.draw.circle(display, "green", (face_center), 3)

    # def get_face_normal(self, face):
    #     p1 = self.vertices[face[0]]
    #     p2 = self.vertices[face[1]]
    #     p3 = self.vertices[face[-2]]

    #     v1 = list(map(sub, p2, p1))
    #     v2 = list(map(sub, p3, p1))

    #     return cross(v1, v2)
    def get_face_normal(self, face):
        return self.normals[face[1]]

    def get_face_center(self, face):
        points = [self.vertices[i] for i in face[0]]

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        center_c = (sum(x) / len(points), sum(y) / len(points), sum(z) / len(points))

        return center_c
