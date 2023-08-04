from file_handler import *
from user_interface import *
from messenger_algorithm import *
from cable_classes import *
from visualizer import get_cable_pull_sheet
import random

get_cable_pull_sheet() # Excel with cables
get_cable_sizes()      # Repository of all cables and their parameters
sort_stationing()      # List each stationing value in the pull sheet
stationing_sections()  # List cables between each section of stationing

cable_list.append(Cable('1.162', '500+00', '600+00', 'CABLE 2', 'E'))
cable_list.append(Cable('1.162', '500+00', '600+00', 'CABLE 2', 'E'))
# print(cable_list[23].cable_size)
add_to_draw_queue(cable_list[23], 4, 0)
add_to_draw_queue(cable_list[24], 2, 0)
#
# print("Distance between the two cables is:")
# print(abs(draw_queue[0] - draw_queue[1]))
# print(draw_queue[0][3].diameter)
#
# print("The sum of the two cables' radii is: ")
# print(draw_queue[0][3].diameter + draw_queue[1][3].diameter)

# Accessing the radius from the first tuple in draw_queue
location_1 = draw_queue[0][0]

# Accessing the radius from the second tuple in draw_queue
location_2 = draw_queue[1][0]

# Performing math with the radius values
cables_distance = abs(location_1 - location_2)
print("Distance between the centers of the cables:", cables_distance)

# Accessing the radius from the first tuple's CableParameters object in draw_queue
radius_1 = (draw_queue[0][3].diameter)/2

# Accessing the radius from the second tuple's CableParameters object in draw_queue
radius_2 = (draw_queue[1][3].diameter)/2

# Performing math with the radius values
sum_of_radii = radius_1 + radius_2
print("Sum of the radii:", sum_of_radii)

if cables_distance > sum_of_radii:
    print("Cables are not overlapping")
else:
    print("Cables are overlapping")

generate_cable_image(draw_queue)



# for i in range(random.randint(1, 22)):
#     print(cable_list[i].cable_size)
#     add_to_draw_queue(cable_list[i], random.randint(0, 10), random.randint(0, 360))
# generate_cable_image(draw_queue)


# For the Cable class:
#
# pull_number: The pull number of the cable.
# stationing_start: The starting stationing of the cable.
# stationing_end: The ending stationing of the cable.
# cable_size: The size of the cable.
# express: The express value of the cable.
# For the CableParameters class:
#
# size: The size of the cable.
# diameter: The diameter of the cable.
# pounds_per_foot: The weight of the cable per foot.
# cross_sectional_area: The cross-sectional area of the cable.