from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
from random import randrange

ESCAPE = '\033'
window = 0

# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0


class Triangle2D(object):
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3


class Triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []

    def draw(self):
        glBegin(GL_TRIANGLES)

        glColor3f(*self.color)
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs=None):
        if maqs == None or maqs == 0:
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

    def add_voxel(self, voxel):
        self.voxlist += [voxel]

    def draw_voxels(self):
        for voxel in self.voxlist:
            voxel.draw()

    def project(self, axis):
        if type(axis) == int:
            return triangle2D(self.s1[:axis] + self.s1[axis + 1:])
        #TODO: if axis == X, Y, Z



class Voxel(object):
    width = 0.05

    def __init__(self, x, y, z, color=(0, 1, 0)):
        self.coord_x = x
        self.coord_y = y
        self.coord_z = z
        self.color = color

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


def getcoord():
    return randrange(201) - 100
A, B, C = [getcoord(), getcoord(), getcoord()], [getcoord(), getcoord(), getcoord()], [getcoord(), getcoord(), getcoord()]
#A, B, C = [-0.5, -0.4, 0.0], [0.7, -0.5, -0.5], [0.0, 0.8, 0.3]

print(A, B, C)

exa = Triangle3D(A, B, C)
exa.add_voxel(Voxel(*A))
exa.add_voxel(Voxel(*B))
exa.add_voxel(Voxel(*C))

exa.normalize()


def init_gl(width, height):
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width) / float(height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def key_pressed(*args):
    if args[0] == ESCAPE:
        sys.exit()


def draw_gl_scene():
    global X_AXIS, Y_AXIS, Z_AXIS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0, 0.0, -6.0)

    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)

    # Draw Triangle
    exa.draw()

    # Draw voxels at each vertex
    exa.draw_voxels()

    X_AXIS = X_AXIS - 1
#    Z_AXIS = Z_AXIS - 0.30

    glutSwapBuffers()


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(200, 200)

    window = glutCreateWindow('proto')

    glutDisplayFunc(draw_gl_scene)
    glutIdleFunc(draw_gl_scene)
    glutKeyboardFunc(key_pressed)
    init_gl(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main()
