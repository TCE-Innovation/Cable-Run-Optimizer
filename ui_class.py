from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cable Run Optimizer")
        self.setWindowIcon(QIcon("TCE Logo.png"))
        # self.setFixedHeight(400)
        # self.setFixedWidth(400)
        self.setGeometry(500,300, 400, 300) # x,y,width,height
        self.setStyleSheet("background-color: #728bbe;")


app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec_())
