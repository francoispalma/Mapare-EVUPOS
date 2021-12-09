# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

from OpenGL.GL import *


class Voxel:
    """Voxel class that represents a single voxel.
    """

    # Voxel width, for rendering purposes.
    width = 1

    def __init__(self, coord_x, coord_y, coord_z, color=(0, 1, 0)):
        """coord_x, coord_y, coord_z: respectively the x y and z coordinate for
        the voxel in question.
        color: for rendering purposes, gives a colour to the cube being drawn.
        """
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.coord_z = coord_z
        self.color = color

    def __repr__(self):
        return f'Voxel(coord:[{self.coord_x}, {self.coord_y}, {self.coord_z}], color:{self.color})'

    def get_coords(self):
        """Returns the x, y and z coordinate in list form.
        """
        return [self.coord_x, self.coord_y, self.coord_z]

    def __getitem__(self, item):
        """Returns a specific coordinate, meant to be used as if the voxel is a
        list.
        """
        return self.get_coords()[item]

    def __hash__(self):
        """Hash function. Not needed after reflection but done so we keep it.
        """
        return hash(tuple(self.get_coords()))

    def __eq__(self, other):
        """Equals function. Used for collision detection. Some sacrifices are
        made for speed. We assume the "other" being given is always a voxel and
        we don't check explicitly.
        """
        return self.coord_x == other.coord_x and self.coord_y == other.coord_y\
               and self.coord_z == other.coord_z

    def get_faces(self):
        """Function to get the faces of the cube for the voxel render.
        We calculate the faces again each frame to not have to keep everything
        in memory.
        """
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
        """Function to draw the voxel cube.
        """
        glBegin(GL_QUADS)

        for face in self.get_faces():
            glColor3f(*self.color)
            for sommet in face:
                glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs):
        """Function to normalize from integer coordinates to -1.0 to 1.0 floats.
        It is expected that a voxel is part of the cover of a triangle and so
        the parent triangle will be the one calling this so maqs will be given
        by the triangle.
        """
        self.coord_x /= maqs
        self.coord_y /= maqs
        self.coord_z /= maqs


class Voxelmatrix:
    """Class to handle the collision matrix of the triangle's cover.
    """

    def __init__(self, s1, s2, s3):
        """s1, s2, s3: The three vertices of the parent triangle.
        """
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
        """Returns true if the voxel is already in the voxelization, false
        otherwise.
        """
        return self.m[Vox[0] - self._minx][Vox[1] - self._miny][Vox[2] - self._minz] >= 1

    def __repr__(self):
        """Quick and dirty for some testing.
        """
        return self.m.__repr__()

    def __getitem__(self, item):
        """Returns the number of the time that the voxel has been hit in the
        matrix.
        """
        return self.m[item[0] - self._minx][item[1] - self._miny][item[2] - self._minz]

    def hit(self, x, y, z):
        """Hits the correct spot in the matrix to signify that voxel exists in
        the current voxelization.
        """
        self.m[x - self._minx][y - self._miny][z - self._minz] += 1
