import os
import openpyxl
import math
from cable_classes import *


def get_cable_pull_sheet():
    # Provide the path to the folder containing the Cable Pull Sheet
    folder_path = r'C:\Users\roneill\Documents\CRO'

    # Iterate over files in the file explorer
    for file_name in os.listdir(folder_path):
        # Check if the file is an Excel file
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Check if the file name is "Messenger Cable Sizes"
            if file_name == 'Cable Sizes.xlsx':
                get_cable_sizes()
                continue  # Skip this file and move to the next file

            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)

            # Load the Excel file
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Print the sheet names
            print(f"File: {file_name}")
            print("Sheet Names:")
            for sheet_name in workbook.sheetnames:
                print(sheet_name)

    # Initialize variables to store relevant column indices
    # This is done because the formatting of pull sheets can vary
    pull_number_col_index = -1
    stationing_start_col_index = -1
    stationing_end_col_index = -1
    cable_size_col_index = -1
    express_col_index = -1

    # Iterate over the column headers in the first row
    for column_index in range(1, sheet.max_column + 1):
        header = sheet.cell(row=1, column=column_index).value
        if header:
            # Convert the header to lowercase for case-insensitive matching
            header = header.lower()

            # Check if the header contains the keywords
            if 'pull' in header:
                pull_number_col_index = column_index
            elif 'stationing' in header:
                if 'start' in header:
                    stationing_start_col_index = column_index
                elif 'end' in header:
                    stationing_end_col_index = column_index
            elif 'size' in header:
                cable_size_col_index = column_index
            elif 'express' in header:
                express_col_index = column_index

    # Print the identified column indices
    print("Pull Column Index:", pull_number_col_index)
    print("Stationing Start Column Index:", stationing_start_col_index)
    print("Stationing End Column Index:", stationing_end_col_index)
    print("Cable Size Column Index:", cable_size_col_index)
    print("Express Column Index:", express_col_index)
    print()

    # Iterate over the rows to extract information from relevant columns
    # Iterate over the rows to extract information from relevant columns
    for row in sheet.iter_rows(min_row=2):
        pull_number = sheet.cell(row=row[0].row,
                                 column=pull_number_col_index).value if pull_number_col_index != -1 else None
        stationing_start = sheet.cell(row=row[0].row,
                                      column=stationing_start_col_index).value if stationing_start_col_index != -1 else None
        stationing_end = sheet.cell(row=row[0].row,
                                    column=stationing_end_col_index).value if stationing_end_col_index != -1 else None
        cable_size = sheet.cell(row=row[0].row,
                                column=cable_size_col_index).value if cable_size_col_index != -1 else None
        express = sheet.cell(row=row[0].row,
                             column=express_col_index).value if express_col_index != -1 else None

        cable = Cable(pull_number, stationing_start, stationing_end, express, cable_size)
        cable_list.append(cable)

    for cable in cable_list:
        print("Pull Number:", cable.pull_number)
        print("Stationing Start:", cable.stationing_start)
        print("Stationing End:", cable.stationing_end)
        print("Cable Size:", cable.express)
        print("Express:", cable.cable_size)
        print()


def get_cable_sizes():
    # Provide the path to the folder containing the Cable Pull Sheet
    file_path = r'C:\Users\roneill\Documents\CRO\Cable Sizes.xlsx'

    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Iterate over the rows starting from the second row
    for row in sheet.iter_rows(min_row=2, values_only=True):
        # Extract the cable parameters from each row
        size = row[0]
        diameter = row[1]
        pounds_per_foot = row[2]
        cross_sectional_area = round(math.pi * (diameter/2) ** 2, 2)

        # Create a CableParameters object and append it to the list
        cable = CableParameters(size, diameter, pounds_per_foot, cross_sectional_area)
        cable_sizes.append(cable)

    # Close the workbook
    workbook.close()

    # Access the parameters of a cable
    for cable in cable_sizes:
        print("Size:", cable.size)
        print("Diameter:", cable.diameter)
        print("Cable Weight:", cable.pounds_per_foot)
        print("Cross Sectional Area:", cable.cross_sectional_area)
        print()


def generate_output_file():
    print("Output file going to be generated")
    global stationing_values

    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    print("appended")

    # Write the stationing sections and cables into the Excel file
    for section, cables in stationing_values.items():
        # Write the section header
        sheet.append([f"Between {section[0]} and {section[1]}:"])

        # Write the cable pull numbers
        for cable in cables:
            sheet.append([cable])

        # Add an empty row between sections
        sheet.append([])

    # Save the workbook to a file
    workbook.save("stationing_sections.xlsx")

    print("Output file generated")
