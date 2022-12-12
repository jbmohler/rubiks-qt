import random

HEX_COLORS = {
        'W': '#ffffff',
        'B': '#0000ff',
        'G': '#00ff00',
        'O': '#ffa500',
        'R': '#ff0000',
        'Y': '#ffff00',
        }

class Rubiks:
    COLORS = 'WYROBG'
    OFFSET = {
                '+x': 0,
                '-x': 1,
                '+y': 2,
                '-y': 3,
                '+z': 4,
                '-z': 5}

    FACE_LEFT = [ (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)]

    ADJ_LEFT = {
        '+z': [
            ('+x', 0, 0),
            ('+x', 0, 1),
            ('+x', 0, 2),
            ('+y', 0, 0),
            ('+y', 0, 1),
            ('+y', 0, 2),
            ('-x', 0, 0),
            ('-x', 0, 1),
            ('-x', 0, 2),
            ('-y', 0, 0),
            ('-y', 0, 1),
            ('-y', 0, 2),
            ] ,
        '-z': [
            ('+x', 2, 2),
            ('+x', 2, 1),
            ('+x', 2, 0),
            ('+y', 2, 2),
            ('+y', 2, 1),
            ('+y', 2, 0),
            ('-x', 2, 2),
            ('-x', 2, 1),
            ('-x', 2, 0),
            ('-y', 2, 2),
            ('-y', 2, 1),
            ('-y', 2, 0),
            ],
        '+x':[
            ('+z', 0, 0),
            ('+z', 1, 0),
            ('+z', 2, 0),
            ('+y', 0, 0),
            ('+y', 1, 0),
            ('+y', 2, 0),
            ('-z', 0, 0),
            ('-z', 1, 0),
            ('-z', 2, 0),
            ('-y', 0, 0),
            ('-y', 1, 0),
            ('-y', 2, 0),
            ],
        '-x':[
            ('-z', 0, 2),
            ('-z', 1, 2),
            ('-z', 2, 2),
            ('-y', 0, 2),
            ('-y', 1, 2),
            ('-y', 2, 2),
            ('+z', 0, 2),
            ('+z', 1, 2),
            ('+z', 2, 2),
            ('+y', 0, 2),
            ('+y', 1, 2),
            ('+y', 2, 2),
            ],
        '+y':[
            ('+z', 0, 0),
            ('+z', 1, 0),
            ('+z', 2, 0),
            ('+x', 0, 0),
            ('+x', 1, 0),
            ('+x', 2, 0),
            ('-z', 0, 0),
            ('-z', 1, 0),
            ('-z', 2, 0),
            ('-x', 0, 0),
            ('-x', 1, 0),
            ('-x', 2, 0),
            ],
        '-y':[
            ('+z', 0, 2),
            ('+z', 1, 2),
            ('+z', 2, 2),
            ('+x', 0, 2),
            ('+x', 1, 2),
            ('+x', 2, 2),
            ('-z', 0, 2),
            ('-z', 1, 2),
            ('-z', 2, 2),
            ('-x', 0, 2),
            ('-x', 1, 2),
            ('-x', 2, 2),
            ],
        }

    def __init__(self):
        self.sides = [color for color in self.COLORS for _ in range(9)]

        #random.shuffle(self.sides)


    def label(self, face, x, y):
        offset = self.OFFSET
        return self.sides[offset[face]*9+x*3+y]

    def set_label(self, face, x, y, color):
        offset = self.OFFSET

        self.sides[offset[face]*9+x*3+y] = color

    def rotate(self, face, lr):
        pebbles = None
        if lr == 'l':
            pebbles = list(self.FACE_LEFT)
        elif lr == 'r':
            pebbles = list(reversed(self.FACE_LEFT))

        adj = [self.label(face, x, y) for x, y in pebbles]

        pebbles = pebbles[2:] + pebbles[:2]

        for color, xy in zip(adj, pebbles):
            x, y = xy
            self.set_label(face, x, y, color)

        pebbles = None
        if lr == 'l':
            pebbles = list(self.ADJ_LEFT[face])
        elif lr == 'r':
            pebbles = list(reversed(self.ADJ_LEFT[face]))

        adj = [self.label(axis, x, y) for axis, x, y in pebbles]

        pebbles = pebbles[3:] + pebbles[:3]

        for color, ax_xy in zip(adj, pebbles):
            ax, x, y = ax_xy
            self.set_label(ax, x, y, color)


def draw(painter, cube, pers):
    from PySide6 import QtWidgets, QtCore, QtGui

    MARGIN = 50
    SQSIZE= 40

    if pers[0] > 0:
        face = "+x"
    if pers[1] > 0:
        face = "+y"
    if pers[2] > 0:
        face = "+z"
    if pers[0] < 0:
        face = "-x"
    if pers[1] < 0:
        face = "-y"
    if pers[2] < 0:
        face = "-z"

    painter.drawText(200, 15, face)

    for i in range(3):
        for j in range(3):
            color = cube.label(face, i, j)
            painter.setBrush(QtGui.QColor(HEX_COLORS[color]))
            painter.drawRect(MARGIN+i*SQSIZE, MARGIN+j*SQSIZE, SQSIZE, SQSIZE)
