import pygame
from math import sin, cos, radians
from numpy import cross, dot
from utils.math import vnorm, vextend, vadd
from operator import sub

class OBJ:
    def __init__(self, path):
        self.name = path.split("/")[-1].split(".")[-2]
        self.vertices = dict()
        self.normals = dict()
        self.faces = list()

        with open(path) as file:
            self.read_obj(file)

        self.generate_sides()

    def read_obj(self, file):
        data = file.readlines()

        i = 1
        j = 1
        for line in data:
            line = line.strip().split()
            if "v" in line[0]:
                self.vertices.update({i: [float(v) for v in line[1:]]})
                i += 1
            if "vn" in line[0]:
                self.normals.update({j:[float(v) for v in line[1:]]})
                j += 1
            if "f" in line[0]:
                if "//" in line:
                    normal_index = int(line[1:][0].split("//")[1])
                    verts = [int(v.split("//")[0]) for v in line[1:]]
                else:
                    normal_index = int(line[1:][0].split("/")[2])
                    verts = [int(v.split("/")[0]) for v in line[1:]]
                self.faces.append([verts, normal_index])
                

    def generate_sides(self):
        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for i, face in enumerate(self.faces):
            face = face[0]
            if len(face) == 4:
                self.faces[i].append([(face[p[0]], face[p[1]]) for p in pairs_q])
            elif len(face) == 3:
                self.faces[i].append([(face[p[0]], face[p[1]]) for p in pairs_t])
            else:
                raise ValueError(f"Face {face} is not a triangle nor a quad (Vertex count < 3 or > 4).")
        
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

    def draw_edges(self, display:pygame.display, face:list, screen_center:tuple, scale:float):
            edges = face[2]
            for edge in edges:
                v1 = (screen_center[0] - self.vertices[edge[0]][0] * scale,
                      screen_center[1] - self.vertices[edge[0]][1] * scale)
                v2 = (screen_center[0] - self.vertices[edge[1]][0] * scale,
                      screen_center[1] - self.vertices[edge[1]][1] * scale)
                
                pygame.draw.line(display, "gold", v1, v2, 1)

    def draw_wireframe(self, display:pygame.display, screen_center:tuple, scale:float, normals:bool):
        for face in self.faces:
            self.draw_edges(display, face, screen_center, scale)
            
            if normals:
                self.draw_normal(display, face, screen_center, scale)

    def draw_face(self, display:pygame.display, face:list, screen_center:tuple, scale:float, normals:bool, edge_mode:bool):
        face_center = self.get_face_center(face)
        face_normal = vadd(face_center, vextend(self.get_face_normal(face), 0.25))
        face_normal = (screen_center[0] - face_normal[0] * scale, 
                       screen_center[1] - face_normal[1] * scale,
                       screen_center[1] - face_normal[2] * scale)
        
        if dot([-1, 0, 0], face_normal) < 0:
            final_coords = [(screen_center[0] - self.vertices[i][0] * scale,
                             screen_center[1] - self.vertices[i][1] * scale) for i in face[0]]
            
            pygame.draw.polygon(display, "white", final_coords)

            if edge_mode: 
                self.draw_edges(display, face, screen_center, scale)
            if normals:   
                self.draw_normal(display, face, screen_center, scale)

    def draw_mesh(self, display:pygame.display, screen_center:tuple, scale:float, normals:bool, edge_mode:bool):
        for face in self.faces:
            self.draw_face(display, face, screen_center, scale, normals, edge_mode)

    def render(self, display:pygame.display, wireframe:bool, edge_mode:bool, normals:bool, scale:float):
            screen_center = (display.get_width() // 2, display.get_height() // 2)
            
            if wireframe:
                self.draw_wireframe(display, screen_center, scale, normals)
            else:
                self.draw_mesh(display, screen_center, scale, normals, edge_mode)

    def draw_normal(self, display, face, screen_center, scale):
            face_center = self.get_face_center(face)
            face_normal = vextend(self.get_face_normal(face), 0.25)
            face_normal = vadd(face_center, face_normal)

            face_center = (screen_center[0] - face_center[0] * scale,
                           screen_center[1] - face_center[1] * scale)
            
            face_normal = (screen_center[0] - face_normal[0] * scale, 
                           screen_center[1] - face_normal[1] * scale)
            
            pygame.draw.line(display, "blue", face_center, face_normal)
            pygame.draw.circle(display, "green", (face_center), 3)

    def get_face_normal(self, face):
        return self.normals[face[1]]

    def get_face_center(self, face):
        points = [self.vertices[i] for i in face[0]]

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        center_c = (sum(x) / len(points), sum(y) / len(points), sum(z) / len(points))

        return center_c