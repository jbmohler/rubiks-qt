import traceback
import importlib
from PySide6 import QtWidgets, QtCore, QtGui

import rubiks


def get_load():
    return importlib.reload(rubiks)


class QRubix(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QRubix, self).__init__()

        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMinimumSize(500, 500)

        self.engine = get_load()

        self.north = (0, 10, 0)
        self.perspective = (10, 10, 10)

        self.perspective, self.north = self.engine.norm_north(
            self.perspective, self.north
        )

        self.cube = self.engine.Rubiks()

        self.ops = self.cube.scramble()

    def navigate(self, direction):
        self.perspective, self.north = self.engine.navigate(
            self.perspective, self.north, direction
        )

        self.update()

    def keyPressEvent(self, event):
        is_key_press = event.type() == QtCore.QEvent.KeyPress
        if is_key_press and event.key() == QtCore.Qt.Key_Up:
            self.navigate("north")
        if is_key_press and event.key() == QtCore.Qt.Key_Down:
            self.navigate("south")
        if is_key_press and event.key() == QtCore.Qt.Key_Right:
            self.navigate("east")
        if is_key_press and event.key() == QtCore.Qt.Key_Left:
            self.navigate("west")

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        try:
            self.engine.draw(qp, self.cube, self.perspective, self.north)
        except Exception as e:
            traceback.print_exc()

        qp.end()


class QRubixFrame(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QRubixFrame, self).__init__()

        self.tiles = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout(self.tiles)

        self.rubix_views = [QRubix() for _ in range(8)]

        import itertools

        corners = itertools.product([-1, 1], [-1, 1], [-1, 1])

        for index, rbx in enumerate(self.rubix_views):
            if index != 0:
                rbx.cube = self.rubix_views[0].cube

            x, y, z = next(corners)
            rbx.perspective = (x * 5, y * 5, z * 5)
            rbx.north = (x * 5, y * 5 + 3, z * 5)

        self.ops = [
            (face, "l" if lr == "r" else "r") for face, lr in self.rubix_views[0].ops
        ]

        self.layout.addWidget(self.rubix_views[0], 0, 0)
        self.layout.addWidget(self.rubix_views[1], 1, 0)
        self.layout.addWidget(self.rubix_views[2], 2, 0)
        self.layout.addWidget(self.rubix_views[3], 0, 1)
        self.layout.addWidget(self.rubix_views[4], 2, 1)
        self.layout.addWidget(self.rubix_views[5], 0, 2)
        self.layout.addWidget(self.rubix_views[6], 1, 2)
        self.layout.addWidget(self.rubix_views[7], 2, 2)

        self.setCentralWidget(self.tiles)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.reset)

        QtCore.QTimer.singleShot(1000, self.start)

        # self.index = 0
        # self._pers = [(10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)]

        """
        self.ops = list(reversed([
                ('+y', 'l'),
                ('+z', 'r'),
                ('+y', 'r'),
                ('+z', 'l'),
                ]*6))
        self.ops = list(reversed([
                ('+z', 'r'),
                ('+y', 'r'),
                ('+z', 'l'),
                ('-y', 'l'),
                ('+z', 'r'),
                ('+y', 'l'),
                ('+z', 'l'),
                ('-y', 'r'),
                ]))
        #self.ops = self.ops[:4]

        self.ops = []
        for direction in '-+':
            for ax in 'zyx':
                face = f'{direction}{ax}'
                self.ops.append((face, 'l'))
                self.ops.append((face, 'r'))
                #if not self.cube.is_solved():
                #    raise RuntimeError(f'one of the action of {face} solved')
        self.ops = [
            ('+z', 'l'),
            ('+x', 'l'), 
            ('-x', 'l'),
        ]
        self.ops = []
                """

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_X:
            print("done")
            self.timer.stop()

    def start(self):
        self.timer.setInterval(500)
        self.timer.start()

    def reset(self):
        # self.index = (self.index + 1) % 6
        # self.perspective = self._pers[self.index]

        if len(self.ops) > 0:
            face, lr = self.ops.pop()
            print(face, lr)
            self.rubix_views[0].cube.rotate(face, lr)

        for rbx in self.rubix_views:
            rbx.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = QRubixFrame()
    w.show()
    app.exec()
