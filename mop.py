from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
 
ESCAPE = '\033'
 
window = 0
 
#rotation
X_AXIS = 0.0
Y_AXIS = 0.0
Z_AXIS = 0.0
 
DIRECTION = 1
 
 
class triangle3D(object):
    
    def __init__(self, s1, s2, s3):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
    
    def draw(self):
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

exa = triangle3D([-0.5, -0.4, 0.0],
                 [0.7, -0.5, -0.5],
                 [0.0, 0.8, 0.3])

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
    global DIRECTION
 
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
    glLoadIdentity()
    glTranslatef(0.0,0.0,-6.0)
 
    glRotatef(X_AXIS,1.0,0.0,0.0)
    glRotatef(Y_AXIS,0.0,1.0,0.0)
    glRotatef(Z_AXIS,0.0,0.0,1.0)
 
    # Draw Triangle
    glBegin(GL_TRIANGLES)
 
    glColor3f(1.0, 0.0, 0.0)
    exa.draw()

    glEnd()
 
 
    X_AXIS = X_AXIS - 0.30
#    Z_AXIS = Z_AXIS - 0.30
 
    glutSwapBuffers()
 
 
 
def main():
 
    global window
 
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640,480)
    glutInitWindowPosition(200,200)

    window = glutCreateWindow('OpenGL Python Triangle')
 
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutKeyboardFunc(keyPressed)
    InitGL(640, 480)
    glutMainLoop()
 
if __name__ == "__main__":
    main() 
