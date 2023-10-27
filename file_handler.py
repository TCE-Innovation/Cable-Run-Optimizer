from settings import *

if local_code_flag:

    import os
    import re
    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment, Font
    import math
    from cable_classes import *
    import subprocess

    file_path = None

    # Extract the diameter and weight of all cables from Cable Sizes.xlsx
    def get_cable_sizes():
        print("[STATUS] Fetching cable sizes...")

        # Path to the folder containing the Cable Pull Sheet
        file_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1' \
                    r'\Code\Git Files\Cable-Run-Optimizer\Cable Sizes.xlsx'

        # Load the Excel file
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        cable_sizes_list = parse_cable_sizes_excel(sheet)

        # Close the Excel workbook
        workbook.close()

        print(f"[PASS] Cable sizes acquired.\n")

        return cable_sizes_list

    # Open cable pull sheet and extract all the cables and their info from it
    def get_cable_pull_sheet(cable_list, cable_sizes_list):
        # Initialize empty cable list to hold cables from pull sheet
        cable_list = []

        print("[STATUS] Fetching cable pull sheet...")
        # Updated column headers to match your fixed column format
        pull_number_col_index = 1  # Column A
        cable_size_col_index = 2  # Column B
        express_col_index = 3  # Column C
        stationing_start_col_index = 4  # Column D
        stationing_end_col_index = 5  # Column E
        distance_col_index = 6  # Column F (for absolute distances)

        # Path to the "Test Basic Pull Sheet.xlsx" file
        file_path = r'C:\Users\roneill\OneDrive - Iovino Enterprises, LLC\Documents 1' \
                    r'\Code\Git Files\Cable-Run-Optimizer\Test Basic Pull Sheet.xlsx'

        # Load the Excel file
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        # Regular expression pattern to detect stationing values (both numerical and location descriptors)
        # stationing_pattern = r'\d+\+\d+|[A-Z\-]+'

        # Iterate over the rows to extract information from relevant columns
        for row in sheet.iter_rows(min_row=2, values_only=True):
            pull_number         = row[0]
            cable_size          = row[1]
            express             = row[2]
            stationing_start    = row[3]
            stationing_end      = row[4]

            # Check if stationing_start is a numerical stationing value
            if '+' in str(stationing_start):
                # If it's a numerical stationing value, treat it as such
                absolute_distance = None
                # stationing_values_numeric.append((stationing_start, stationing_end))
            else:
                # If it's a location descriptor, check if there's an absolute distance in Column F
                absolute_distance = row[5]  # Assuming Column F contains absolute distance
                stationing_text_pairs.append((stationing_start, stationing_end))  # Log text descriptor pair

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
                    pull_number,
                    stationing_start,
                    stationing_end,
                    cable_size,
                    express,
                    cable_info.diameter,
                    cable_info.pounds_per_foot,
                    cable_info.cross_sectional_area,
                    absolute_distance
                )
                cable_list.append(cable)
        print(f"[PASS] Cable pull sheet obtained.\n")

        # Print out the cables at the end of the function
        for cable in cable_list:
            print(f"Cable: Pull #{cable.pull_number}, Size: {cable.cable_size}, Express: {cable.express}, "
                  f"Stationing Start: {cable.stationing_start}, Stationing End: {cable.stationing_end}, "
                  f"Absolute Distance: {cable.absolute_distance}")

        # Return the cable list if needed for further processing
        return cable_list


elif server_code_flag:

    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import Alignment, Font
    import math
    from io import BytesIO
    from .cable_classes import *
    import logging
    from .azure import upload_to_azure

    # Extract the diameter and weight of all cables from Cable Sizes.xlsx
    def get_cable_sizes(cable_sizes, bytes_flag):
        try:
            if bytes_flag:
                logging.info("Bytes flag is true, loading workbook from bytes.")
                workbook = openpyxl.load_workbook(BytesIO(cable_sizes))
            else:
                logging.info("Bytes flag is false, loading workbook from file.")
                workbook = openpyxl.load_workbook(BytesIO(cable_sizes.read()))

            sheet = workbook.active

            logging.info("Running parse_cable_sizes_excel function.")
            cable_sizes_list = parse_cable_sizes_excel(sheet)

            # Close the workbook
            workbook.close()

            return cable_sizes_list

        except openpyxl.utils.exceptions.InvalidFileException:
            # Handle the case where the file cannot be opened (invalid Excel file)
            logging.info("Invalid Excel file or sheet")
        except Exception as e:
            # Handle other exceptions
            logging.info(f"An error occurred: {str(e)}")

    # Open cable pull sheet and extract all the cables and their info from it
    def get_cable_pull_sheet(pull_sheet, cable_sizes_list):
        cable_list = []

        global stationing_text_pairs
        stationing_text_pairs = []

        # Load the Excel file
        workbook = openpyxl.load_workbook(BytesIO(pull_sheet.read()))
        sheet = workbook.active

        # Iterate over the rows to extract information from relevant columns
        for row in sheet.iter_rows(min_row=2, values_only=True):
            pull_number = row[0]
            cable_size = row[1]
            express = row[2]
            stationing_start = row[3]
            stationing_end = row[4]

            # Check if stationing_start is a numerical stationing value
            if '+' in str(stationing_start):
                # If it's a numerical stationing value, treat it as such
                absolute_distance = None
            else:
                # If it's a location descriptor, check if there's an absolute distance in Column F
                absolute_distance = row[5]  # Assuming Column F contains absolute distance
                stationing_text_pairs.append((stationing_start, stationing_end))  # Log text descriptor pair

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
                    pull_number,
                    stationing_start,
                    stationing_end,
                    cable_size,
                    express,
                    cable_info.diameter,
                    cable_info.pounds_per_foot,
                    cable_info.cross_sectional_area,
                    absolute_distance
                )
                cable_list.append(cable)
                logging.info("Length of cable_list: %s", len(cable_list))

        print(f"[PASS] Cable pull sheet obtained.\n")

        # Print out the cables at the end of the function
        for cable in cable_list:
            print(f"Cable: Pull #{cable.pull_number}, Size: {cable.cable_size}, Express: {cable.express}, "
                  f"Stationing Start: {cable.stationing_start}, Stationing End: {cable.stationing_end}, "
                  f"Absolute Distance: {cable.absolute_distance}")

        # Close the workbook
        workbook.close()

        # Return the cable list if needed for further processing
        return cable_list


def sort_stationing(cable_list):
    if server_code_flag:
        logging.info("Running sort_stationing function.")

    global stationing_text_pairs
    stationing_values_numeric = []

    if server_code_flag:
        logging.info("Start: stationing_text_pairs %s", stationing_text_pairs)
        logging.info("Start: stationing_values_numeric %s", stationing_values_numeric)

    # Create a set to store unique stationing values
    unique_stationing_values = set()

    if server_code_flag:
        logging.info("In sort stationing. Length of cable_list: %s", len(cable_list))

    for cable in cable_list:
        if cable.absolute_distance is None:  # Only adding numeric stationing values
            unique_stationing_values.add(cable.stationing_start)

        if cable.absolute_distance is None:  # Only adding numeric stationing values
            unique_stationing_values.add(cable.stationing_end)

    # Convert the set to a list and sort it numerically
    stationing_values_numeric = sorted(list(unique_stationing_values))

    print("[STATUS] Printing all stationing values obtained: ")
    # Print out all the stationing values
    for value in stationing_values_numeric:
        print(value)

    # Create a set to store unique stationing text pairs
    unique_stationing_text_pairs = set(stationing_text_pairs)
    stationing_text_pairs = list(unique_stationing_text_pairs)

    if server_code_flag:
        logging.info("End: stationing_text_pairs %s", stationing_text_pairs)
        logging.info("End: stationing_values_numeric %s", stationing_values_numeric)

    return stationing_values_numeric, stationing_text_pairs


def parse_cable_sizes_excel(sheet):
    # Initialize variables to track the special case
    special_case = False
    first_row_skipped = False  # Flag to skip the first row when in the special case
    length = None
    width = None

    cable_sizes_list = []

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
            cross_sectional_area = round(math.pi * ((float(diameter) / 2) ** 2), 4)

            # Create a CableParameters object and append it to the list
            cable = CableParameters(size, diameter, pounds_per_foot, cross_sectional_area)
            cable_sizes_list.append(cable)

    if server_code_flag:
       logging.info("End of parse_cable_sizes_excel. Cable sizes list length: %s", len(cable_sizes_list))

    return cable_sizes_list


def parse_cable_pull_sheet(sheet):
    pass


# Create excel output file with list of conduits and which cables are in them
def generate_output_file_for_conduit(conduits):
    if local_code_flag:
        from cable_classes import conduit_sizes
    elif server_code_flag:
        from .cable_classes import conduit_sizes

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
        "Express/Local",
        "Minimum Conduit Size (in)",
        "Conduit Fill",
        "Upsized Conduit (in)",
        "Upsized Conduit Fill"
    ]
    sheet.append(headers)

    if server_code_flag:
        logging.info("Conduit list length: %s", len(conduits))

    # Write conduit data and cable attributes to the Excel file
    for conduit_name, conduit in conduits.items():

        conduit_sizes_index = next((index for index, x in enumerate(conduit_sizes) if x == conduit.conduit_size), None)

        for cable in conduit.cables:
            row_data = [
                f"Conduit {conduit.conduit_number}",  # Conduit name
                f"{conduit.stationing_start}",  # Stationing start
                f"{conduit.stationing_end}",  # Stationing end
                int(cable.pull_number),  # Pull Number
                cable.cable_size,  # Cable size (ex. 7C#14)
                cable.express,  # Express or local
                conduit.conduit_size,  # Conduit size in inches
                str(conduit.conduit_fill) + "%",  # f"{round((100 - conduit_free_air_space), 2)}%",   # Conduit fill
                conduit_sizes[conduit_sizes_index + 1],  # Upsized conduit
                f"{(100 * conduit.conduit_area / (math.pi * ((conduit_sizes[conduit_sizes_index + 1] / 2) ** 2))):.2f}%"
                # Upsized conduit fill
            ]
            sheet.append(row_data)


    # Write bundle data and cable attributes to the Excel file
    for bundle_name, bundle in bundles.items():

        for cable in bundle.cables:
            row_data = [
                f"Conduit {bundle.bundle_number}",  # Bundle number
                f"{bundle.stationing_start}",       # Stationing start
                f"{bundle.stationing_end}",         # Stationing end
                int(cable.pull_number),             # Individual cable pull number
                cable.cable_size,                   # Cable size (ex. 7C#14)
                cable.express,                      # Express or local
                bundle.bundle_diameter,             # Bundle diameter
                bundle.bundle_weight                # Bundle weight
                # Upsized conduit fill
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

    if local_code_flag:
        # Save the workbook to a file
        output_filename = "Output File.xlsx"
        workbook.save(output_filename)

        print(f"[PASS] Output file {output_filename} has been saved.")
        print(f"[STATUS] Opening output file...")

        pdf_file_path = 'C:/Users/roneill/OneDrive - Iovino Enterprises, LLC/Documents 1/Code/Git Files/Cable-Run-Optimizer/Output File.xlsx'

        subprocess.run(["start", "", pdf_file_path], shell=True, check=True)

    elif server_code_flag:

        # Upload the workbook to azure blob storage
        sas_url = upload_to_azure(workbook)

        print(f"Conduit data has been saved to uploaded to blob storage.")

        return sas_url

    def generate_output_file_for_conduit(conduits):
        if local_code_flag:
            from cable_classes import conduit_sizes
        elif server_code_flag:
            from .cable_classes import conduit_sizes

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
            "Express/Local",
            "Minimum Conduit Size (in)",
            "Conduit Fill",
            "Upsized Conduit (in)",
            "Upsized Conduit Fill"
        ]
        sheet.append(headers)

        if server_code_flag:
            logging.info("Conduit list length: %s", len(conduits))

        if run_conduit_optimization:
            # Write conduit data and cable attributes to the Excel file
            for conduit_name, conduit in conduits.items():

                conduit_sizes_index = next(
                    (index for index, x in enumerate(conduit_sizes) if x == conduit.conduit_size), None)

                for cable in conduit.cables:
                    row_data = [
                        f"Conduit {conduit.conduit_number}",  # Conduit name
                        f"{conduit.stationing_start}",  # Stationing start
                        f"{conduit.stationing_end}",  # Stationing end
                        int(cable.pull_number),  # Pull Number
                        cable.cable_size,  # Cable size (ex. 7C#14)
                        cable.express,  # Express or local
                        conduit.conduit_size,  # Conduit size in inches
                        str(conduit.conduit_fill) + "%",
                        # f"{round((100 - conduit_free_air_space), 2)}%",   # Conduit fill
                        conduit_sizes[conduit_sizes_index + 1],  # Upsized conduit
                        f"{(100 * conduit.conduit_area / (math.pi * ((conduit_sizes[conduit_sizes_index + 1] / 2) ** 2))):.2f}%"
                        # Upsized conduit fill
                    ]
                    sheet.append(row_data)

        if run_messenger_optimization:
            # Write bundle data and cable attributes to the Excel file
            for bundle_name, bundle in bundles.items():

                for cable in bundle.cables:
                    row_data = [
                        f"Conduit {bundle.bundle_number}",  # Bundle number
                        f"{bundle.stationing_start}",  # Stationing start
                        f"{bundle.stationing_end}",  # Stationing end
                        int(cable.pull_number),  # Individual cable pull number
                        cable.cable_size,  # Cable size (ex. 7C#14)
                        cable.express,  # Express or local
                        bundle.bundle_diameter,  # Bundle diameter
                        bundle.bundle_weight  # Bundle weight
                        # Upsized conduit fill
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
            for row_num, row in enumerate(sheet.iter_rows(min_row=2, max_row=sheet.max_row, min_col=1, max_col=1),
                                          start=2):
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

        if local_code_flag:
            # Save the workbook to a file
            output_filename = "Output File.xlsx"
            workbook.save(output_filename)

            print(f"[PASS] Output file {output_filename} has been saved.")
            print(f"[STATUS] Opening output file...")

            pdf_file_path = 'C:/Users/roneill/OneDrive - Iovino Enterprises, LLC/Documents 1/Code/Git Files/Cable-Run-Optimizer/Output File.xlsx'

            subprocess.run(["start", "", pdf_file_path], shell=True, check=True)

        elif server_code_flag:

            # Upload the workbook to azure blob storage
            sas_url = upload_to_azure(workbook)

            print(f"Conduit data has been saved to uploaded to blob storage.")

            return sas_url


# Create excel output file with list of conduits and which cables are in them
def generate_output_file_for_messenger(bundles):
    if local_code_flag:
        from cable_classes import conduit_sizes
    elif server_code_flag:
        from .cable_classes import conduit_sizes

    print("\n[STATUS] Generating output file...")

    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Set column headers
    headers = [
        "Bundle",
        "Stationing Start",
        "Stationing End",
        "Pull #",
        "Cable Size",
        "Express/Local",
        "Bundle Diameter (in)",
        "Bundle Weight (lb/mft)",
    ]
    sheet.append(headers)

    if server_code_flag:
        logging.info("Conduit list length: %s", len(bundles))

    # Write bundle data and cable attributes to the Excel file
    for bundle_name, bundle in bundles.items():

        for cable in bundle.cables:
            row_data = [
                f"Bundle {bundle.bundle_number}",  # Bundle number
                f"{bundle.stationing_start}",       # Stationing start
                f"{bundle.stationing_end}",         # Stationing end
                int(cable.pull_number),             # Individual cable pull number
                cable.cable_size,                   # Cable size (ex. 7C#14)
                cable.express,                      # Express or local
                bundle.bundle_diameter,             # Bundle diameter
                bundle.bundle_weight/1000           # Bundle weight
                # Upsized conduit fill
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

    if local_code_flag:
        # Save the workbook to a file
        output_filename = "Output File.xlsx"
        workbook.save(output_filename)

        print(f"[PASS] Output file {output_filename} has been saved.")
        print(f"[STATUS] Opening output file...")

        pdf_file_path = 'C:/Users/roneill/OneDrive - Iovino Enterprises, LLC/Documents 1/Code/Git Files/Cable-Run-Optimizer/Output File.xlsx'

        subprocess.run(["start", "", pdf_file_path], shell=True, check=True)

    elif server_code_flag:

        # Upload the workbook to azure blob storage
        sas_url = upload_to_azure(workbook)

        print(f"Conduit data has been saved to uploaded to blob storage.")

        return sas_url
