import traceback
import importlib
from PySide6 import QtWidgets, QtCore, QtGui

import rubiks

def get_load():
    return importlib.reload(rubiks)

class QRubix(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QRubix, self).__init__()

        self.setMinimumSize(300, 300)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.reset)
        self.timer.start()

        self.index = 0
        self._pers = [(10, 0, 0), (0, 10, 0), (0, 0, 10), (-10, 0, 0), (0, -10, 0), (0, 0, -10)]

        self.north = (0, 10, 0)
        self.perspective = (10, -10, 10)

        self.engine = get_load()
        self.cube = self.engine.Rubiks()

    def reset(self):
        #self.index = (self.index + 1) % 6
        #self.perspective = self._pers[self.index]

        self.cube.rotate('-z', 'r')

        self.update()

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

        self.rubix = QRubix()
        self.setCentralWidget(self.rubix)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = QRubixFrame()
    w.show()
    app.exec()
