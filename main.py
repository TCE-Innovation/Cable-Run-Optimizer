from settings import local_code_flag
from settings import server_code_flag

if local_code_flag:

    from conduit_algorithm import *
    from file_handler import *

    get_cable_sizes()             # Excel of all cables and their parameters
    get_cable_pull_sheet()        # Pull sheet excel
    stationing_values = sort_stationing()             # List each stationing value in the pull sheet, ordered
    optimize_for_conduit(stationing_values_numeric, stationing_text_pairs)        # Run conduit algorithm, generate conduit images
    generate_output_file()        # Create output excel file with generated conduits

elif server_code_flag:

    from .conduit_algorithm import *
    from .file_handler import get_cable_pull_sheet, get_cable_sizes, sort_stationing, generate_output_file
    import logging

    def execute_CRO(pull_sheet, cable_sizes, bytes_flag):
        logging.info("Running execute_CRO main function.")

        logging.info("Getting cable sizes.")
        get_cable_sizes(cable_sizes, bytes_flag)               # Excel of all cables and their parameters

        logging.info("Getting pull sheet.")
        get_cable_pull_sheet(pull_sheet)           # Pull sheet excel

        logging.info("Sorting stationing values.")
        stationing_values_numeric, stationing_text_pairs = sort_stationing()      # List each stationing value in the pull sheet, ordered
        logging.info("stationing values numeric: %s", str(stationing_values_numeric))
        logging.info("stationing values text pairs: %s", str(stationing_text_pairs))


        logging.info("Optimizing for conduit.")
        optimize_for_conduit(stationing_values_numeric, stationing_text_pairs)                 # Run conduit algorithm, generate conduit images

        logging.info("Generating output file.")
        sas_url = generate_output_file()                     # Create output excel file with generated conduits

        return sas_url

