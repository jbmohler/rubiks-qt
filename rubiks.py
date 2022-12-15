import math
import itertools
import random

HEX_COLORS = {
        'W': '#ffffff',
        'B': '#0000ff',
        'G': '#00ff00',
        'O': '#ff7518',
        'R': '#d70040',
        'Y': '#ffea00',
        }

class Rubiks:
    COLORS = 'ROBGWY'
    OFFSET = {
                '+x': 0,
                '-x': 1,
                '+y': 2,
                '-y': 3,
                '+z': 4,
                '-z': 5}

    FACE_ROT1 = [ (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1)]
    FACE_ROT2 = [ (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

    FACE_LEFT = {
            '+z': FACE_ROT1,
            '-z': FACE_ROT2,
            '+x': FACE_ROT1,
            '-x': FACE_ROT2,
            '+y': FACE_ROT2,
            '-y': FACE_ROT1,
            }

    ADJ_LEFT = {
        '+z': [
            ('+x', [(y, 2) for y in (0, 1, 2)]),
            ('+y', [(x, 2) for x in (2, 1, 0)]),
            ('-x', [(y, 2) for y in (2, 1, 0)]),
            ('-y', [(x, 2) for x in (0, 1, 2)]),
            ] ,
        '-z': [
            ('+y', [(x, 0) for x in (0, 1, 2)]),
            ('+x', [(y, 0) for y in (2, 1, 0)]),
            ('-y', [(x, 0) for x in (2, 1, 0)]),
            ('-x', [(y, 0) for y in (0, 1, 2)]),
            ],
        '+x':[
            ('+y', [(2, z) for z in (0, 1, 2)]),
            ('+z', [(2, y) for y in (2, 1, 0)]),
            ('-y', [(2, z) for z in (2, 1, 0)]),
            ('-z', [(2, y) for y in (0, 1, 2)]),
            ],
        '-x':[
            ('+z', [(0, y) for y in (0, 1, 2)]),
            ('+y', [(0, z) for z in (2, 1, 0)]),
            ('-z', [(0, y) for y in (2, 1, 0)]),
            ('-y', [(0, z) for z in (0, 1, 2)]),
            ],
        '+y':[
            ('+z', [(x, 2) for x in (0, 1, 2)]),
            ('+x', [(2, z) for z in (2, 1, 0)]),
            ('-z', [(x, 2) for x in (2, 1, 0)]),
            ('-x', [(2, z) for z in (0, 1, 2)]),
            ],
        '-y':[
            ('+x', [(0, z) for z in (0, 1, 2)]),
            ('+z', [(x, 0) for x in (2, 1, 0)]),
            ('-x', [(0, z) for z in (2, 1, 0)]),
            ('-z', [(x, 0) for x in (0, 1, 2)]),
            ],
        }

    def __init__(self):
        self.sides = self.solved_map()

    def scramble(self):
        for n in range(30):
            sign = random.choice('+-')
            axis = random.choice('xyz')
            direction = random.choice('lr')

            print(f'{sign}{axis}', direction)
            self.rotate(f'{sign}{axis}', direction)

    def solved_map(self):
        return [color for color in self.COLORS for _ in range(9)]

    def is_solved(self):
        return self.sides == self.solved_map()

    def label(self, face, x, y):
        offset = self.OFFSET
        return self.sides[offset[face]*9+x*3+y]

    def set_label(self, face, x, y, color):
        offset = self.OFFSET

        self.sides[offset[face]*9+x*3+y] = color

    def rotate(self, face, lr):
        pebbles = None
        face_left = self.FACE_LEFT[face]
        if lr == 'l':
            pebbles = list(face_left)
        elif lr == 'r':
            pebbles = list(reversed(face_left))

        adj = [self.label(face, x, y) for x, y in pebbles]

        pebbles = pebbles[2:] + pebbles[:2]

        for color, xy in zip(adj, pebbles):
            x, y = xy
            self.set_label(face, x, y, color)

        adjacent = [(f, xy[0], xy[1]) for f, coords in self.ADJ_LEFT[face] for xy in coords]
        pebbles = None
        if lr == 'l':
            pebbles = adjacent
        elif lr == 'r':
            pebbles = list(reversed(adjacent))

        adj = [self.label(axis, x, y) for axis, x, y in pebbles]

        pebbles = pebbles[3:] + pebbles[:3]

        for color, ax_xy in zip(adj, pebbles):
            ax, x, y = ax_xy
            self.set_label(ax, x, y, color)

        self.sanity_check()

    def label_3t(self, face, xyz):
        z2 = lambda sx: 0 if sx == '-' else 2

        if face[1] == 'x':
            if z2(face[0]) != xyz[0]:
                raise RuntimeError(f'{face} with 3-tuple {xyz} is confusing me')
            return self.label(face, xyz[1], xyz[2])
        if face[1] == 'y':
            if z2(face[0]) != xyz[1]:
                raise RuntimeError(f'{face} with 3-tuple {xyz} is confusing me')
            return self.label(face, xyz[0], xyz[2])
        if face[1] == 'z':
            if z2(face[0]) != xyz[2]:
                raise RuntimeError(f'{face} with 3-tuple {xyz} is confusing me')
            return self.label(face, xyz[0], xyz[1])
        raise RuntimeError(f'unknown face {face}')

    def sanity_check(self):
        z2 = lambda sx: 0 if sx == '-' else 2

        corners_target = []
        corners_are = []
        for s1, s2, s3 in itertools.product('-+', '-+', '-+'):
            f1, f2, f3 = s1 + 'x', s2 + 'y', s3 + 'z'

            t = [self.label(f1, 1,1 ), self.label(f2, 1, 1), self.label(f3, 1, 1)]
            corners_target.append(''.join(sorted(t)))

            coords = z2(s1), z2(s2), z2(s3)
            t = [self.label_3t(f1, coords), self.label_3t(f2, coords), self.label_3t(f3, coords)]
            if len(set(t)) != 3:
                raise RuntimeError(f'corner with coords {f1}, {f2}, {f3} has duplicate color')
            corners_are.append(''.join(sorted(t)))

        if set(corners_target) != set(corners_are):
            raise RuntimeError('mis-configured corner')


def dot(v1, v2):
    return sum(c1*c2 for c1, c2 in zip(v1, v2))

def cross(v1, v2):
    return (
            v1[1]*v2[2]-v1[2]*v2[1],
            v1[0]*v2[2]-v1[2]*v2[0],
            v1[0]*v2[1]-v1[1]*v2[0],
            )

def make_unit(v):
    rad = math.sqrt(sum(c**2 for c in v))
    return tuple(c/rad for c in v)

def on_sphere(p3, radius):
    vlen = math.sqrt(sum(c**2 for c in p3))
    return tuple(c*radius/vlen for c in p3)

def vsum(v1, v2):
    return [c1+c2 for c1, c2 in zip(v1, v2)]

def vneg(v):
    return [-c for c in v]

def navigate(pers, nstar, direction):
    vstr = lambda v: f'({v[0]:.1f}, {v[1]:.1f}, {v[2]:.1f})'
    print(vstr(pers), 'north ', vstr(nstar))
    pers = on_sphere(pers, 10)
    nstar = on_sphere(nstar, 10)

    perp = make_unit(pers)
    north = make_unit(vsum(nstar, vneg(pers)))
    east = cross(north, perp)

    NAV_DISTANCE = .3

    if direction == 'north':
        # move pers and nstar north
        pers = vsum(pers, on_sphere(north, NAV_DISTANCE))
        nstar = vsum(nstar, on_sphere(north, NAV_DISTANCE))
    elif direction == 'south':
        # move pers and nstar south
        pers = vsum(pers, on_sphere(vneg(north), NAV_DISTANCE))
        nstar = vsum(nstar, on_sphere(vneg(north), NAV_DISTANCE))
    elif direction == 'east':
        # move pers east (keep nstar same)
        pers = vsum(pers, on_sphere(east, NAV_DISTANCE))
    elif direction == 'west':
        # move pers west (keep nstar same)
        pers = vsum(pers, on_sphere(vneg(east), NAV_DISTANCE))



    print(vstr(pers), 'north ', vstr(nstar))

    return pers, nstar

def pp_plane(p1, p2, nv):
    # the plane in question is plane perpendicular to nv passing through the
    # point at 2*nv; the plane is tangent to the 2 sphere centered at the
    # origin

    # plane equation given by
    #  nv <dot> (x, y, z) = 2 * nv <dot> nv

    # line equation given by p1 + t * (p2 - p1) intersects the plane at ...
    # nv <dot> (p1x + t * (p2x - p1x), .. ) = 2 * nv <dot> nv
    # nv <dot> p1 + t * nv <dot> (p2-p1) = 2 * nv <dot> nv

    # solving for t, we get
    # t = (2 * nv <dot> nv - nv <dot> p1) / (nv <dot> (p2-p1))

    delta = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    t = (2 * dot(nv, nv) - dot(nv, p1)) / dot(nv, delta)
    return (p1[0] + t*delta[0], p1[1] + t*delta[1], p1[2] + t*delta[2])

def draw(painter, cube, pers, nstar):
    from PySide6 import QtWidgets, QtCore, QtGui

    # rescale pers to be on a sphere of radius 10 from the origin
    pers = on_sphere(pers, 10.)
    normvec = on_sphere(pers, 1.)

    north_p = pp_plane((0, 0, 0), nstar, normvec)

    # make unit vector north and east on the viewing plane
    north = make_unit(vsum(north_p, vneg(pp_plane((0, 0, 0), pers, normvec))))
    east = cross(north, normvec)

    CENTER = 200
    SQSIZE = 120

    faces = []

    if pers[0] > 0:
        faces.append("+x")
    if pers[1] > 0:
        faces.append("+y")
    if pers[2] > 0:
        faces.append("+z")
    if pers[0] < 0:
        faces.append("-x")
    if pers[1] < 0:
        faces.append("-y")
    if pers[2] < 0:
        faces.append("-z")

    painter.drawText(200, 15, str(faces))

    pen = QtGui.QPen(QtGui.QColor('black'))
    pen.setWidth(2)
    painter.setPen(pen)

    for face in faces:
        for i in range(3):
            for j in range(3):
                color = cube.label(face, i, j)

                i1 = -1 + i *2/3
                i2 = -1 + (i+1) * 2/3
                j1 = -1 + j *2/3
                j2 = -1 + (j+1) * 2/3

                # get coords of corner of the face
                if face == '+x':
                    rect = [
                            (1., i1, j1),
                            (1., i1, j2),
                            (1., i2, j2),
                            (1., i2, j1),
                            ]
                if face == '-x':
                    rect = [
                            (-1., i1, j1),
                            (-1., i1, j2),
                            (-1., i2, j2),
                            (-1., i2, j1),
                            ]
                if face == '+y':
                    rect = [
                            (i1, 1, j1),
                            (i1, 1, j2),
                            (i2, 1, j2),
                            (i2, 1, j1),
                            ]
                if face == '-y':
                    rect = [
                            (i1, -1, j1),
                            (i1, -1, j2),
                            (i2, -1, j2),
                            (i2, -1, j1),
                            ]
                if face == '+z':
                    rect = [
                            (i1, j1, 1),
                            (i1, j2, 1),
                            (i2, j2, 1),
                            (i2, j1, 1),
                            ]
                if face == '-z':
                    rect = [
                            (i1, j1, -1),
                            (i1, j2, -1),
                            (i2, j2, -1),
                            (i2, j1, -1),
                            ]

                poly = QtGui.QPolygonF()
                for p3d in rect:
                    on_plane = pp_plane(p3d, pers, normvec)
                    poly.append(QtCore.QPointF(
                        CENTER+dot(east, on_plane)*SQSIZE,
                        CENTER-dot(north, on_plane)*SQSIZE,
                        ))

                center = poly.boundingRect().center()

                # draw polygon
                painter.setBrush(QtGui.QColor(HEX_COLORS[color]))
                painter.drawPolygon(poly)
                #painter.drawText(center, f'{i}-{j}')
