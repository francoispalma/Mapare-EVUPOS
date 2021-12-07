# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

from OpenGL.GL import *


class Voxel(object):
    width = 1

    def __init__(self, coord_x, coord_y, coord_z, color=(0, 1, 0)):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.coord_z = coord_z
        self.color = color

    def __repr__(self):
        return f'Voxel(coord:[{self.coord_x}, {self.coord_y}, {self.coord_z}], color:{self.color})'

    def get_coords(self):
        return [self.coord_x, self.coord_y, self.coord_z]

    def __getitem__(self, item):
        return self.get_coords()[item]

    def __hash__(self):
        return hash(tuple(self.get_coords()))

    def __eq__(self, other):
        return self.coord_x == other.coord_x and self.coord_y == other.coord_y and self.coord_z == other.coord_z

    def copy(self):
        return self.get_coords().copy()

    def get_faces(self):
        # TODO: do it smartly with gray's code.
        faces = []

        faces += [[[self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width]]]

        faces += [[[self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width]]]

        faces += [[[self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width]]]

        faces += [[[self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width]]]

        faces += [[[self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z + Voxel.width]]]

        faces += [[[self.coord_x + Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x + Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y - Voxel.width, self.coord_z - Voxel.width],
                   [self.coord_x - Voxel.width, self.coord_y + Voxel.width, self.coord_z - Voxel.width]]]

        return faces

    def draw(self):
        glBegin(GL_QUADS)

        faces = self.get_faces()

        for face in faces:
            glColor3f(*self.color)
            for sommet in face:
                glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs):
        # temporary
        self.coord_x /= maqs
        self.coord_y /= maqs
        self.coord_z /= maqs


class Voxelmatrix(object):
    def __init__(self, s1, s2, s3):
        self._minx = min(s1[0], s2[0], s3[0])
        self._miny = min(s1[1], s2[1], s3[1])
        self._minz = min(s1[2], s2[2], s3[2])
        X = max(s1[0], s2[0], s3[0]) - min(s1[0], s2[0], s3[0]) + 1
        Y = max(s1[1], s2[1], s3[1]) - min(s1[1], s2[1], s3[1]) + 1
        Z = max(s1[2], s2[2], s3[2]) - min(s1[2], s2[2], s3[2]) + 1
        self._s1 = s1
        self._s2 = s2
        self._s3 = s3
        self._X = X
        self._Y = Y
        self._Z = Z
        self.m = [[[0] * Z for i in range(Y)] for j in range(X)]

    def __contains__(self, Vox):
        return self.m[Vox[0] - self._minx][Vox[1] - self._miny][Vox[2] - self._minz] >= 1

    def __repr__(self):
        return self.m.__repr__()

    def __getitem__(self, item):
        return self.m[item[0] - self._minx][item[1] - self._miny][item[2] - self._minz]

    def hit(self, x, y, z):
        self.m[x - self._minx][y - self._miny][z - self._minz] += 1
