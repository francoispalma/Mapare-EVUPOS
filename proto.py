from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np


ESCAPE = '\033'
window = 0


#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0


class triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color

    def draw(self):
        glBegin(GL_TRIANGLES)

        glColor3f(*self.color)
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

        glEnd()


class voxel(object):
    width = 0.05

    def __init__(self, x, y, z, color=(0, 1, 0)):
        self.coord_x = x
        self.coord_y = y
        self.coord_z = z
        self.color = color
        # Do normalization later
        

    def get_coords(self):
        return (self.coord_x, self.coord_y, self.coord_z)

    def get_faces(self):
        # TODO: do it smartly with gray's code.
        w = voxel.width
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


A, B, C = [-0.5, -0.4, 0.0], [0.7, -0.5, -0.5], [0.0, 0.8, 0.3]

exa = triangle3D(A, B, C)
vox1 = voxel(*A)
vox2 = voxel(*B)
vox3 = voxel(*C)

def InitGL(Width, Height): 
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def keyPressed(*args):
    if args[0] == ESCAPE:
        sys.exit()


def DrawGLScene():
    global X_AXIS,Y_AXIS,Z_AXIS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    glTranslatef(0.0,0.0,-6.0)

    glRotatef(X_AXIS,1.0,0.0,0.0)
    glRotatef(Y_AXIS,0.0,1.0,0.0)
    glRotatef(Z_AXIS,0.0,0.0,1.0)

    # Draw Triangle
    exa.draw()
    vox1.draw()
    vox2.draw()
    vox3.draw()
    
    # Draw voxels at each vertex
    

    X_AXIS = X_AXIS - 0.30
#    Z_AXIS = Z_AXIS - 0.30

    glutSwapBuffers()


def main():
    global window

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(200,200)

    window = glutCreateWindow('proto')

    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()


if __name__ == "__main__":
    main() 
