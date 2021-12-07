# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

from OpenGL.GL import *
from voxel import Voxel, Voxelmatrix
import numpy as np


def sort_on_axis(P0, P1, P2, i):
    """Function that sorts P0, P1 and P2 along the i axis.
    """
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
    """Function that returns the sign of the expression expr. 0 returns 0.
    """
    return -1 + (expr > 0) * 2 + (expr == 0)


def get_min(L):
    """Function that returns the minimum value and index of a list L.
    """
    mini = L[0]
    index = 0
    for j in range(1, 3):
        if L[j] < L[index]:
            mini = L[j]
            index = j
    return mini, index


def bresenham(P0, P1, Q, axis, vm, color=(0, 1, 0)):
    """Bresenham's algorithm for the 2D case to mark the P0 to P1 line.
    """
    axes = [0, 1, 2]
    axes.remove(axis)
    X = axes[0]
    Y = axes[1]
    dx = P1[X] - P0[X]
    sx = sign(dx)
    dx = abs(dx)
    dy = P1[Y] - P0[Y]
    sy = sign(dy)
    dy = -abs(dy)
    err = dx + dy

    Pcurrent = P0.copy()
    while Pcurrent[X] != P1[X] or Pcurrent[Y] != P1[Y]:
        e2 = 2 * err

        ytest = e2 >= dy
        err += ytest * dy
        Pcurrent[X] += ytest * sx

        xtest = e2 <= dx
        err += xtest * dx
        Pcurrent[Y] += xtest * sy

        if Pcurrent not in vm:
            Q += [Voxel(*Pcurrent, color)]
        vm.hit(*Pcurrent)

    if Q:  # We remove the last one as it should be P1 which we already have.
        Q.pop()

    return Q


def mark_line_ILV(P0, P1, Q, vm, color=(0, 1, 0)):
    """Function that marks a line of voxels between P0 and P1, putting it in Q.
    """
    dP = []
    dP += [sign(P1[0] -  P0[0])]
    dP += [sign(P1[1] -  P0[1])]
    dP += [sign(P1[2] -  P0[2])]

    # We test the 2D case.
    axis = None
    for i in range(3):
        if dP[i] == 0:
            axis = i
            break
    if axis is not None:
        return bresenham(P0, P1, Q, axis, vm, color)

    L = []
    L += [abs(P1[1] - P0[1]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[1] - P0[1])]
    M = L.copy()

    Pcurrent = P0.copy()
    while Pcurrent[0] != P1[0] or Pcurrent[1] != P1[1] or Pcurrent[2] != P1[2]:
        Lmin, Lindex = get_min(L)
        Pcurrent[Lindex] += dP[Lindex]
        L = (np.array(L) - Lmin).tolist()
        L[Lindex] = 2 * M[Lindex]
        if Pcurrent not in vm:
            Q += [Voxel(*Pcurrent, color)]
        vm.hit(*Pcurrent)

    return Q


def get_sub_sequence(Q, slice_, axis):
    """Function that returns a slice of Q with a specific coordinate on axis.
    """
    i = 0
    while i < len(Q) and Q[i][axis] < slice_:
        i += 1
    VLC = Q[:i]
    
    # We remove the sequence for the next iteration.
    Q[:] = Q[i:]
    return VLC


def get_next_in_slice(P0, Q, endP, axis):
    """Function that determines the next voxel for the subsequence Q.
    """
    # If Q is empty we just return P0
    if not Q:
        return P0

    # We determine the axes we're projecting on.
    axes = [0, 1, 2]
    axes.remove(axis)
    X = axes[0]
    Y = axes[1]

    # We get the sides of the triangle.
    dXAB = endP[X] - P0[X]
    dYAB = endP[Y] - P0[Y]

    C0 = dYAB * P0[X] - dXAB * P0[Y]
    C1 = C0 - abs(dXAB) - abs(dYAB)
    C2 = C0 + abs(dXAB) + abs(dYAB)
    C0 += dXAB * sign(Q[0][X] - P0[X]) + dYAB * sign(Q[0][Y] - P0[Y])

    if len(Q) > 1 and C1 <= C0 <= C2:
        while len(Q) > 1 and C1 <= C0 <= C2:
            C0 += dYAB * sign(Q[1][X] - Q[0][X]) + dXAB * sign(Q[1][Y] - Q[0][Y])
            stock = Q.pop(0)
    else:
        stock = Q.pop(0)

    return stock.get_coords()


def fill_interior(Q1, Q2, P0, P1, P2, axis, vm):
    """Function that voxelizes the interior of the triangle P0P1P2.
    """
    maxi = max(len(Q1), len(Q2))
    compteur = maxi / 20
    Q1c = Q1.copy()
    Q2c = Q2.copy()
    Qout = []
    Pstart = Q1c.pop(0)
    Pstop = Q2c.pop(0)
    for i in range (P2[axis] - P0[axis]):
        slice_ = P0[axis] + i + 0.5
        Q1sub = get_sub_sequence(Q1c, slice_, axis)
        Q2sub = get_sub_sequence(Q2c, slice_, axis)
        while Q1sub and Q2sub:
            tmp = get_next_in_slice(Pstart, Q1sub, Pstop, axis)
            Pstop = get_next_in_slice(Pstop, Q2sub, Pstart, axis)
            Pstart = tmp
            mark_line_ILV(Pstart, Pstop, Qout, vm, (0, compteur / maxi, 0))
            compteur += 1
    return Qout


class Triangle3D(object):
    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []
        self._dominant_axis = None

        self._voxmatrix = Voxelmatrix(s1, s2, s3)

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
        i = self.find_dominant_axis()
        P0, P1, P2 = sort_on_axis(P0, P1, P2, i)
        Q0, Q1, Q2 = [Voxel(*P0)], [Voxel(*P1)], [Voxel(*P0)]
        self._voxmatrix.hit(*P0)
        self._voxmatrix.hit(*P1)
        self._voxmatrix.hit(*P2)
        mark_line_ILV(P0, P1, Q0, self._voxmatrix, (0, 0, 1))
        mark_line_ILV(P1, P2, Q1, self._voxmatrix, (0, 1, 1))
        mark_line_ILV(P0, P2, Q2, self._voxmatrix, (1, 1, 0))
        Q2 += [Voxel(*P2)]
        Q1 = Q0 + Q1 + [Voxel(*P2)]
        interior = fill_interior(Q1, Q2, P0, P1, P2, i, self._voxmatrix)
        self.voxlist += Q1[1:] + Q2[:-1] + interior

    def trim(self):
        self.voxlist = list(set(self.voxlist))
