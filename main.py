from conduit_algorithm import *
from visualizer import get_cable_pull_sheet
from user_interface import *


# user_interface()
get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit()        # Run conduit algorithm, generate conduit images
generate_output_file()        # Create output excel file with generated conduits

