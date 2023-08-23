from file_handler import *
from user_interface import *
from messenger_algorithm import *
from conduit_algorithm import *
from cable_classes import *
from visualizer import get_cable_pull_sheet


# user_interface()
get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit()
generate_output_file()