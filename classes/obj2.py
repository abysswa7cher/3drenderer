import pygame
from math import sin, cos, radians
from numpy import cross, dot
from utils.math import vnorm, vextend, vadd
from classes.mesh import Mesh
from operator import sub

class OBJ:
    def __init__(self, path):
        self.meshes = list()
        self.axis = {"x": [[0,0,0], [1,0,0], "red"],
                     "y": [[0,0,0], [0,1,0], "green"],
                     "z": [[0,0,0], [0,0,1], "blue"]}

        with open(path) as file:
            self.read_obj(file)

    def read_obj(self, file):
        text = file.read()
        data = [line.split() for line in text.split("\n")[2:] if line != ""]
        vertices = dict()
        normals = dict()

        i = 1
        j = 1
        for line in data:
            if line[0] == "v":
                v = [float(c) for c in line[1:]]
                vertices.update({i:v})
                i += 1
            if line[0] == "vn":
                vn = [float(c) for c in line[1:]]
                normals.update({j:vn})
                j += 1

        for mesh_text in [block.split("\n") for block in text.split("o ")][1:]:
            
            mesh_faces = list()
            mesh_vertices = dict()
            mesh_normals = dict()

            for line in [line.split() for line in mesh_text]:
                if len(line) > 0:
                    if line[0] == "f":
                        normal_index = int(line[1:][0].split("/")[2])
                        verts = [int(v.split("/")[0]) for v in line[1:]]
                        mesh_faces.append([verts, normal_index])

                        for v in verts:
                            mesh_vertices.update({v:vertices[v]})

                        if normal_index not in mesh_normals:
                            mesh_normals.update({normal_index:normals[normal_index]})

            self.meshes.append(Mesh(mesh_vertices, mesh_normals, mesh_faces, mesh_text[0]))

    def __rotate_z(self, v_dict, v_key, angle):
        c = cos(angle)
        s = sin(angle)
        
        x, y, z = v_dict[v_key]
        
        rotated_z = [(c*x) + (-s*y), (s*x) + (c*y), z]
        
        v_dict.update({v_key:rotated_z})

    def __rotate_x(self, v_dict, v_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = v_dict[v_key]

        rotated_x = [x, (c*y)+(-s*z), (s*y) + (c*z)]

        v_dict.update({v_key:rotated_x})

    def __rotate_y(self, v_dict, v_key, angle):
        c = cos(angle)
        s = sin(angle)

        x, y, z = v_dict[v_key]

        rotated_y = [(c*x) + (s*z), y, (-s*x) + (c*z)]

        v_dict.update({v_key:rotated_y})

    def __self_rotate_x(self, angle):
        for i, mesh in enumerate(self.meshes):
            for v in mesh.v:
                self.__rotate_x(self.meshes[i].v, v, angle)
            for vn in mesh.vn:
                self.__rotate_x(self.meshes[i].vn, vn, angle)

    def __self_rotate_y(self, angle):
        for i, mesh in enumerate(self.meshes):
            for v in mesh.v:
                self.__rotate_y(self.meshes[i].v, v, angle)
            for vn in mesh.vn:
                self.__rotate_y(self.meshes[i].vn, vn, angle)
    
    def __self_rotate_z(self, angle):
        for i, mesh in enumerate(self.meshes):
            for v in mesh.v:
                self.__rotate_z(self.meshes[i].v, v, angle)
            for vn in mesh.vn:
                self.__rotate_z(self.meshes[i].vn, vn, angle)

    def update(self, action, angle, mode, axis):
        if action:
            angle = radians(angle)
            # mode represents activated
            # translation (mode[0]) or rotation (mode[1])
            if mode[1]:
                # rotation along x 
                # when user presses LMB
                if axis[0] and action[0]:
                    self.__self_rotate_x(angle)

                # reverse rotation along x 
                # when user presses LMB
                if axis[0] and action[1]:
                    self.__self_rotate_x(-angle)
                
                # rotation along y 
                # when user presses LMB
                if axis[1] and action[0]:
                    self.__self_rotate_y(angle)
                
                # reverse rotation along y
                # when user presses LMB
                if axis[1] and action[1]:
                    self.__self_rotate_y(-angle)
                
                # rotation along z 
                # when user presses LMB
                if axis[2] and action[0]:
                    self.__self_rotate_z(angle)
                
                # reverse rotation along z 
                # when user presses LMB
                if axis[2] and action[1]:
                    self.__self_rotate_z(-angle)

    def draw_edges(self, display:pygame.display, mesh:Mesh, screen_center:tuple, scale:float):
        for edges in mesh.e:
            for edge in edges:
                self.draw_edge(display, mesh, edge, screen_center, scale)

    def draw_edge(self, display:pygame.display, mesh:Mesh, edge:tuple, screen_center:tuple, scale:float):
        v1 = (screen_center[0] - mesh.v[edge[0]][0] * scale,
              screen_center[1] - mesh.v[edge[0]][1] * scale)
        v2 = (screen_center[0] - mesh.v[edge[1]][0] * scale,
              screen_center[1] - mesh.v[edge[1]][1] * scale)
            
        pygame.draw.line(display, "gold", v1, v2, 1)

    def draw_wireframe(self, display:pygame.display, screen_center:tuple, scale:float, normals:bool):
        for mesh in self.meshes:
            for face in mesh.f:
                self.draw_edges(display, mesh, screen_center, scale)
                
                if normals:
                    self.draw_normal(display, mesh, face, screen_center, scale)

    def draw_face(self, display:pygame.display, mesh:Mesh, face:list, screen_center:tuple, scale:float, normals:bool, edge_mode:bool):
        face_normal = self.get_face_normal(mesh, face)
        
        if dot([0, 0, -1], face_normal) < 0:
            face_center = self.get_face_center(mesh, face)
            face_normal = vadd(face_center, vextend(face_normal, 0.25))

            face_center = [(screen_center[0] - mesh.v[i][0] * scale,
                            screen_center[1] - mesh.v[i][1] * scale) for i in face[0]]
            
            face_normal = (screen_center[0] - face_normal[0] * scale, 
                           screen_center[1] - face_normal[1] * scale)
                
            pygame.draw.polygon(display, mesh.color, face_center)

            if edge_mode:
                for edge in mesh.e:
                    for p in edge:
                        for vertex in face[0]:
                            if vertex in p:
                                self.draw_edge(display, mesh, p, screen_center, scale)
            if normals:   
                self.draw_normal(display, mesh, face, screen_center, scale)

    def draw_mesh(self, display:pygame.display, screen_center:tuple, scale:float, normals:bool, edge_mode:bool):
        for mesh in self.meshes:
            for face in mesh.f:
                self.draw_face(display, mesh, face, screen_center, scale, normals, edge_mode)

    def render(self, display:pygame.display, wireframe:bool, edge_mode:bool, normals:bool, scale:float):
            screen_center = (display.get_width() // 2, display.get_height() // 2)
            
            if wireframe:
                self.draw_wireframe(display, screen_center, scale, normals)
            else:
                self.draw_mesh(display, screen_center, scale, normals, edge_mode)

    def draw_normal(self, display, mesh, face, screen_center, scale):
            face_center = self.get_face_center(mesh, face)
            face_normal = vextend(self.get_face_normal(mesh, face), 0.25)
            face_normal = vadd(face_center, face_normal)

            if face_normal is not None:

                face_center = (screen_center[0] - face_center[0] * scale,
                               screen_center[1] - face_center[1] * scale)
                
                face_normal = (screen_center[0] - face_normal[0] * scale, 
                               screen_center[1] - face_normal[1] * scale)
                
                pygame.draw.line(display, "blue", face_center, face_normal)
                pygame.draw.circle(display, "green", (face_center), 3)

    def get_face_normal(self, mesh, face):
        return mesh.vn[face[1]]

    def get_face_center(self, mesh, face):
        points = [mesh.v[i] for i in face[0]]

        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        center_c = (sum(x) / len(points), sum(y) / len(points), sum(z) / len(points))

        return center_c