from file_handler import *
from user_interface import *
from messenger_algorithm import *
from cable_classes import *
from visualizer import get_cable_pull_sheet

get_cable_pull_sheet()
get_cable_sizes()      # Repository of all cables and their parameters
sort_stationing()      # List each stationing value in the pull sheet
stationing_sections()  # List cables between each section of stationing


# Add to draw queue cables with specified coordinates, radius, angle
# add_to_draw_queue(cable_list[5], 5, 30)
# add_to_draw_queue(cable_list[6], 0, 0)
# print(cable_list[5].cable_size)
# print("Number of cables in queue:", len(draw_queue))

print(cable_list[0].cable_size)
add_to_draw_queue(cable_list[0], 0, 0)
generate_cable_image(draw_queue)

# Generate the final image with all the cables to be drawn
# generate_cable_image(draw_queue)