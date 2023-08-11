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
    add_to_draw_queue(cable_list[0], 0, 0)
    # add_to_draw_queue(cable_list[5], 1, 0) # 83 is 1
    conduits[conduit_name] = conduit

    # if not enough space, create new conduit and load next biggest cable to center
    # if enough space, trigger placement function
    check_free_air_space(conduit, cable_list[1])
    find_open_space(conduit, cable_list[1])


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


def find_open_space(conduit, new_cable):
    radius_increment = 0.25  # Define the radius increment
    angle_increment = 15  # Define the angle increment
    max_radius = 6  # Maximum radius for placement

    # Initial placement at (radius=0, angle=0)
    radius = 0
    angle = 0

    # Function to calculate distance between two polar coordinates
    def calculate_distance(r1, a1, r2, a2):
        x1 = r1 * math.cos(math.radians(a1))
        y1 = r1 * math.sin(math.radians(a1))
        x2 = r2 * math.cos(math.radians(a2))
        y2 = r2 * math.sin(math.radians(a2))
        return round(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2), 2)

    # Iterate through possible cable placements until a valid one is found or the conduit is full
    while True:
        # Initialize a flag to track cable overlap
        overlap = False

        # Iterate through existing cable data within the conduit
        for i, cable_data in enumerate(conduit.cable_data):
            cable_radius, cable_angle = cable_data  # Extract radius and angle from cable data
            distance = calculate_distance(radius, angle, cable_radius, cable_angle)  # Calculate distance between cables

            print(f"Distance: {distance}, Radii Sum: {((new_cable.diameter/2) + (new_cable.diameter/2))}")
            # Check if the distance between cables is less than the sum of their diameters (overlap condition)
            if distance < ((new_cable.diameter/2) + (new_cable.diameter/2)):

                print(f"FAIL: radius: {radius}, angle: {angle}")  # Print failure message with current placement
                overlap = True  # Set the overlap flag to True
                break  # Exit the loop since overlap is detected

        # If no overlap is detected, proceed with cable placement
        if not overlap:
            print(f"PASS: radius: {radius}, angle: {angle}")  # Print successful placement message
            # Call a function to add the new cable to the draw queue
            add_to_draw_queue(new_cable, radius, angle)
            return radius, angle  # Return the valid placement

        # Increment angle by angle_increment
        if radius == 0:
            radius =+ radius_increment
        else:
            angle += angle_increment



        # Check if angle has completed a full circle (360 degrees)
        if angle >= 360:
            angle = angle % 360  # Reset angle to 0
            radius += radius_increment  # Increment radius

        # Check if the conduit is full
        if radius > max_radius:
            print("Failed: Conduit is full.")
            break


