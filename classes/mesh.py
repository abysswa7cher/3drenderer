from random import choice
from operator import itemgetter

COLORS = None
with open("colors.txt") as file:
    COLORS = [line.strip() for line in file.readlines()]

class Mesh:
    def __init__(self, v:dict=dict(), vn:dict=dict(), f:list=list(), color:str=str()):
        self.v = v
        self.vn = vn
        self.f = f
        self.e = list()
        if color in COLORS:
            self.color = color
        else:
            self.color = choice(COLORS)

        self.check_validity()
        self.generate_sides()

        self.v = dict(sorted(self.v.items(), key=lambda x: x[1][2]))

    def generate_sides(self):
        pairs_q = [(0, 1), (1, 2), (2, 3), (3, 0)]
        pairs_t = [(0, 1), (1, 2), (2, 0)]

        for face in self.f:
            face = face[0]
            if len(face) == 4:
                self.e.append([(face[p[0]], face[p[1]]) for p in pairs_q])
            elif len(face) == 3:
                self.e.append([(face[p[0]], face[p[1]]) for p in pairs_t])
            else:
                raise ValueError(f"Face {face} is not a triangle nor a quad (Vertex count < 3 or > 4).")
    
    def check_validity(self):
        for face in self.f:
            if face[1] not in self.vn.keys():
                raise ValueError("Vertex {} not found in {}".format(face[1], self.vn))
            for vertex in face[0]:
                if vertex not in self.v.keys():
                    raise ValueError("Vertex {} not found in {}".format(vertex, self.v))

    def __str__(self):
        return f"\n------\nMesh(\n    Color: {self.color}\n    Vertices: {self.v}\n    Faces: {self.f}    \nNormals: {self.vn}\n    Edges: {self.e})"

    def __repr__(self):
        return f"\n------\nMesh(\n    Color: {self.color}\n    Vertices: {self.v}\n    Faces: {self.f}    \nNormals: {self.vn}\n    Edges: {self.e})"
    