import sys
import pandas as pd
# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
#     QFileDialog, QTabWidget, QRadioButton, QGroupBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cable Run Optimizer")
        self.setWindowIcon(QIcon("TCE Logo.png"))
        layout = QVBoxLayout()

        # Create a group box for the radio buttons
        radio_group_box = QGroupBox("Select Cable Run Type")
        radio_layout = QVBoxLayout()

        self.messenger_radio = QRadioButton("Messenger")
        radio_layout.addWidget(self.messenger_radio)

        self.conduit_radio = QRadioButton("Conduit")
        radio_layout.addWidget(self.conduit_radio)

        radio_group_box.setLayout(radio_layout)

        layout.addWidget(radio_group_box)

        upload_button = QPushButton("Upload Pull Sheet")
        upload_button.clicked.connect(self.upload_file)
        layout.addWidget(upload_button)

        self.filtered_tab_widget = QTabWidget()
        layout.addWidget(self.filtered_tab_widget)

        self.full_tab_widget = QTabWidget()
        layout.addWidget(self.full_tab_widget)

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


app = QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec_())
