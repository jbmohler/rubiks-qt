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

        self.north = (0, 10, 0)
        self.perspective = (10, 10, 10)

        self.engine = get_load()
        self.cube = self.engine.Rubiks()

    def navigate(self, direction):
        self.perspective, self.north = self.engine.navigate(self.perspective, self.north, direction)

        self.update()

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Up:
            self.navigate('north')
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Down:
            self.navigate('south')
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Right:
            self.navigate('east')
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Left:
            self.navigate('west')

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
        self.layout = QtWidgets.QHBoxLayout(self.tiles)

        self.rubix1 = QRubix()
        self.rubix2 = QRubix()

        self.rubix2.cube = self.rubix1.cube
        self.rubix2.perspective = (-5, -8, -8)
        self.rubix2.north = (0, -10, 0)

        self.layout.addWidget(self.rubix1)
        self.layout.addWidget(self.rubix2)

        self.setCentralWidget(self.tiles)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.reset)
        self.timer.start()

        #self.index = 0
        #self._pers = [(10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)]

        self.ops = list(reversed([
                ('+y', 'l'),
                ('+z', 'r'),
                ('+y', 'r'),
                ('+z', 'l'),
                ]*6))
        """self.ops = list(reversed([
                ('+z', 'r'),
                ('+y', 'r'),
                ('+z', 'l'),
                ('-y', 'l'),
                ('+z', 'r'),
                ('+y', 'l'),
                ('+z', 'l'),
                ('-y', 'r'),
                ]))"""
        #self.ops = self.ops[:4]

    def keyPressEvent(self, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_X:
            print('done')
            self.timer.stop()

    def reset(self):
        #self.index = (self.index + 1) % 6
        #self.perspective = self._pers[self.index]

        if len(self.ops) > 0:
            face, lr = self.ops.pop()
            print(face, lr)
            self.rubix1.cube.rotate(face, lr)

        self.rubix1.update()
        self.rubix2.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = QRubixFrame()
    w.show()
    app.exec()
