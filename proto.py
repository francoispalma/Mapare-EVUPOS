# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

from random import randrange
import sys
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from triangle import Triangle3D


# window position
WINPOSX = 200
WINPOSY = 200


# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
CONST_ROT = 8.0
AUTO_ROT = 1

# zoom
FOVY = 45.0
WINRATIO = 0


# translation
XCOORD = 0.0
YCOORD = 0.0
ZCOORD = -6.0

def get_coord():
    return randrange(201) - 100

method = Triangle3D.voxelize_triangle
nbtriangles = 1000

# Command line arguments
if len(sys.argv) > 1:
    if "covertest" in sys.argv:
        presum = 0
        aftsum = 0
        for i in range(nbtriangles):
            A, B, C = [get_coord(), get_coord(), get_coord()], \
                      [get_coord(), get_coord(), get_coord()], \
                      [get_coord(), get_coord(), get_coord()]
            tmp = Triangle3D(A, B, C)
            tmp2 = Triangle3D(A, B, C)
            tmp.voxelize_triangle()
            tmp.trim()
            presum += len(tmp.voxlist)
            tmp2.naive_voxelize()
            tmp2.trim()
            aftsum += len(tmp2.voxlist)

        print(presum/aftsum, presum, aftsum)
    if "naive" in sys.argv:
        method = Triangle3D.naive_voxelize
    if "benchmark" in sys.argv:
        totaltime = 0
        presum = 0
        aftsum = 0
        for i in range(nbtriangles):
            A, B, C = [get_coord(), get_coord(), get_coord()], \
                      [get_coord(), get_coord(), get_coord()], \
                      [get_coord(), get_coord(), get_coord()]
            tmp = Triangle3D(A, B, C)
            c1 = time.process_time()
            method(tmp)
            totaltime += time.process_time() - c1
            presum += len(tmp.voxlist)
            tmp.trim()
            aftsum += len(tmp.voxlist)

        print(aftsum/presum, aftsum, presum)
        print(totaltime)
    if "--pos" in sys.argv:
        index = sys.argv.index("--pos")
        try:
            val1 = sys.argv[index + 1]
            val2 = sys.argv[index + 2]
        except IndexError:
            print("Please provide 2 coordinates after '--pos'")
            exit()
        try:
            WINPOSX = int(val1)
            WINPOSY = int(val2)
        except ValueError:
            print("Please provide valid integer coordinates after '--pos'")
            exit()


# Get three random vertices for the demo
A, B, C = [get_coord(), get_coord(), get_coord()], \
          [get_coord(), get_coord(), get_coord()], \
          [get_coord(), get_coord(), get_coord()]

print(A, B, C)

# We construct a triangle from them
exa = Triangle3D(A, B, C)
method(exa)
exa.trim()

exa.normalize()


def init_gl(width, height):
    """Function to initialise some variables at the beginning.
    """

    global WINRATIO
    glClearColor(0.9, 0.9, 0.9, 1.0)
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    WINRATIO = float(width) / float(height)
    gluPerspective(FOVY, WINRATIO, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def key_pressed(*args):
    """Function for keyboard inputs.
    """
    global X_AXIS, Y_AXIS, Z_AXIS, AUTO_ROT, FOVY, XCOORD, YCOORD
    AUTO_ROT = 0
    if args[0] == b'e':
        Z_AXIS += CONST_ROT
    elif args[0] == b'r':
        X_AXIS -= CONST_ROT
    elif args[0] == b't':
        Z_AXIS -= CONST_ROT
    elif args[0] == b'd':
        Y_AXIS += CONST_ROT
    elif args[0] == b'f':
        X_AXIS += CONST_ROT
    elif args[0] == b'g':
        Y_AXIS -= CONST_ROT
    elif args[0] == b'+':
        FOVY = max(1.0, FOVY - 1.0)
    elif args[0] == b'-':
        FOVY += 1.0
    elif args[0] == b'c':
        FOVY = 45.0
    elif args[0] == b'i':
        YCOORD += 0.1
    elif args[0] == b'j':
        XCOORD -= 0.1
    elif args[0] == b'k':
        YCOORD -= 0.1
    elif args[0] == b'l':
        XCOORD += 0.1
    elif args[0] == b'a':
        AUTO_ROT = 1
    else:
        print(args[0])


def draw_gl_scene():
    """Function used as our draw loop.
    """
    global X_AXIS, Y_AXIS, Z_AXIS

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Zoom
    gluPerspective(FOVY, WINRATIO, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Translation
    glTranslatef(XCOORD, YCOORD, ZCOORD)

    # Rotation
    glRotatef(X_AXIS, 1.0, 0.0, 0.0)
    glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
    glRotatef(Z_AXIS, 0.0, 0.0, 1.0)

    # Draw Triangle
    exa.draw()

    # Draw voxels
    exa.draw_voxels()

    # Autorotation
    X_AXIS = X_AXIS - 0.8 * AUTO_ROT
    Z_AXIS = Z_AXIS - 0.01 * AUTO_ROT

    # Buffer swap since we are in double mode.
    glutSwapBuffers()


def main():
    """Main function called in the demo.
    """

    width = 480
    height = 480

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutInitWindowPosition(WINPOSX, WINPOSY)

    glutCreateWindow('proto')

    glutDisplayFunc(draw_gl_scene)
    glutIdleFunc(draw_gl_scene)
    glutKeyboardFunc(key_pressed)
    init_gl(width, height)
    glutMainLoop()


if __name__ == "__main__":
    main()
