from cable_classes import *
from visualizer import *
from file_handler import *
import math


def optimize_for_conduit():
    # Place first cable down into center
    # current_stationing = list(cables_between_stationing.keys())[0]
    # first_cable = cables_between_stationing[current_stationing][0]
    # add_to_draw_queue(first_cable, 0, 0)

    conduit_name = "conduit1"
    conduit = Conduit()
    conduit.add_cable(cable_list[0], 0, 0)
    # add_to_draw_queue(cable_list[0], 0, 0)
    conduits[conduit_name] = conduit

    # if not enough space, create new conduit and load next biggest cable to center
    # if enough space, trigger placement function
    check_free_air_space(conduit, cable_list[1])
    find_open_space(conduit, cable_list[1])


    # print(conduits["conduit1"].angles[0])

    # check_free_air_space()


    pass


def check_free_air_space(conduit, cable):
    total_area = 0
    for cable in conduit.cables:
        total_area += cable.cross_sectional_area

    total_area += cable.cross_sectional_area

    print("Total cross-sectional area in the conduit:", total_area)

    if total_area/113.1 < (1-free_air_space_requirement):
        print("Conduit can fit next cable")
        return 0
    else:
        print("Conduit cannot fit next cable")
        return 1
    pass


# def find_open_space(conduit, cable):
#     print("PLEASE WORK:")
#     print(conduit.cables[0].diameter)
#     pass


def find_open_space(conduit, new_cable):
    radius_increment = 1  # Define the radius increment
    angle_increment = 15  # Define the angle increment
    max_radius = 6

    # Initial placement at (radius=0, angle=0)
    radius = 0
    angle = 0

    # Function to calculate distance between two polar coordinates
    def calculate_distance(r1, a1, r2, a2):
        x1 = r1 * math.cos(math.radians(a1))
        y1 = r1 * math.sin(math.radians(a1))
        x2 = r2 * math.cos(math.radians(a2))
        y2 = r2 * math.sin(math.radians(a2))
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    while True:
        # Check if the new cable's placement overlaps with any existing cables
        overlap = False
        for cable in conduit.cables:
            distance = calculate_distance(radius, angle, cable.diameter / 2, cable.angle)
            if distance < (new_cable.diameter + cable.diameter) / 2:
                print(f"FAIL: radius: {radius}, angle: {angle}")
                overlap = True
                break

        if not overlap:
            print(f"Placing cable at radius: {radius}, angle: {angle}")
            return radius, angle  # Found a valid placement

        # Increment radius and angle
        radius += radius_increment
        if angle >= 360:
            angle = angle % 360
            radius += radius_increment
        angle += angle_increment

        # Check if the conduit is full
        if radius > max_radius:
            print("Failed: Conduit is full.")
            break
