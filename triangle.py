# -*- mode: python; indent-tabs-mode: nil; tab-width: 4 -*-

import numpy as np

from OpenGL.GL import *
from voxel import Voxel


def sort_on_axis(P0, P1, P2, i):
    """Function that sorts P0, P1 and P2 along the i axis.
    """
    if P0[i] <= P1[i]:
        if P0[i] <= P2[i]:
            if P1[i] <= P2[i]:
                return P0, P1, P2
            return P0, P2, P1
        return P2, P0, P1
    if P1[i] <= P2[i]:
        if P0[i] <= P2[i]:
            return P1, P0, P2
        return P1, P2, P0
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


def bresenham(P0, P1, Q, axis, color=(0, 1, 0)):
    """Bresenham's algorithm for the 2D case to mark the P0 to P1 line, putting
    it in Q. We use branchless programming as much as possible.
    color is to specify a color for the voxel line.
    """

    # Initialization.
    # We get X and Y.
    axes = [0, 1, 2]
    axes.remove(axis)
    X = axes[0]
    Y = axes[1]

    # We get dx and its sign, dy and its sign then the error.
    dx = P1[X] - P0[X]
    sx = sign(dx)
    dx = abs(dx)
    dy = P1[Y] - P0[Y]
    sy = sign(dy)
    dy = -abs(dy)
    errsum = dx + dy

    Pcurrent = P0.copy()
    while Pcurrent[X] != P1[X] or Pcurrent[Y] != P1[Y]:
        # We get the current error and double it.
        e2 = 2 * errsum

        # We determine if y or x is the one that needs to change.
        # In case of a tie we choose the one with the biggest deviation.
        ytest = e2 >= dy
        xtest = (e2 <= dx) - (ytest == 1 and e2 - dy <= dx - e2)
        ytest = (ytest == 1) - (xtest == 1)

        # We update the current point's coordinates.
        Pcurrent[X] += ytest * sx
        Pcurrent[Y] += xtest * sy

        # We add it to the Queue.
        Q += [Voxel(*Pcurrent, color)]

        # We update the error.
        errsum += ytest * dy + xtest * dx

    if Q:  # We remove the last one as it should be P1 which we already have.
        Q.pop()

    return Q


def mark_line_ILV(P0, P1, Q, color=(0, 1, 0)):
    """Function that marks a line of voxels between P0 and P1, putting it in Q.
    color is to specify a color for the voxel line.
    """
    dP = []
    dP += [sign(P1[0] -  P0[0])]
    dP += [sign(P1[1] -  P0[1])]
    dP += [sign(P1[2] -  P0[2])]

    # We test the 2D case.
    for i in range(3):
        if dP[i] == 0:  # If one of the axes is flat we use bresenham.
            return bresenham(P0, P1, Q, i, color)

    L = []
    L += [abs(P1[1] - P0[1]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[2] - P0[2])]
    L += [abs(P1[0] - P0[0]) * abs(P1[1] - P0[1])]
    M = L.copy()

    Pcurrent = P0.copy()
    while Pcurrent[0] != P1[0] or Pcurrent[1] != P1[1] or Pcurrent[2] != P1[2]:
        Lmin, Lindex = get_min(L)
        Pcurrent[Lindex] += dP[Lindex]
        L = [L[i] - Lmin for i in range(3)]
        L[Lindex] = 2 * M[Lindex]

        Q += [Voxel(*Pcurrent, color)]

    return Q


def get_sub_sequence(Q, slice_, axis):
    """Function that returns a slice of Q with a specific coordinate on axis.
    """
    VLC = []
    while Q and Q[0][axis] < slice_:
        VLC += [Q.pop(0)]

    return VLC


def get_next_in_slice(P0, Q, endP, axis):
    """Function that determines the next voxel for the subsequence Q.
    """
    # If Q is empty we just return P0.
    if not Q:
        return P0

    if len(Q) == 1:
        return Q.pop().get_coords()

    # We determine the axes we're projecting on.
    axes = [0, 1, 2]
    axes.remove(axis)
    X = axes[0]
    Y = axes[1]

    # We get the sides of the triangle.
    dXAB = P0[X] - endP[X]
    dYAB = P0[Y] - endP[Y]

    if dXAB == dYAB == 0:
        return Q.pop(0).get_coords()

    C1 = dYAB * P0[X] - dXAB * P0[Y]
    C2 = C1 + abs(dXAB) + abs(dYAB)
    C1 = C1 - abs(dXAB) - abs(dYAB)

    stock = Q.pop(0)
    while Q and C1 <= dYAB * Q[0][X] - dYAB * Q[0][Y] <= C2:
        stock = Q.pop(0)

    return stock.get_coords()


def fill_interior(Q1, Q2, P0, P2, axis):
    """Function that voxelizes the interior of the triangle P0P1P2.
    """
    # We're giving a colour gradient to each scanline to better visualize it.
    maxi = max(len(Q1), len(Q2))
    compteur = maxi / 20

    Q1c = Q1.copy()
    Q2c = Q2.copy()
    Qout = []
    Pstart = Q1c.pop(0)
    Pstop = Q2c.pop(0)

    def do_scanlines(edge1, edge2):
        nonlocal Pstop, Pstart, compteur
        while edge1 and edge2:
            tmp = get_next_in_slice(Pstart, edge1, Pstop, axis)
            Pstop = get_next_in_slice(Pstop, edge2, Pstart, axis)
            Pstart = tmp
            mark_line_ILV(Pstart, Pstop, Qout, (0, compteur / maxi, 0))
            compteur += 1

    for i in range(P2[axis] - P0[axis] + 1):
        slice_ = P0[axis] + i + 1

        Q1sub = get_sub_sequence(Q1c, slice_, axis)
        Q2sub = get_sub_sequence(Q2c, slice_, axis)

        do_scanlines(Q1sub, Q2sub)

        temp, temp2 = Pstart, Pstop

        # We check to see if there's something left in the edge and react.
        if len(Q1sub) > 1:
            mark_line_ILV(Pstop, Q1sub[-1], Q2sub, (0, compteur / maxi, 0))
            do_scanlines(Q1sub, Q2sub)
            if len(Q1sub) > 2:
                mid = len(Q1sub) // 2
                mark_line_ILV(Pstop, Q1sub[mid], Q2sub, (0, compteur / maxi, 0))
                do_scanlines(Q1sub, Q2sub)
        elif len(Q2sub) > 1:
            mark_line_ILV(Pstart, Q2sub[-1], Q1sub, (0, compteur / maxi, 0))
            do_scanlines(Q1sub, Q2sub)
            if len(Q2sub) > 2:
                mid = len(Q2sub) // 2
                mark_line_ILV(Pstart, Q2sub[mid], Q1sub, (0, compteur / maxi, 0))
                do_scanlines(Q1sub, Q2sub)

        Pstart, Pstop = temp, temp2

    return Qout


class Triangle3D():
    """Triangle class to represent a triangle in 3D for voxelization purposes.
    """

    def __init__(self, s1, s2, s3, color=(1, 0, 0)):
        """s1, s2, s3: the three vertices in [x, y, z] format.
        color: for rendering purposes, gives a colour the triangle's interior.
        """
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.color = color
        self.voxlist = []
        self._dominant_axis = None

    def __repr__(self):
        return f'Triangle3D(s1:{self.s1}, s2:{self.s2}, s3:{self.s3}, color:{self.color}, voxlist:{self.voxlist})'

    def draw(self):
        """Function that draws the triangle in openGL.
        """
        glBegin(GL_TRIANGLES)

        glColor3f(*self.color)
        for sommet in [self.s1, self.s2, self.s3]:
            glVertex3f(*sommet)

        glEnd()

    def normalize(self, maqs=None):
        """Function to normalize from integer coordinates to -1.0 to 1.0 floats.
        """
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

        # We also normalize of the voxels in the triangle's voxelization.
        Voxel.width = 1 / maqs
        for voxel in self.voxlist:
            voxel.normalize(maqs)

    def find_dominant_axis(self):
        """Function to determine the dominant axis of the triangle.
        """
        if self._dominant_axis is not None:
            return self._dominant_axis

        # First we get a normal vector through a cross product.
        a = (np.array(self.s2) - np.array(self.s1)).tolist()
        b = (np.array(self.s3) - np.array(self.s1)).tolist()
        normal_vector = [a[1] * b[2] - a[2] * b[1],
                         a[2] * b[0] - a[0] * b[2],
                         a[0] * b[1] - a[1] * b[0]]

        # Then we determine the maximum value of that vector and its axis.
        i = 0
        val = normal_vector[0]
        for j in range(1, 3):
            if normal_vector[j] > val:
                i = j
                val = normal_vector[j]

        self._dominant_axis = i

        return i

    def add_voxel(self, voxel):
        """Function to add a voxel to the voxelization of the triangle.
        """
        self.voxlist += [voxel]

    def draw_voxels(self):
        """Function to draw the triangle's voxelization.
        """
        for voxel in self.voxlist:
            voxel.draw()

    def voxelize_triangle(self):
        """Voxelization of the triangle through a method by Zhang et al.
        We stick to their notations as much as possible.

        Note that calling this method multiple times will not clear the previous
        values.
        """
        P0, P1, P2 = self.s1, self.s2, self.s3

        # First we find the dominant axis.
        i = self.find_dominant_axis()

        # Then we sort the vertices along that axis (smallest to highest value).
        P0, P1, P2 = sort_on_axis(P0, P1, P2, i)

        # We declare 3 queues with the beginning vertices as a starting point.
        Q0, Q1, Q2 = [Voxel(*P0)], [Voxel(*P1)], [Voxel(*P0)]

        # Then we voxelize each edge.
        mark_line_ILV(P0, P1, Q0, (0, 0, 1))
        mark_line_ILV(P1, P2, Q1, (0, 1, 1))
        mark_line_ILV(P0, P2, Q2, (1, 1, 0))

        # We add the vertex to terminate the edge for calculation purposes.
        Q2 += [Voxel(*P2)]

        # Q1 becomes the union of Q1 and Q0.
        Q1 = Q0 + Q1 + [Voxel(*P2)]

        # Then we apply the scanline algorithm to fill the interior.
        interior = fill_interior(Q1, Q2, P0, P2, i)

        # We'll have P0 and P2 twice unless we do this.
        Q1.pop(0)
        Q2.pop()

        # Finally we add everything to the voxelization.
        self.voxlist += Q1 + Q2 + interior

    def naive_voxelize(self):
        """Voxelization of the triangle using a naive scanline method.
        Same general principles as the normal voxelize.
        """
        P0, P1, P2 = self.s1, self.s2, self.s3
        axis = self.find_dominant_axis()
        P0, P1, P2 = sort_on_axis(P0, P1, P2, axis)
        Q0, Q1, Q2 = [Voxel(*P0)], [Voxel(*P1)], [Voxel(*P0)]
        mark_line_ILV(P0, P1, Q0, (0, 0, 1))
        mark_line_ILV(P1, P2, Q1, (0, 1, 1))
        mark_line_ILV(P0, P2, Q2, (1, 1, 0))
        Q1 += [Voxel(*P2)]
        Q2 += [Voxel(*P2)]
        Q1c = Q1.copy()
        Q2c = Q2.copy()
        Pstart = P0.copy()
        Pstop = P1.copy()
        i = 0

        while Q1c and Q2c and i <= P2[axis] - P0[axis]:
            slice_ = P0[axis] + i + 1
            Q1sub = get_sub_sequence(Q1c, slice_, axis)
            Q2sub = get_sub_sequence(Q2c, slice_, axis)
            while Q1sub or Q2sub:
                if Q2sub:
                    Pstart = Q2sub.pop(0)
                if Q1sub:
                    Pstop = Q1sub.pop(0)
                mark_line_ILV(Pstart, Pstop, Q0)
            i += 1
        self.voxlist += Q2 + Q1 + Q0

    def trim(self):
        """Function to remove any voxel overlapping with another.
        Mostly for rendering purposes.
        """
        self.voxlist = list(set(self.voxlist))
