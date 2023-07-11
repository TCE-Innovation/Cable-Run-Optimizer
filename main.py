from file_handler import obtain_cable_data
from messenger_algorithm import sort_stationing
from messenger_algorithm import stationing_sections
from PyQt5.QtWidgets import QApplication, QWidget
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFileDialog, QTabWidget, QRadioButton, QGroupBox, QMessageBox
from user_interface import user_interface

# obtain_cable_data()
# sort_stationing()
# stationing_sections()
# generate_output_file()

# print("Cable info")
# print(cable_list[0].pull_number)


user_interface()