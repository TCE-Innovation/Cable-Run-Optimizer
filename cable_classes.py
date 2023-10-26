import math


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
                 cable_size, express, diameter, weight, cross_sectional_area, absolute_distance):
        self.pull_number = pull_number
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.cable_size = cable_size
        self.express = express
        self.diameter = diameter
        self.weight = weight
        self.cross_sectional_area = cross_sectional_area
        self.absolute_distance = absolute_distance


# Class to create conduits
class Conduit:
    def __init__(self, stationing_start, stationing_end,
                 conduit_area, conduit_fill, conduit_size, conduit_number):
        self.cables = []        # List to hold cable objects
        self.cable_data = []    # List to hold cable data as (radius, angle) tuples
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.conduit_fill = conduit_fill
        self.conduit_area = conduit_area if conduit_area is not None else 0     # Use 0 if conduit_area is not provided
        self.conduit_size = conduit_size if conduit_size is not None else 3.5   # Use 3.5, max conduit size
        self.conduit_number = conduit_number

    # def add_cable(self, cable, radius, angle):
    #     self.cables.append(cable)
    #     self.cable_data.append((radius, angle))

    def add_cable(self, cable):
        self.cables.append(cable)

    def calculate_conduit_area_and_default_fill(self):
        self.conduit_area = sum(cable.cross_sectional_area for cable in self.cables)
        self.conduit_fill = 100 * self.conduit_area / (((max_conduit_size/2) ** 2) * math.pi)


# Class to create conduits
class Bundle:
    def __init__(self, stationing_start, stationing_end,
                 bundle_diameter, bundle_weight,  bundle_number):
        self.cables = []        # List to hold cable objects
        self.cable_data = []
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.bundle_diameter = bundle_diameter
        self.bundle_weight = bundle_weight
        self.bundle_number = bundle_number

    # def add_cable(self, cable, radius, angle):
    #     self.cables.append(cable)
    #     self.cable_data.append((radius, angle))

    def add_cable(self, cable):
        self.cables.append(cable)

    def calculate_bundle_diameter_and_weight(self):
        self.bundle_diameter = sum(cable.diameter for cable in self.cables)
        self.bundle_weight = sum(cable.weight for cable in self.cables)


# Create an empty dictionary to represent bundles
# Holds all the generated bundles
# bundles = {}
bundle_number = 1
max_bundle_weight = 20000   # lb/mft


# Potential conduit sizes, inches
conduit_sizes = [0.75, 1, 1.25, 1.5, 2, 2.5, 3, 3.5, 4]
max_conduit_size = 3.5

conduit_number = 1                  # Increments whenever another conduit is made
conduit_free_air_space = 100        # Value used in calculations to check that conduit fill is in spec
free_air_space_requirement = 0.6    # Value used in calculations to check that conduit fill is in spec

# Text for image generation
stationing_start_text = None
stationing_end_text = None
express_text = None

# Initialize an empty list to store unique stationing values
# Used in file_handler.py
stationing_values_numeric = list()
stationing_text_pairs = list()

# List to hold cables to be drawn with their polar coordinates (radius and angle)
# Used in visualizer.py
draw_queue = []

# For output pdf file generation
# Used in visualizer.py
# When the first conduit is created, the flag is set to be true
# to know that following conduit pdf files will be merged

first_file_flag = False

cable_list = []