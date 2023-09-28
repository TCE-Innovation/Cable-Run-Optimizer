###############
#### Local ####
###############
from conduit_algorithm import *
from file_handler import *

# user_interface()
get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit()        # Run conduit algorithm, generate conduit images
generate_output_file()        # Create output excel file with generated conduits

###############
#### Server ###
###############
'''
from .conduit_algorithm import *
from .file_handler import get_cable_pull_sheet, get_cable_sizes, sort_stationing, generate_output_file
import logging

def execute_CRO(pull_sheet, cable_sizes):
    logging.info("Running execute_CRO main function.")

    logging.info("Getting cable sizes.")
    get_cable_sizes(cable_sizes)               # Excel of all cables and their parameters
    
    logging.info("Getting pull sheet.")
    get_cable_pull_sheet(pull_sheet)           # Pull sheet excel
    
    logging.info("Sorting stationing values.")
    stationing_values = sort_stationing()      # List each stationing value in the pull sheet, ordered
    logging.info("stationing values: " + str(stationing_values))
    
    logging.info("Optimizing for conduit.")
    optimize_for_conduit(stationing_values)                 # Run conduit algorithm, generate conduit images

    logging.info("Generating output file.")
    sas_url = generate_output_file()                     # Create output excel file with generated conduits

    return sas_url

'''