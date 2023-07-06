from PyQt5.QtWidgets import QApplication, QWidget
import sys

class Window(QWidget):
    def __int__(self):
        super().__init__()



app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())