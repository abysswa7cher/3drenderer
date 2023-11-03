import pygame
from math import sin, cos, sqrt, radians
from numpy import dot

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

            pygame.draw.line(display, "gold", v1, v2, 1)

    def draw_faces(self, display:pygame.display, center:tuple, scale:float):
        for face in self.faces:
            final_coords = [(center[0] - self.vertices[i][0] * scale, 
                             center[1] - self.vertices[i][1] * scale) for i in face]
            
            pygame.draw.polygon(display, "white", final_coords)

    def render(self, display:pygame.display, wireframe:bool, scale:float):
            screen_center = (display.get_width() // 2, display.get_height() // 2)
            
            if wireframe:
                self.draw_normals(display, screen_center, scale)
                self.draw_edges(display, screen_center, scale)
            else:
                self.draw_normals(display, screen_center, scale)
                self.draw_faces(display, screen_center, scale)

    def draw_normals(self, display, screen_center, scale):
        faces = self.faces
        faces.reverse()

        for face in faces:
            face_center = self.get_face_center(face)
            face_center = (screen_center[0] - face_center[0] * scale, 
                           screen_center[1] - face_center[1] * scale)
            
            face_normal = self.get_face_normal(face)
            face_normal = (screen_center[0] - face_normal[0] * scale, 
                           screen_center[1] - face_normal[1] * scale, face_normal[2])
            
            face_normal = self.vnorm(face_normal)[0:2]
            face_normal = (screen_center[0] - face_normal[0] * scale, 
                           screen_center[1] - face_normal[1] * scale)
            
            # pygame.draw.line(display, "green", (face_center[0], face_center[1]), face_normal)
            pygame.draw.circle(display, "green", (face_normal), 2)
            pygame.draw.circle(display, "red", (face_center), 3)


    def get_face_normal(self, face):
        p1, p2, p3 = self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[-1]]

        v1 = p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2]
        v2 = p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2]


        x =  (v1[1] * v2[2]) - (v1[2] - v2[2])
        y = -((v2[2] * v1[0]) - (v2[0] * v1[2]))
        z =  (v1[0] * v2[1]) - (v1[2] * v2[0])

        return [x, y, z]
    
    def get_face_center(self, face):
        points = [self.vertices[i] for i in face]

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        center_c = (sum(x) / len(points), sum(y) / len(points), sum(z) / len(points))

        return center_c

    def vnorm(self, vector):
        mag = sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
        if mag == 0:
            return vector
        else:
            unit_vector = [vector[0] / mag,
                        vector[1] / mag,
                        vector[2] / mag]
        
            return unit_vector
    
# obj = OBJ("cube.obj")
# obj.get_face_center()