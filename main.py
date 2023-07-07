from file_handler import obtain_cable_data
from messenger_algorithm import sort_stationing
from messenger_algorithm import stationing_sections
from PyQt5.QtWidgets import QApplication, QWidget
import sys

# obtain_cable_data()
# sort_stationing()
# stationing_sections()
# generate_output_file()

# print("Cable info")
# print(cable_list[0].pull_number)

app = QApplication(sys.argv)

window = QWidget()

window.show()
sys.exit(app.exec_())
