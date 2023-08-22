import os
import openpyxl
import math
from cable_classes import *


def get_cable_sizes():
    # Provide the path to the folder containing the Cable Pull Sheet
    file_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1\Code\Git Files\Cable-Run-Optimizer\Cable Sizes.xlsx'

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


def get_cable_pull_sheet():
    # Provide the path to the folder containing the Cable Pull Sheet
    folder_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1\Code\Git Files\Cable-Run-Optimizer'

    # Iterate over files in the file explorer
    for file_name in os.listdir(folder_path):
        # Check if the file is an Excel file
        if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
            # Check if the file name is "Messenger Cable Sizes"
            if file_name == 'Cable Sizes.xlsx':
                continue  # Skip this file and move to the next file

            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)

            # Load the Excel file
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active

            # Print the sheet names
            # print(f"File: {file_name}")
            # print("Sheet Names:")
            # for sheet_name in workbook.sheetnames:
            #     print(sheet_name)
            # print()

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
            elif 'start' in header or 'from' in header:
                stationing_start_col_index = column_index
            elif 'end' in header or 'to' in header:
                stationing_end_col_index = column_index
            elif 'size' in header:
                cable_size_col_index = column_index
            elif 'express' in header:
                express_col_index = column_index

    # # Print the identified column indices
    # print("Pull # Column Index:", pull_number_col_index)
    # print("Stationing Start Column Index:", stationing_start_col_index)
    # print("Stationing End Column Index:", stationing_end_col_index)
    # print("Cable Size Column Index:", cable_size_col_index)
    # print("Express Column Index:", express_col_index)
    # print()

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

    #     cable = Cable(str(pull_number), stationing_start, stationing_end, cable_size, express)
    #     cable_list.append(cable)

        # Modify stationing values
        if stationing_start is not None:
            stationing_start = int(stationing_start.replace('+', ''))
        if stationing_end is not None:
            stationing_end = int(stationing_end.replace('+', ''))

        # Find the corresponding CableParameters object based on the cable size
        # Initialize a variable to store cable information
        cable_info = None
        # Iterate through the list of cable size information
        for info in cable_sizes:
            # Check if the cable size matches the size of the current cable object
            if info.size == cable_size:
                # If a match is found, store the cable size information
                cable_info = info
                # Exit the loop since we found the relevant cable size
                break
        # print(pull_number)
        # print(stationing_start)
        # print(stationing_end)
        # print(cable_size)
        # print(express)
        # print(cable_info.diameter)
        # print(cable_info.pounds_per_foot)
        # print(cable_info.cross_sectional_area)
        # Create the Cable object with associated cable_info
        if cable_info is not None:
            # print(pull_number)
            cable = Cable(
                str(pull_number),
                int(stationing_start),
                int(stationing_end),
                cable_size,
                express,
                cable_info.diameter,
                cable_info.pounds_per_foot,
                cable_info.cross_sectional_area
            )
            cable_list.append(cable)


    print("Cable Pull Sheet:")
    for cable in cable_list:
        print(
            f"Pull Number: {cable.pull_number:<10} Stationing Start: {cable.stationing_start:<10} Stationing End: {cable.stationing_end:<10} Cable Size: {cable.cable_size:<10} Express: {cable.express:<10} Diameter: {cable.diameter:<10} Weight: {cable.weight:<10} Cross Sectional Area: {cable.cross_sectional_area:<10}")
    print()
    print("CABLE PULL SHEET OBTAINED")


# Take the stationing from pull sheet and
# organize it into a numerically ordered list,
# where duplicate values are removed
def sort_stationing():
    global stationing_values

    # Create a set to store unique stationing values
    unique_stationing_values = set()

    for cable in cable_list:
        if cable.stationing_start:
            unique_stationing_values.add(cable.stationing_start)

        if cable.stationing_end:
            unique_stationing_values.add(cable.stationing_end)

    # Convert the set to a list and sort it numerically
    stationing_values = sorted(list(unique_stationing_values))

    print("Stationing Values: ")
    for value in stationing_values:
        print(f"{str(value)[:-2]}+{str(value)[-2:]}")


# def generate_output_file():
#     print("Generating output file...")
#
#     # Create a new workbook and select the active sheet
#     workbook = openpyxl.Workbook()
#     sheet = workbook.active
#
#     # Set column headers
#     headers = [
#         "Conduit Name",
#         "Cable Pull Numbers",
#         "Stationing Start",
#         "Stationing End",
#         "Cable Size",
#         "Express",
#         "Diameter",
#         "Weight",
#         "Cross Sectional Area"
#     ]
#     sheet.append(headers)
#
#     # Write conduit data and cable attributes to the Excel file
#     for conduit_name, conduit in conduits.items():
#         for cable in conduit.cables:
#             row_data = [
#                 conduit_name,
#                 cable.pull_number,
#                 f"{str(cable.stationing_start)[:-2]}+{str(cable.stationing_start)[-2:]}",
#                 f"{str(cable.stationing_end)[:-2]}+{str(cable.stationing_end)[-2:]}",
#                 cable.cable_size,
#                 cable.express,
#                 cable.diameter,
#                 cable.weight,
#                 cable.cross_sectional_area
#             ]
#             sheet.append(row_data)
#
#     # Merge cells for conduit names and align them to the middle
#     current_conduit = None
#     start_merge_row = 2
#     for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1):
#         conduit_cell = row[0]
#         if conduit_cell.value != current_conduit:
#             if current_conduit is not None:
#                 end_merge_row = conduit_cell.row - 1
#                 merged_range = f"A{start_merge_row}:A{end_merge_row}"
#                 sheet.merge_cells(merged_range)
#                 for row_num in range(start_merge_row, end_merge_row + 1):
#                     cell = sheet[f"A{row_num}"]
#                     cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
#             current_conduit = conduit_cell.value
#             start_merge_row = conduit_cell.row
#
#     # Merge the last set of cells and align them to the middle
#     end_merge_row = sheet.max_row
#     merged_range = f"A{start_merge_row}:A{end_merge_row}"
#     sheet.merge_cells(merged_range)
#     for row_num in range(start_merge_row, end_merge_row + 1):
#         cell = sheet[f"A{row_num}"]
#         cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
#
#     # Set column width to fit the text in each header
#     for col_num, header in enumerate(headers, start=1):
#         col_letter = openpyxl.utils.get_column_letter(col_num)
#         column_width = max(len(header), max(len(str(cell.value)) for cell in sheet[col_letter]))
#         sheet.column_dimensions[col_letter].width = column_width + 2  # Adding some extra width for padding
#
#     # Save the workbook to a file
#     output_filename = "Output File.xlsx"
#     workbook.save(output_filename)
#     print(f"Conduit data has been saved to {output_filename}")
#
#     print("Output file generated")

def generate_output_file():
    print("Generating output file...")

    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set column headers
    headers = [
        "Conduit Name",
        "Stationing Start",
        "Stationing End",
        "Cable Pull Numbers",
        "Cable Size",
        "Express",
        "Diameter",
        "Weight",
        "Cross Sectional Area"
    ]
    sheet.append(headers)

    # Write conduit data and cable attributes to the Excel file
    for conduit_name, conduit in conduits.items():
        stationing_start = conduit.stationing_start
        stationing_end = conduit.stationing_end

        for cable in conduit.cables:
            row_data = [
                conduit_name,
                f"{str(stationing_start)[:-2]}+{str(stationing_start)[-2:]}",
                f"{str(stationing_end)[:-2]}+{str(stationing_end)[-2:]}",
                cable.pull_number,
                cable.cable_size,
                cable.express,
                cable.diameter,
                cable.weight,
                cable.cross_sectional_area
            ]
            sheet.append(row_data)

    # Merge cells for conduit names and align them to the middle
    current_conduit = None
    start_merge_row = 2
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1):
        conduit_cell = row[0]
        if conduit_cell.value != current_conduit:
            if current_conduit is not None:
                end_merge_row = conduit_cell.row - 1
                merged_range = f"A{start_merge_row}:A{end_merge_row}"
                sheet.merge_cells(merged_range)
                for row_num in range(start_merge_row, end_merge_row + 1):
                    cell = sheet[f"A{row_num}"]
                    cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")
            current_conduit = conduit_cell.value
            start_merge_row = conduit_cell.row

    # Merge the last set of cells and align them to the middle
    end_merge_row = sheet.max_row
    merged_range = f"A{start_merge_row}:A{end_merge_row}"
    sheet.merge_cells(merged_range)
    for row_num in range(start_merge_row, end_merge_row + 1):
        cell = sheet[f"A{row_num}"]
        cell.alignment = openpyxl.styles.Alignment(horizontal="center", vertical="center")

    # Set column width to fit the text in each header
    for col_num, header in enumerate(headers, start=1):
        col_letter = openpyxl.utils.get_column_letter(col_num)
        column_width = max(len(header), max(len(str(cell.value)) for cell in sheet[col_letter]))
        sheet.column_dimensions[col_letter].width = column_width + 2  # Adding some extra width for padding

    # Save the workbook to a file
    output_filename = "Output File.xlsx"
    workbook.save(output_filename)
    print(f"Conduit data has been saved to {output_filename}")

    print("Output file generated")
