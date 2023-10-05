###############
#### Local ####
###############
import os
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
import math
from cable_classes import *
import subprocess

###############
#### Server ###
###############
'''
import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment, Font
import math
from io import BytesIO
from .cable_classes import *
import logging
from .azure import upload_to_azure
'''


###############
#### Local ####
###############
# Extract the diameter and weight of all cables from Cable Sizes.xlsx
def get_cable_sizes():  # Local function
    print("[STATUS] Fetching cable sizes...")

    # Path to the folder containing the Cable Pull Sheet
    file_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1' \
                r'\Code\Git Files\Cable-Run-Optimizer\Cable Sizes.xlsx'

    # Load the Excel file
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Initialize variables to track the special case
    special_case = False
    first_row_skipped = False  # Flag to skip the first row when in the special case
    length = None
    width = None

    # Iterate over the rows starting from the second row
    # First row has headers, not cable data, so don't scan those
    for row in sheet.iter_rows(min_row=2, values_only=True):

        # Check to see if the file scanner has reached the section with 2 conductor cables
        if row[0] == "* 2 Conductor Cables Below *":
            special_case = True     # Set flag to move onto headers of 2 conductor cables
            continue                # Skip this iteration of the loop, to move onto the headers of 2 conductor cables
        # If at the headers of the 2 conductor cables
        # Skip the iteration of the for loop to avoid scanning in header titles
        if special_case:
            if not first_row_skipped:
                first_row_skipped = True
                continue  # Skip the first row

            # Reading in data for 2 conductor cables
            size = row[0]
            length = row[1]
            width = row[2]
            weight = row[3]

            # Calculate the cross-sectional area as the product of length and width
            # 2 conductor cables are approximated as rectangles
            cross_sectional_area = length * width

            # Create a CableParameters object with diameter set to "None" and add to cable sizes list
            cable = CableParameters(size, None, weight, cross_sectional_area)
            cable_sizes_list.append(cable)
        # For all cables other than 2 conductor cables
        else:
            # Extract the cable parameters as usual
            size = row[0]
            diameter = row[1]
            pounds_per_foot = row[2]
            cross_sectional_area = round(math.pi * ((diameter / 2) ** 2), 4)  # Area of circle

            # Create a CableParameters object and append it to the list
            cable = CableParameters(size, diameter, pounds_per_foot, cross_sectional_area)
            cable_sizes_list.append(cable)

    # Close the Excel workbook
    workbook.close()

    print("[PASS] Cable sizes acquired.\n")


###############
#### Server ###
###############
# Extract the diameter and weight of all cables from Cable Sizes.xlsx
'''
def get_cable_sizes(cable_sizes):
    try:
        # Load the Excel file
        workbook = openpyxl.load_workbook(BytesIO(cable_sizes.read()))
        sheet = workbook.active
        
        # Initialize variables to track the special case
        special_case = False
        first_row_skipped = False  # Flag to skip the first row when in the special case
        length = None
        width = None

        # Iterate over the rows starting from the second row (second because first row has the headers)
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Check for the special case
            if row[0] == "* 2 Conductor Cables Below *":
                special_case = True
                continue  # Skip this row

            if special_case:
                if not first_row_skipped:
                    first_row_skipped = True
                    continue  # Skip the first row

                # This is the special case, so process the data differently
                size = row[0]
                length = row[1]
                width = row[2]
                weight = row[3]

                print(length)
                print(width)

                # Calculate the cross-sectional area as the product of length and width
                cross_sectional_area = length * width

                # Create a CableParameters object with diameter set to "None"
                cable = CableParameters(size, None, weight, cross_sectional_area)
                cable_sizes_list.append(cable)

            else:
                # Extract the cable parameters as usual
                size = row[0]
                diameter = row[1]
                pounds_per_foot = row[2]
                cross_sectional_area = round(math.pi * ((diameter / 2) ** 2), 4)

                # Create a CableParameters object and append it to the list
                cable = CableParameters(size, diameter, pounds_per_foot, cross_sectional_area)
                cable_sizes_list.append(cable)

        # Close the workbook
        workbook.close()

    except openpyxl.utils.exceptions.InvalidFileException:
        # Handle the case where the file cannot be opened (invalid Excel file)
        logging.info("Invalid Excel file or sheet")
    except Exception as e:
        # Handle other exceptions
        logging.info(f"An error occurred: {str(e)}")
'''


# Open cable pull sheet and extract all the cables and their info from it
# def get_cable_pull_sheet(pull_sheet): # Server function
def get_cable_pull_sheet(): # Local function
    print("[STATUS] Fetching cable pull sheet...")
    ###############
    #### Local ####
    ###############
    # Path to the folder containing the Cable Pull Sheet
    folder_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1' \
                  r'\Code\Git Files\Cable-Run-Optimizer'

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


    ###############
    #### Server ###
    ###############
    '''
    # Open cable pull sheet and extract all the cables and their info from it
    def get_cable_pull_sheet(pull_sheet):
        # Load the Excel file
        workbook = openpyxl.load_workbook(BytesIO(pull_sheet.read()))
        sheet = workbook.active
    '''

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

        # Modify stationing values
        if stationing_start is not None:
            stationing_start = int(stationing_start.replace('+', ''))
        if stationing_end is not None:
            stationing_end = int(stationing_end.replace('+', ''))

        # Find the corresponding CableParameters object based on the cable size
        # Initialize a variable to store cable information
        cable_info = None
        # Iterate through the list of cable size information
        for info in cable_sizes_list:
            # Check if the cable size matches the size of the current cable object
            if info.size == cable_size:
                # If a match is found, store the cable size information
                cable_info = info
                # Exit the loop since we found the relevant cable size
                break

        if cable_info is not None:
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
    print("[PASS] Cable pull sheet obtained.\n")


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
    return stationing_values


# Create excel output file with list of conduits and which cables are in them
def generate_output_file():
    from cable_classes import conduit_sizes

    print("\n[STATUS] Generating output file...")

    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set column headers
    headers = [
        "Conduit",
        "Stationing Start",
        "Stationing End",
        "Pull #",
        "Cable Size",
        "Express",
        "Minimum Conduit Size",
        "Conduit Fill",
        "Upsized Conduit",
        "Upsized Conduit Fill"
    ]
    sheet.append(headers)

    # Write conduit data and cable attributes to the Excel file
    for conduit_name, conduit in conduits.items():

        conduit_sizes_index = next((index for index, x in enumerate(conduit_sizes) if x == conduit.conduit_size), None)

        for cable in conduit.cables:
            row_data = [
                f"Conduit {conduit.conduit_number}",                                                                   # Conduit name
                f"{str(conduit.stationing_start)[:-2]}+{str(conduit.stationing_start)[-2:]}",   # Stationing start
                f"{str(conduit.stationing_end)[:-2]}+{str(conduit.stationing_end)[-2:]}",       # Stationing end
                int(cable.pull_number),                 # Pull Number
                cable.cable_size,                       # Cable size (ex. 7C#14)
                cable.express,                          # Express or local
                conduit.conduit_size,                   # Conduit size in inches
                str(conduit.conduit_fill) + "%",             # f"{round((100 - conduit_free_air_space), 2)}%",   # Conduit fill
                conduit_sizes[conduit_sizes_index + 1], # Upsized conduit
                f"{(100 * conduit.conduit_area / (math.pi * ((conduit_sizes[conduit_sizes_index + 1] / 2) ** 2))):.2f}%" # Upsized conduit fill
            ]
            sheet.append(row_data)

    # Set column width to fit the text in each header
    for col_num, header in enumerate(headers, start=1):
        col_letter = openpyxl.utils.get_column_letter(col_num)
        column_width = max(len(header), max(len(str(cell.value)) for cell in sheet[col_letter]))
        sheet.column_dimensions[col_letter].width = column_width + 2  # Adding some extra width for padding

    # Apply bold font to the header row
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    # Dictionary to store counts for each conduit name
    conduit_counts = {}

    # Count the occurrences of each conduit name
    for row_num, row in enumerate(sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1)):
        conduit_name = row[0].value
        if conduit_name not in conduit_counts:
            conduit_counts[conduit_name] = 1
        else:
            conduit_counts[conduit_name] += 1

    # Merge cells for each conduit name and adjust Stationing Start and Stationing End columns
    for conduit_name, count in conduit_counts.items():
        start_row = None
        for row_num, row in enumerate(sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1), start=2):
            if row[0].value == conduit_name:
                if start_row is None:
                    start_row = row_num
                if count == 1:
                    continue

                if row_num - start_row + 1 == count:

                    # Define the column letters for merging and alignment
                    columns_to_merge = ['A', 'B', 'C', 'F', 'G', 'H', 'I', 'J']

                    # Loop through the columns and apply merging and alignment
                    for column in columns_to_merge:
                        column_range = f'{column}{start_row}:{column}{row_num}'
                        sheet.merge_cells(column_range)
                        sheet[f'{column}{start_row}'].alignment = Alignment(vertical='center', horizontal='center')

                    start_row = None

    # Center align cells in all columns for rows starting from the second row
    for row in sheet.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical='center', horizontal='center')

    ###############
    #### Local ####
    ###############
    # Save the workbook to a file
    output_filename = "Output File.xlsx"
    workbook.save(output_filename)

    print(f"[PASS] Output file {output_filename} has been saved.")
    print(f"[STATUS] Opening output file...")

    pdf_file_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC' \
                    r'\Documents 1\Code\Git Files\Cable-Run-Optimizer\Output File.xlsx'
    subprocess.run(["start", "", pdf_file_path], shell=True, check=True)


    
    ###############
    #### Server ###
    ###############
    '''
    # Upload the workbook to azure blob storage
    sas_url = upload_to_azure(workbook)

    print(f"Conduit data has been saved to uploaded to blob storage.")

    return sas_url
    '''
