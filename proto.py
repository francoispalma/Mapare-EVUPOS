from random import randrange

from OpenGL.GLU import *
from OpenGL.GLUT import *

from Triangle import *
from Voxel import *

ESCAPE = '\033'
window = 0

# rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0


def get_coord():
    return randrange(201) - 100


A, B, C = [get_coord(), get_coord(), get_coord()], \
          [get_coord(), get_coord(), get_coord()], \
          [get_coord(), get_coord(), get_coord()]

# A, B, C = [-0.5, -0.4, 0.0], [0.7, -0.5, -0.5], [0.0, 0.8, 0.3]

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
    #   Z_AXIS = Z_AXIS - 0.30

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
