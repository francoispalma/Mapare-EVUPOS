from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
import numpy as np

class triangle3D(object):
    s1 = [0, 0, 0]
    s2 = [0, 0, 0]
    s3 = [0, 0, 0]
    
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
    
    def projection(self, axis):  # returns 2D triangle
        pass


class triangle2D(object):
    s1 = [0, 0]
    s2 = [0, 0]
    s3 = [0, 0]
    
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3


class voxel(object):
    coord_x = 0
    coord_y = 0
    coord_z = 0
    width = 0
    
    def __init__(self, x, y, z, width):
        self.coord_x = x
        self.coord_y = y
        self.coord_z = z
        self.width = width


if __name__ == "__name__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

    glutCreateWindow('proto')
    glutReshapeWindow(512, 512)

    glutMainLoop()
