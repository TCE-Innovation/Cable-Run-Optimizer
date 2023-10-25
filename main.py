from settings import local_code_flag
from settings import server_code_flag

if local_code_flag:

    from conduit_algorithm import *
    from file_handler import *
    from cable_classes import *

    print("[START] Running local code...")

    cable_sizes_list = get_cable_sizes()             # Excel of all cables and their parameters
    cable_list = get_cable_pull_sheet(cable_list, cable_sizes_list)        # Pull sheet excel
    stationing_values_numeric, stationing_text_pairs = sort_stationing(cable_list)             # List each stationing value in the pull sheet, ordered
    conduits = optimize_for_conduit(stationing_values_numeric, stationing_text_pairs, cable_list)        # Run conduit algorithm, generate conduit images
    generate_output_file(conduits)        # Create output excel file with generated conduits

elif server_code_flag:

    from .conduit_algorithm import *
    from .file_handler import get_cable_pull_sheet, get_cable_sizes, sort_stationing, generate_output_file
    from .cable_classes import *
    import logging

    def execute_CRO(pull_sheet, cable_sizes, bytes_flag):
        logging.info("Running execute_CRO main function.")

        logging.info("Running get_cable_sizes().")
        cable_sizes_list = get_cable_sizes(cable_sizes, bytes_flag)                                        # Excel of all cables and their parameters

        logging.info("Running get_cable_pull_sheet().")
        cable_list = get_cable_pull_sheet(pull_sheet, cable_sizes_list)                                                # Pull sheet excel

        logging.info("Sorting stationing values.")
        stationing_values_numeric, stationing_text_pairs = sort_stationing(cable_list)            # List each stationing value in the pull sheet, ordered

        logging.info("Optimizing for conduit.")
        conduits = optimize_for_conduit(stationing_values_numeric, stationing_text_pairs, cable_list)          # Run conduit algorithm, generate conduit images
        logging.info("after opt con conduits list %s", len(conduits))

        logging.info("Generating output file.")
        sas_url = generate_output_file(conduits)                                                # Create output excel file with generated conduits

        return sas_url