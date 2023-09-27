# Class used to hold data taken from Cables Sizes.xlsx
# To be fed into Cable class
class CableParameters:
    def __init__(self, size, diameter, pounds_per_foot, cross_sectional_area):
        self.size = size
        self.diameter = diameter
        self.pounds_per_foot = pounds_per_foot
        self.cross_sectional_area = cross_sectional_area


# Class that holds the information from the cable pull sheet + cable size info
# Logic matches data from Cable Parameters class
# to fill in information that isn't from cable pull sheet (diameter, weight, area)
class Cable:
    def __init__(self, pull_number, stationing_start: int, stationing_end: int,
                 cable_size, express, diameter: float, weight, cross_sectional_area):
        self.pull_number = pull_number
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.cable_size = cable_size
        self.express = express
        self.diameter = diameter
        self.weight = weight
        self.cross_sectional_area = cross_sectional_area

# Class to create conduits
class Conduit:
    def __init__(self, stationing_start, stationing_end, conduit_free_air_space):
        self.cables = []  # List to hold cable objects
        self.cable_data = []  # List to hold cable data as (radius, angle) tuples
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.conduit_free_air_space = conduit_free_air_space

    def add_cable(self, cable, radius, angle):
        self.cables.append(cable)
        self.cable_data.append((radius, angle))

# Class to create bundles
class Bundle:
    def __init__(self):
        self.cables = []  # List to hold cable objects
        self.radii = []  # List to hold radii
        self.angles = []  # List to hold angles


# List of Cable objects, all cables obtained from the pull sheet
cable_list = []

# List to store cable parameter objects, all cable entries from Cables Sizes.xlsx
cable_sizes = []

# Create an empty dictionary to represent conduits
# Holds all the generated conduits
conduits = {}

# Create an empty dictionary to represent bundles
# Holds all the generated bundles
bundles = {}


conduit_size = 3                    # Conduit diameter in inches, to be made editable
conduit_number = 1                  # Increments whenever another conduit is made
conduit_free_air_space = 100        # Value used in calculations to check that conduit fill is in spec
free_air_space_requirement = 0.6    # Value used in calculations to check that conduit fill is in spec

# Text for image generation
stationing_start_text = None
stationing_end_text = None
express_text = None

# Initialize an empty list to store unique stationing values
# Used in file_handler.py
stationing_values = list()

# List to hold cables to be drawn with their polar coordinates (radius and angle)
# Used in visualizer.py
draw_queue = []

# For output pdf file generation
# Used in visualizer.py
# When the first conduit is created, the flag is set to be true
# to know that following conduit pdf files will be merged

first_file_flag = False
