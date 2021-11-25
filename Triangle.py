from OpenGL.GL import *
from Voxel import Voxel
import numpy as np


def sort_on_axis(P0, P1, P2, i):
    if P0[i] > P1[i]:
        if P0[i] > P2[i]:
            if P1[i] > P2[i]:
                return P0, P1, P2
            else:
                return P0, P2, P1
        else:
            return P2, P0, P1
    else:
        if P1[i] > P2[i]:
            if P0[i] > P2[i]:
                return P1, P0, P2
            else:
                return P1, P2, P0
        else:
            return P2, P1, P0


def sign(expr):
    return -1 + (expr >= 0) * 2


def mark_line_ILV(P0, P1, Q):
    dP = []
    dP += [sign(P1[0] -  P0[0])]
    dP += [sign(P1[1] -  P0[1])]
    dP += [sign(P1[2] -  P0[2])]
    L = []
    L += [abs(P1[1] - P0[1]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[1] - P0[1])]
    M = L.copy()
    Pcurrent = P0.copy()
    while Pcurrent[0] != P1[0] or Pcurrent[1] != P1[1] or Pcurrent[2] != P1[2]:
        Lmin = min(L[0], L[1], L[2])
        Lindex = abs((Lmin == L[1]) - (Lmin == L[2]) * 2)
        Pcurrent[Lindex] = Pcurrent[Lindex] + dP[Lindex]
        L = (np.array(L) - Lmin).tolist()
        L[Lindex] = 2 * M[Lindex]
        Q += [Voxel(*Pcurrent)]

    return Q


def fill_interior(Q1, Q2, P0, P2, axis):
    for i in range (P2[axis] - P0[axis]):
        slice_ = P0[axis] + i + 0.5
        Q1sub = get_sub_sequence(Q1, slice_)
        Q2sub = get_sub_sequence(Q2, slice_)
        Qout = [[]]
        while Q1sub or Q2sub:
            if Q1sub:
                Pstart = Q1sub.pop()
            if Q2sub:
                Pstop = Q2sub.pop()
            mark_line_ILV(Pstart, Pstop, Qout[0])
        return Qout[0]


class Triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []
        self._projection = None
        self._dominant_axis = None

    def __repr__(self):
        return f'Triangle3D(s1:{self.s1}, s2:{self.s2}, s3:{self.s3}, color:{self.color}, voxlist:{self.voxlist})'

    def draw(self):
        glBegin(GL_TRIANGLES)

        glColor3f(*self.color)
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs=None):
        if maqs is None or maqs == 0:
            maqs = 0
            for coord in self.s1 + self.s2 + self.s3:
                if abs(coord) > maqs:
                    maqs = abs(coord)

        if maqs == 0:
            raise ValueError

        self.s1 = (np.array(self.s1) / maqs).tolist()
        self.s2 = (np.array(self.s2) / maqs).tolist()
        self.s3 = (np.array(self.s3) / maqs).tolist()
        Voxel.width = 1 / maqs
        for voxel in self.voxlist:
            voxel.normalize(maqs)
        if self._projection is not None:
            self._projection.normalize(maqs)

    def find_dominant_axis(self):
        if self._dominant_axis is not None:
            return self._dominant_axis
        a = (np.array(self.s2) - np.array(self.s1)).tolist()
        b = (np.array(self.s3) - np.array(self.s1)).tolist()
        normal_vector = [a[1] * b[2] - a[2] * b[1],
                         a[2] * b[0] - a[0] * b[2],
                         a[0] * b[1] - a[1] * b[0]]
        i = 0
        val = normal_vector[0]
        for j in range(1, 3):
            if normal_vector[j] > val:
                i = j
                val = normal_vector[j]

        self._dominant_axis = i

        return i

    def add_voxel(self, voxel):
        self.voxlist += [voxel]

    def draw_voxels(self):
        for voxel in self.voxlist:
            voxel.draw()

    def voxelize_triangle(self):
        P0, P1, P2 = self.s1, self.s2, self.s3
        if self._dominant_axis is not None:
            i = self._dominant_axis
        else:
            i = self.find_dominant_axis()
        P0, P1, P2 = sort_on_axis(P0, P1, P2, i)
        Q0, Q1, Q2 = [[]], [[]], [[]]
        mark_line_ILV(P0, P1, Q0[0])
        mark_line_ILV(P1, P2, Q1[0])
        mark_line_ILV(P0, P2, Q2[0])
        Q1[0] = Q0[0] + Q1[0]
        fill_interior(Q1, Q2, P0, P2, i)
        self.voxlist += Q1[0] + Q2[0]
        
