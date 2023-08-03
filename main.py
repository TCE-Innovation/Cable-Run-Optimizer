from file_handler import *
from user_interface import *
from messenger_algorithm import *
from cable_classes import *
from visualizer import *


# get_cable_pull_sheet()
# sort_stationing()
# stationing_sections()
# print(cable_list[0].pull_number)

# Sample cable pull sheet information
cable_list = [
    Cable('1.160', '500+00', '600+00', '7C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.162', '500+00', '600+00', 'SCALE CABLE', 'E'),
    Cable('1.163', '500+00', '600+00', 'SCALE CABLE 2', 'E')
]

# Get cable sizing parameters: Size, Diameter, Weight, and calculate cross-sectional areas
get_cable_sizes()

# Add to draw queue cables with specified coordinates, radius, angle
add_to_draw_queue(cable_list[5].cable_size, 5, 135)
add_to_draw_queue(cable_list[6].cable_size, 0, 0)
print(cable_list[5].cable_size)
print("Number of cables in queue:", len(draw_queue))

# Generate the final image with all the cables to be drawn
# generate_cable_image(draw_queue)