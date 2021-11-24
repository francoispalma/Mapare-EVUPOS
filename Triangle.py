from OpenGL.GL import *
import numpy as np


class Triangle2D(object):
    def __init__(self, s1, s2, s3, color=(0, 0, 1)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color

    def get_color(self):
        return self.color

    def get_vertices(self):
        return [self.s1, self.s2, self.s3]

    def __repr__(self):
        return f'Triangle2D(s1:{self.s1}, s2:{self.s2}, s3:{self.s3})'


class Triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []
        self._projection = None

    def __repr__(self):
        return f'Triangle3D(s1:{self.s1}, s2:{self.s2}, s3:{self.s3}, color:{self.color}, voxlist:{self.voxlist})'

    def draw(self):
        glBegin(GL_TRIANGLES)

        glColor3f(*self.color)
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs=None):
        if maqs is None or maqs == 0:
            maqs = 0
            for coord in self.s1 + self.s2 + self.s3:
                if abs(coord) > maqs:
                    maqs = abs(coord)

        if maqs == 0:
            raise ValueError

        self.s1 = (np.array(self.s1) / maqs).tolist()
        self.s2 = (np.array(self.s2) / maqs).tolist()
        self.s3 = (np.array(self.s3) / maqs).tolist()
        for voxel in self.voxlist:
            voxel.normalize(maqs)

    def find_dominant_axis(self):
        a = (np.array(self.s2) - np.array(self.s1)).tolist()
        b = (np.array(self.s3) - np.array(self.s1)).tolist()
        normal_vector = [a[1] * b[2] - a[2] * b[1],
                         a[2] * b[0] - a[0] * b[2],
                         a[0] * b[1] - a[1] * b[0]]
        i = 0
        val = normal_vector[0]
        for j in range(1, 3):
            if normal_vector[j] > val:
                i = j
                val = normal_vector[j]

        return i

    def add_voxel(self, voxel):
        self.voxlist += [voxel]

    def draw_voxels(self):
        for voxel in self.voxlist:
            voxel.draw()

    def project(self, axis):
        if type(axis) == int:
            triangle = Triangle2D(self.s1[:axis] + self.s1[axis + 1:],
                                  self.s2[:axis] + self.s2[axis + 1:],
                                  self.s3[:axis] + self.s3[axis + 1:])
        # TODO: if axis == X, Y, Z
        self._projection = triangle
        return triangle

    def draw_projection(self):
        if self._projection is None:
            pass
        else:
            glBegin(GL_TRIANGLES)

            glColor3f(*self._projection.get_color())
            for sommet in self._projection.get_vertices():
                glVertex3f(*sommet, 0)

            glEnd()
