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

    def __init__(self):
        self.sides = [color for color in self.COLORS for _ in range(9)]

        random.shuffle(self.sides)

    def label(self, axis, x, y):
        offset = {
                '+x': 0,
                '+y': 1,
                '-x': 2,
                '-y': 3,
                '+z': 4,
                '-z': 5}

        return self.sides[offset[axis]*9+x*3+y]

def draw(painter, cube):
    from PySide6 import QtWidgets, QtCore, QtGui

    MARGIN = 50
    SQSIZE= 40

    for i in range(3):
        for j in range(3):
            color = cube.label('+x', i, j)
            painter.setBrush(QtGui.QColor(HEX_COLORS[color]))
            painter.drawRect(MARGIN+i*SQSIZE, MARGIN+j*SQSIZE, SQSIZE, SQSIZE)
