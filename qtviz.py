from PySide6 import QtWidgets, QtCore
import traceback

def get_load():
    exec('import rubix')
    return rubix

class QRubix(QWidget):
    def __init__(self, parent=None):
        super(QRubix, self).__init__()

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


class QRubixFrame(QMainWindow):
    def __init__(self, parent=None):
        super(QRubixFrame, self).__init__()

        self.rubix = QRubix()
        self.setCentralWidget(self.rubix)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = QRubixFrame()
    w.show()
    app.exec_()
