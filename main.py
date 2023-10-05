###############
#### Local ####
###############
from conduit_algorithm import *
from file_handler import *

get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
stationing_values = sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit(stationing_values)        # Run conduit algorithm, generate conduit images
generate_output_file()        # Create output excel file with generated conduits

# conduit_nmbr = 1
#
# conduit = Conduit(100, 200,
#                   conduit_area=0, conduit_fill=0, conduit_size=3.5, conduit_number=conduit_nmbr)
# # Conduit area will be updated every time a new cable is added (add_cable_to_conduit function)
# # Conduit size + fill will be updated when the optimal conduit size is determined (tightly_resize_conduit function)
#
# # Add newly made conduit to list of conduits
# conduits["Conduit" + str(conduit_nmbr)] = conduit
#
# conduit = Conduit(200, 300,
#                   conduit_area=0, conduit_fill=0, conduit_size=2.5, conduit_number=conduit_nmbr)
#
# conduit_nmbr += 1
#
# conduits["Conduit" + str(conduit_nmbr)] = conduit
#
# for conduit_name, conduit in conduits.items():
#     print(f"Conduit Name: {conduit.cables[0]}")
#     print(f"Conduit Size: {conduit.conduit_size}")



# print(conduits["Conduit1"].cables[0])








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