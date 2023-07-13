# import sys
# import pandas as pd
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
#     QFileDialog, QTabWidget, QRadioButton, QGroupBox, QMessageBox
# from PyQt5.QtGui import QIcon
#
#
# class UI(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Cable Run Optimizer")
#         self.setWindowIcon(QIcon("TCE Logo.png"))
#
#         # Set the initial window size
#         self.resize(800, 600)
#
#         layout = QVBoxLayout()
#
#         # Create a group box for the radio buttons
#         radio_group_box = QGroupBox("Select Cable Run Type")
#         radio_layout = QVBoxLayout()
#
#         self.messenger_radio = QRadioButton("Messenger")
#         radio_layout.addWidget(self.messenger_radio)
#
#         self.conduit_radio = QRadioButton("Conduit")
#         radio_layout.addWidget(self.conduit_radio)
#
#         radio_group_box.setLayout(radio_layout)
#
#         layout.addWidget(radio_group_box)
#
#         upload_button = QPushButton("Upload Pull Sheet")
#         upload_button.clicked.connect(self.upload_file)
#         layout.addWidget(upload_button)
#
#         self.filtered_tab_widget = QTabWidget()
#         layout.addWidget(self.filtered_tab_widget)
#
#         self.full_tab_widget = QTabWidget()
#         layout.addWidget(self.full_tab_widget)
#
#         self.generate_results_button = QPushButton("Generate Optimized Results")
#         self.generate_results_button.clicked.connect(self.generate_optimized_results)
#         self.generate_results_button.setEnabled(False)  # Disable the button initially
#         layout.addWidget(self.generate_results_button)
#
#         self.setLayout(layout)
#
#     def upload_file(self):
#         file_dialog = QFileDialog(self)
#         file_dialog.setWindowTitle("Select File")
#         file_dialog.setFileMode(QFileDialog.ExistingFile)
#         file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")
#
#         if file_dialog.exec_() == QFileDialog.Accepted:
#             selected_file = file_dialog.selectedFiles()[0]
#
#             # Read the Excel file using pandas
#             xls = pd.ExcelFile(selected_file)
#
#             # Clear existing tabs
#             self.filtered_tab_widget.clear()
#             self.full_tab_widget.clear()
#
#             # Create tabs for each sheet
#             for sheet_name in xls.sheet_names:
#                 df = pd.read_excel(xls, sheet_name)
#
#                 # Filter columns
#                 filtered_df = df[["Pull #", "Stationing Start", "Stationing End", "Cable Size", "Local/Express"]]
#
#                 # Filtered tab
#                 filtered_table = QTableWidget()
#                 self.populate_table(filtered_table, filtered_df)
#                 self.filtered_tab_widget.addTab(filtered_table, f"{sheet_name} (Filtered)")
#
#                 # Full tab
#                 full_table = QTableWidget()
#                 self.populate_table(full_table, df)
#                 self.full_tab_widget.addTab(full_table, f"{sheet_name} (Full Sheet)")
#
#             # Enable the "Generate Optimized Results" button
#             self.generate_results_button.setEnabled(True)
#
#     def populate_table(self, table, data_frame):
#         table.clear()
#
#         # Set the number of rows and columns in the table
#         num_rows, num_columns = data_frame.shape
#         table.setRowCount(num_rows)
#         table.setColumnCount(num_columns)
#
#         # Set the headers
#         table.setHorizontalHeaderLabels(data_frame.columns)
#
#         # Populate the table with the data
#         for row in range(num_rows):
#             for column in range(num_columns):
#                 item = QTableWidgetItem(str(data_frame.iloc[row, column]))
#                 table.setItem(row, column, item)
#
#     def generate_optimized_results(self):
#         # Perform the logic to generate the optimized results Excel file
#         # Replace the following placeholder code with your actual implementation
#
#         # Write your code to generate the optimized results Excel file using the selected file data
#         # Here, you can access the selected file using its path
#         file_path = r'C:\Users\roneill\Documents\CRO\Optimized Results.xlsx'
#
#         # Generate the optimized results Excel file
#         # You can use pandas or any other library to generate the Excel file
#         # For example, using pandas:
#         data = [["Optimized Result 1"], ["Optimized Result 2"], ["Optimized Result 3"]]
#         df = pd.DataFrame(data, columns=["Optimized Results"])
#         df.to_excel(file_path, index=False)
#
#         # Show a message box with the "Optimized Results Generated" message
#         QMessageBox.information(self, "Optimized Results", "Optimized Results Generated")
#
#         # Close the UI
#         self.close()
#
#
# def user_interface():
#     app = QApplication(sys.argv)
#     window = UI()
#     window.show()
#     sys.exit(app.exec_())
import os
import openpyxl
import math
import pandas as pd
from cable_classes import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFileDialog, QTabWidget, QRadioButton, QGroupBox, QLabel, QTextEdit, QMessageBox, QHBoxLayout, QDoubleSpinBox, \
    QSplitter
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from file_handler import cable_parameters


class CableSizingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cable Sizing")
        self.setWindowIcon(QIcon("TCE Logo.png"))

        layout = QVBoxLayout()

        self.cable_parameters_table = QTableWidget()
        layout.addWidget(self.cable_parameters_table)

        self.setLayout(layout)

        # Initialize the diameter spin box list
        self.diameter_spinboxes = []

        # Update the cable parameters table
        self.update_cable_parameters()

    def update_cable_parameters(self):
        # Set the number of rows and columns in the table
        num_rows = len(cable_parameters)
        num_columns = 4  # Assuming cable parameters have four attributes: size, diameter, cable weight, and cross-sectional area

        self.cable_parameters_table.setRowCount(num_rows)
        self.cable_parameters_table.setColumnCount(num_columns)

        # Set the table headers
        headers = ["Size", "Diameter", "Cable Weight", "Area"]
        self.cable_parameters_table.setHorizontalHeaderLabels(headers)

        # Initialize the area_labels list
        self.area_labels = []

        # Populate the table with the cable parameters
        for row, cable in enumerate(cable_parameters):
            # Set the size as a label
            size_label = QLabel(cable.size)
            size_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text in the label
            self.cable_parameters_table.setCellWidget(row, 0, size_label)

            # Set the diameter as a double spin box
            diameter_spinbox = QDoubleSpinBox()
            diameter_spinbox.setMinimum(0.0)
            diameter_spinbox.setMaximum(1000.0)
            diameter_spinbox.setValue(cable.diameter)
            diameter_spinbox.setDecimals(2)
            diameter_spinbox.valueChanged.connect(lambda value, r=row: self.update_cross_sectional_area(r))
            diameter_spinbox.setAlignment(QtCore.Qt.AlignCenter)  # Center the text in the spin box
            self.diameter_spinboxes.append(diameter_spinbox)
            self.cable_parameters_table.setCellWidget(row, 1, diameter_spinbox)

            # Set the cable weight as a double spin box
            cable_weight_spinbox = QDoubleSpinBox()
            cable_weight_spinbox.setMinimum(0.0)
            cable_weight_spinbox.setMaximum(1000.0)
            cable_weight_spinbox.setValue(cable.pounds_per_foot)
            cable_weight_spinbox.setDecimals(2)
            cable_weight_spinbox.setAlignment(QtCore.Qt.AlignCenter)  # Center the text in the spin box
            self.cable_parameters_table.setCellWidget(row, 2, cable_weight_spinbox)

            # Set the cross-sectional area as a label
            cross_sectional_area = round(math.pi * (cable.diameter / 2) ** 2, 2)
            cross_sectional_area_label = QLabel(str(cross_sectional_area))
            cross_sectional_area_label.setAlignment(QtCore.Qt.AlignCenter)  # Center the text in the label
            self.cable_parameters_table.setCellWidget(row, 3, cross_sectional_area_label)

            # Add the area label to the area_labels list
            self.area_labels.append(cross_sectional_area_label)

        # Set uniform column widths
        for column in range(num_columns):
            self.cable_parameters_table.setColumnWidth(column, 95)

        # Resize the rows to fit the contents
        self.cable_parameters_table.resizeRowsToContents()

    def update_cross_sectional_area(self, row):
        diameter = self.diameter_spinboxes[row].value()
        cross_sectional_area = round(math.pi * (diameter / 2) ** 2, 2)
        self.area_labels[row].setText(str(cross_sectional_area))  # Update the text of the existing QLabel widget
        self.area_labels[row].setAlignment(QtCore.Qt.AlignCenter)  # Center the text in the label


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cable Run Optimizer")
        self.setWindowIcon(QIcon("TCE Logo.png"))

        # Set the initial window size
        self.resize(675, 600)

        layout = QVBoxLayout()

        # Create a horizontal layout for radio buttons and cable sizing window
        hbox = QHBoxLayout()

        # Create a group box for the radio buttons
        radio_group_box = QGroupBox("Select Cable Run Type")
        radio_layout = QVBoxLayout()

        self.messenger_radio = QRadioButton("Messenger")
        radio_layout.addWidget(self.messenger_radio)

        self.conduit_radio = QRadioButton("Conduit")
        radio_layout.addWidget(self.conduit_radio)

        radio_group_box.setLayout(radio_layout)

        hbox.addWidget(radio_group_box)

        # Create the cable sizing window
        self.cable_sizing_window = CableSizingWindow()
        hbox.addWidget(self.cable_sizing_window)

        # Create a splitter to adjust the size of the cable sizing window
        splitter = QSplitter()
        splitter.addWidget(radio_group_box)
        splitter.addWidget(self.cable_sizing_window)
        splitter.setSizes([100, 300])  # Adjust the initial sizes as needed

        layout.addWidget(splitter)

        upload_button = QPushButton("Upload Pull Sheet")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        self.filtered_tab_widget = QTabWidget()
        layout.addWidget(self.filtered_tab_widget)

        self.full_tab_widget = QTabWidget()
        layout.addWidget(self.full_tab_widget)

        self.generate_results_button = QPushButton("Generate Optimized Results")
        self.generate_results_button.clicked.connect(self.generate_optimized_results)
        self.generate_results_button.setEnabled(False)  # Disable the button initially
        layout.addWidget(self.generate_results_button)

        self.setLayout(layout)

    def upload_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select File")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Excel Files (*.xlsx *.xls)")

        if file_dialog.exec_() == QFileDialog.Accepted:
            selected_file = file_dialog.selectedFiles()[0]

            # Read the Excel file using pandas
            xls = pd.ExcelFile(selected_file)

            # Clear existing tabs
            self.filtered_tab_widget.clear()
            self.full_tab_widget.clear()

            # Create tabs for each sheet
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name)

                # Filter columns
                filtered_df = df[["Pull #", "Stationing Start", "Stationing End", "Cable Size", "Local/Express"]]

                # Filtered tab
                filtered_table = QTableWidget()
                self.populate_table(filtered_table, filtered_df)
                self.filtered_tab_widget.addTab(filtered_table, f"{sheet_name} (Filtered)")

                # Full tab
                full_table = QTableWidget()
                self.populate_table(full_table, df)
                self.full_tab_widget.addTab(full_table, f"{sheet_name} (Full Sheet)")

            # Enable the "Generate Optimized Results" button
            self.generate_results_button.setEnabled(True)

    def populate_table(self, table, data_frame):
        table.clear()

        # Set the number of rows and columns in the table
        num_rows, num_columns = data_frame.shape
        table.setRowCount(num_rows)
        table.setColumnCount(num_columns)

        # Set the headers
        table.setHorizontalHeaderLabels(data_frame.columns)

        # Populate the table with the data
        for row in range(num_rows):
            for column in range(num_columns):
                item = QTableWidgetItem(str(data_frame.iloc[row, column]))
                table.setItem(row, column, item)

    def generate_optimized_results(self):
        # Perform the logic to generate the optimized results Excel file
        # Replace the following placeholder code with your actual implementation

        # Write your code to generate the optimized results Excel file using the selected file data
        # Here, you can access the selected file using its path
        file_path = r'C:\Users\roneill\Documents\CRO\Optimized Results.xlsx'  # Replace with the actual file path

        # Generate the optimized results Excel file
        # You can use pandas or any other library to generate the Excel file
        # For example, using pandas:
        data = [["Optimized Result 1"], ["Optimized Result 2"], ["Optimized Result 3"]]
        df = pd.DataFrame(data, columns=["Optimized Results"])
        df.to_excel(file_path, index=False)

        # Show a message box with the "Optimized Results Generated" message
        QMessageBox.information(self, "Optimized Results", "Optimized results generated successfully.")

    def show_cable_sizing_window(self):
        self.cable_sizing_window.update_cable_parameters()
        self.cable_sizing_window.show()


def user_interface():
    app = QApplication([])
    ui = UI()
    ui.show()
    app.exec_()


user_interface()

