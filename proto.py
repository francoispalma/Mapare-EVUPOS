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


VERTEX_SHADER = """
 
#version 140
 
    in vec4 position;
    void main() {
    gl_Position = position;
 
}
 
 
"""
 
 
 
FRAGMENT_SHADER = """
#version 140
 
    void main() {
 
    gl_FragColor = 
 
    vec4(1.0f, 0.0f,0.0f,1.0f);
 
    }
 
"""
 
shaderProgram = None
quadric = None

def init():
    global quadric
    global VERTEXT_SHADER
    global FRAGMEN_SHADER
    global shaderProgram

    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    
    triangles = [-0.5, -0.5, 0.0,
                 0.5, -0.5, 0.0,
                 0.0, 0.5, 0.0]
    
    triangles = np.array(triangles, dtype=np.float32)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, triangles.nbytes, triangles, GL_STATIC_DRAW)
    
    position = glGetAttribLocation(shaderProgram, 'position')
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(position)
#    quadric = gluNewQuadric()
#    gluQuadricDrawStyle(quadric, GLU_FILL)
    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glUseProgram(shaderProgram)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glUseProgram(0)
    
    glutSwapBuffers()

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow('proto')
    glutReshapeWindow(512, 512)
    
    init()
    
    glutDisplayFunc(display)

    glutMainLoop()
