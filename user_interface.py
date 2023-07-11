import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, \
    QFileDialog, QTabWidget, QRadioButton, QGroupBox, QMessageBox
from PyQt5.QtGui import QIcon


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cable Run Optimizer")
        self.setWindowIcon(QIcon("TCE Logo.png"))

        # Set the initial window size
        self.resize(800, 600)

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
        QMessageBox.information(self, "Optimized Results", "Optimized Results Generated")

        # Close the UI
        self.close()


def user_interface():
    app = QApplication(sys.argv)
    window = UI()
    window.show()
    sys.exit(app.exec_())
