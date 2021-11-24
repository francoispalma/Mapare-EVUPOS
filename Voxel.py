from OpenGL.GL import *


class Voxel(object):
    width = 0.05

    def __init__(self, x, y, z, color=(0, 1, 0)):
        self.coord_x = x
        self.coord_y = y
        self.coord_z = z
        self.color = color

    def __repr__(self):
        return f'voxel(coord:[{self.coord_x}, {self.coord_y}, {self.coord_z}], color:{self.color})'

    def get_coords(self):
        return self.coord_x, self.coord_y, self.coord_z

    def get_faces(self):
        # TODO: do it smartly with gray's code.
        w = Voxel.width
        x, y, z = self.coord_x, self.coord_y, self.coord_z
        faces = []

        faces += [[[x + w, y + w, z + w],
                   [x + w, y + w, z - w],
                   [x + w, y - w, z - w],
                   [x + w, y - w, z + w]]]

        faces += [[[x + w, y + w, z + w],
                   [x + w, y - w, z + w],
                   [x - w, y - w, z + w],
                   [x - w, y + w, z + w]]]

        faces += [[[x + w, y + w, z + w],
                   [x + w, y + w, z - w],
                   [x - w, y + w, z - w],
                   [x - w, y + w, z + w]]]

        faces += [[[x - w, y + w, z + w],
                   [x - w, y + w, z - w],
                   [x - w, y - w, z - w],
                   [x - w, y - w, z + w]]]

        faces += [[[x + w, y - w, z + w],
                   [x + w, y - w, z - w],
                   [x - w, y - w, z - w],
                   [x - w, y - w, z + w]]]

        faces += [[[x + w, y + w, z - w],
                   [x + w, y - w, z - w],
                   [x - w, y - w, z - w],
                   [x - w, y + w, z - w]]]

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
