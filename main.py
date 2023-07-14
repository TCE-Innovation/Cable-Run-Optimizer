from file_handler import *
from user_interface import *
from messenger_algorithm import *
from visualizer import *

get_cable_sizes()

print(len(cable_sizes))
generate_cable_image(cable_sizes[6:11])  # Extract cables from indices 2 to 4 (inclusive)
