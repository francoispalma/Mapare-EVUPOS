from OpenGL.GL import *
from voxel import Voxel
import numpy as np

def sort_on_axis(P0, P1, P2, i):
    if P0[i] <= P1[i]:
        if P0[i] <= P2[i]:
            if P1[i] <= P2[i]:
                return P0, P1, P2
            else:
                return P0, P2, P1
        else:
            return P2, P0, P1
    else:
        if P1[i] <= P2[i]:
            if P0[i] <= P2[i]:
                return P1, P0, P2
            else:
                return P1, P2, P0
        else:
            return P2, P1, P0


def sign(expr):
    return -1 + (expr > 0) * 2


def get_min(L):
    mini = L[0]
    index = 0
    for j in range(1, 3):
        if L[j] < L[index]:
            mini = L[j]
            index = j
    return mini, index


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
    for i in range(3):
        M[i] += (M[i] == 0)  # Règle certain cas pathologiques
    Pcurrent = P0.copy()
    while Pcurrent[0] != P1[0] or Pcurrent[1] != P1[1] or Pcurrent[2] != P1[2]:
        Lmin, Lindex = get_min(L)
        # On s'assure qu'on n'ajoute pas des choses quand il ne faut pas
        Pcurrent[Lindex] += dP[Lindex] * (1 - (Pcurrent[Lindex] == P1[Lindex]))
        L = (np.array(L) - Lmin).tolist()
        # Pour d'autres cas pathologiques
        L[Lindex] = 2 * M[Lindex] + 65536 * (Pcurrent[Lindex] == P1[Lindex])
        Q += [Voxel(*Pcurrent)]

    return Q


def get_sub_sequence(Q, slice_, axis):
    i = 0
    while i < len(Q) and Q[i][axis] < slice_:
        i += 1
    VLC = Q[:i]
    Q[:] = Q[i:]
    return VLC


def dist(A, B, x, y):
    return ((B[x] - A[x]) ** 2 + (B[y] - A[y]) ** 2) ** 0.5

def distA(A, B, x, y, dXAB, dYAB):
    val = abs(dYAB * (B[x] - A[x]) - dXAB * (B[y] - A[y]))
    return val / (dXAB ** 2 + dYAB ** 2 + (dXAB == 0 and dYAB == 0))

def get_next_in_slice(P0, Q, endP, axis):
    if not Q:
        return P0
    axes = [0, 1, 2]
    axes.remove(axis)
    X = axes[0]
    Y = axes[1]
    dXAB = endP[X] - P0[X]
    dYAB = endP[Y] - P0[Y]
    # TODO: passer en entier
    dchapeau = (abs(dXAB) + abs(dYAB)) / ((dXAB ** 2 + dYAB ** 2) ** 0.5 + (dXAB == 0 and dYAB == 0))
    currP = Q[0]
    # Cas pathologique:
    if Q and currP[0] == P0[0] and currP[1] == P0[1] and currP[2] == P0[2]:
        Q.pop()
    while len(Q) > 1 and dist(P0, Q[1], X, Y) < dchapeau:
        Q.pop()
    
    return Q.pop().get_coords()


def fill_interior(Q1, Q2, P0, P1, P2, axis):
    Q1c = Q1.copy()
    Q2c = Q2.copy()
    Qout = []
    Pstart = P0
    Pstop = P1
    for i in range (P2[axis] - P0[axis] + 1):
        slice_ = P0[axis] + i + 0.5
        Q1sub = get_sub_sequence(Q1c, slice_, axis)
        Q2sub = get_sub_sequence(Q2c, slice_, axis)
        while Q1sub or Q2sub:
            tmp = get_next_in_slice(Pstart, Q1sub, Pstop, axis)
            Pstop = get_next_in_slice(Pstop, Q2sub, Pstart, axis)
            Pstart = tmp
            mark_line_ILV(Pstart, Pstop, Qout)
    return Qout


class Triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []
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
        Q0, Q1, Q2 = [], [], []
        mark_line_ILV(P0, P1, Q0)
        mark_line_ILV(P1, P2, Q1)
        mark_line_ILV(P0, P2, Q2)
        #Q1 = Q0 + Q1
        vlergh = fill_interior(Q2, Q1, P0, P1, P2, i)
        self.voxlist += Q0 + Q1 + Q2 + vlergh

    def trim(self):
        print(len(self.voxlist))
        self.voxlist = list(set(self.voxlist))
        print(len(self.voxlist))
