class Cable:
    def __init__(self, pull_number, stationing_start, stationing_end, cable_size, express):
        self.pull_number = pull_number
        self.stationing_start = stationing_start
        self.stationing_end = stationing_end
        self.cable_size = cable_size
        self.express = express


class CableParameters:
    def __init__(self, size, diameter, pounds_per_foot, cross_sectional_area):
        self.size = size
        self.diameter = diameter
        self.pounds_per_foot = pounds_per_foot
        self.cross_sectional_area = cross_sectional_area


# List of Cable objects
cable_list = []

# List to store cable parameter objects
cable_sizes = []

# Initialize an empty set to store unique stationing values
stationing_values = set()

# List to hold cables to be drawn with their polar coordinates (radius and angle)
draw_queue = []