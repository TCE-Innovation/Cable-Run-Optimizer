from file_handler import *
from user_interface import *
from messenger_algorithm import *
from conduit_algorithm import *
from cable_classes import *
from visualizer import get_cable_pull_sheet
import random

get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull Sheet excel
sort_stationing()             # List each stationing value in the pull sheet
create_stationing_sections()  # List cables between each section of stationing
optimize_for_conduit()
# generate_cable_image(draw_queue)

# first_stationing_range = list(cables_between_stationing.keys())[0]
# first_cables = cables_between_stationing[first_stationing_range]
# first_cable = first_cables[0]
#
# print("First cable from the first stationing range:")
# print(f"Stationing range: {str(first_stationing_range[0])[:-2]}+{str(first_stationing_range[0])[-2:]} to {str(first_stationing_range[1])[:-2]}+{str(first_stationing_range[1])[-2:]}")
# print("Cable pull number:", first_cable.cable_size)



# Access the dictionary and print its contents
# for section, cables in cables_between_stationing.items():
#     # Print stationing range with plus sign before the last two digits
#     print(f"Cables between {str(section[0])[:-2]}+{str(section[0])[-2:]} and {str(section[1])[:-2]}+{str(section[1])[-2:]}:")
#     for cable in cables:
#         print(cable)
#     print()  # Print an empty line between sections
#

# print(cables_between_stationing[54300][0])

# print("Test: ")
# print(cable_list[0].diameter)
# print("Test 2:")
# # print(cables_between_stationing[54300, 55300][1].cable_size)
#
# for cable in cables_between_stationing[(54300, 55300)]:
#     print(cable.cable_size)

# Iterate through the stationing ranges in the dictionary
# for start, end in cables_between_stationing.keys():
#     print(f"Stationing range: {str(start)[:-2]}+{str(start)[-2:]} to {str(end)[:-2]}+{str(end)[-2:]}")
#
#     # Iterate through each cable in the stationing range
#     for cable in cables_between_stationing[(start, end)]:
#         print(f"Cable Size: {cable.cable_size}")
#
#     print()  # Print an empty line between stationing ranges

# print(cable_list[0].stationing_end)
#
# add_to_draw_queue(cable_list[0], 5, 90)
# generate_cable_image(draw_queue)

# Take the first five cables from cable_list
# selected_cables = cable_list[:5]
#
# print(cable_list[0].weight)

# # Sort the selected cables based on the diameter of their cable sizes
# sorted_cables = sorted(selected_cables, key=lambda cable: cable.cable_size.diameter, reverse=True)
#
# # Print the sorted cables
# for cable in sorted_cables:
#     print(f"Pull Number: {cable.pull_number}, Diameter: {cable.cable_size.diameter}")


# for i in range(6):
    # sort_cables_in_stationing_section


# cable_list.append(Cable('1.162', '500+00', '600+00', 'CABLE 2', 'E'))
# cable_list.append(Cable('1.162', '500+00', '600+00', 'CABLE 1', 'E'))
# print(cable_list[23].cable_size)
# # add_to_draw_queue(cable_list[23], 4, 0)
# add_to_draw_queue(cable_list[24], 0, 0)
# generate_cable_image(draw_queue)
#
# print("Distance between the two cables is:")
# print(abs(draw_queue[0] - draw_queue[1]))
# print(draw_queue[0][3].diameter)
#
# print("The sum of the two cables' radii is: ")
# print(draw_queue[0][3].diameter + draw_queue[1][3].diameter)

# Accessing the radius from the first tuple in draw_queue
# location_1 = draw_queue[0][0]
#
# # Accessing the radius from the second tuple in draw_queue
# location_2 = draw_queue[1][0]
#
# # Performing math with the radius values
# cables_distance = abs(location_1 - location_2)
# print("Distance between the centers of the cables:", cables_distance)
#
# # Accessing the radius from the first tuple's CableParameters object in draw_queue
# radius_1 = (draw_queue[0][3].diameter)/2
#
# # Accessing the radius from the second tuple's CableParameters object in draw_queue
# radius_2 = (draw_queue[1][3].diameter)/2
#
# # Performing math with the radius values
# sum_of_radii = radius_1 + radius_2
# print("Sum of the radii:", sum_of_radii)
#
# if cables_distance >= sum_of_radii:
#     print("Cables are not overlapping")
# else:
#     print("Cables are overlapping")
#
# generate_cable_image(draw_queue)


#
# for i in range(random.randint(15, 22)):
#     print(cable_list[i].cable_size)
#     add_to_draw_queue(cable_list[i], random.randint(0, 9), random.randint(0, 360))
# generate_cable_image(draw_queue)
