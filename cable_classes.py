class Cable:
    def __init__(self, pull_number, stationing_start: int, stationing_end: int,
                 cable_size, express, diameter, weight, cross_sectional_area):
        self.pull_number = pull_number
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.cable_size = cable_size
        self.express = express
        self.diameter = diameter
        self.weight = weight
        self.cross_sectional_area = cross_sectional_area


# List of Cable objects
cable_list = []


class CableParameters:
    def __init__(self, size, diameter, pounds_per_foot, cross_sectional_area):
        self.size = size
        self.diameter = diameter
        self.pounds_per_foot = pounds_per_foot
        self.cross_sectional_area = cross_sectional_area


# List to store cable parameter objects
cable_sizes = []


class Bundle:
    def __init__(self):
        self.cables = []  # List to hold cable objects
        self.radii = []   # List to hold radii
        self.angles = []  # List to hold angles


# Create an empty dictionary to represent bundles
bundles = {}


class Conduit:
    def __init__(self):
        self.cables = []  # List to hold cable objects
        self.radii = []   # List to hold radii
        self.angles = []  # List to hold angles

    def add_cable(self, cable, radius, angle):
        self.cables.append(cable)
        self.radii.append(radius)
        self.angles.append(angle)


# Create an empty dictionary to represent conduits
conduits = {}

# Initialize an empty set to store unique stationing values
stationing_values = set()

# List to hold cables to be drawn with their polar coordinates (radius and angle)
draw_queue = []

free_air_space_requirement = 0.6

