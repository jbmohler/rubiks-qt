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

        self.engine = get_load()
        self.cube = self.engine.Rubiks()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)

        try:
            self.engine.draw(qp, self.cube)
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
