from OpenGL.GL import *


class Voxel(object):
    width = 0.05

    def __init__(self, coord_x, coord_y, coord_z, color=(0, 1, 0)):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.coord_z = coord_z
        self.color = color

    def __repr__(self):
        return f'Voxel(coord:[{self.coord_x}, {self.coord_y}, {self.coord_z}], color:{self.color})'

    def get_coords(self):
        return self.coord_x, self.coord_y, self.coord_z

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
