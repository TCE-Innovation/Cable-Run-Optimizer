from cable_classes import *
from file_handler import *
from visualizer import *
import math


def optimize_for_conduit():
    from file_handler import stationing_values
    global conduit_number
    global conduit_free_air_space
    global stationing_start_text
    global stationing_end_text

    # Loop through the stationing values and group cables within each stationing range
    print(len(stationing_values))
    for i in range(len(stationing_values) - 1):
        # define the two stationing values that cables will be optimized between
        start_stationing = stationing_values[i]
        print(f"Start stationing value: {start_stationing}")
        end_stationing = stationing_values[i + 1]
        print(f"End Stationing value: {end_stationing}")
        stationing_start_text = f"{str(start_stationing)[:-2]}+{str(start_stationing)[-2:]}"
        stationing_end_text = f"{str(end_stationing)[:-2]}+{str(end_stationing)[-2:]}"

        # Create a list to store cables within the current stationing range
        cables_within_range = []
        for cable in cable_list:
            if cable.stationing_start <= start_stationing and cable.stationing_end >= end_stationing:
                cables_within_range.append(cable)
                print(cable.pull_number)
        # Sort cables within the range based on cross-sectional area (largest cable first)
        cables_within_range.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)
        # Print cables within the range after sorting
        print("Cables within the stationing range after sorting:")
        for cable in cables_within_range:
            print(f"Pull Number: {cable.pull_number}, Cross-sectional Area: {cable.cross_sectional_area}")


        # Create initial conduit for stationing range
        conduit_name = "conduit" + str(conduit_number)
        conduit = Conduit()
        conduits[conduit_name] = conduit

        # Go through all cables in the stationing range
        for cable in cables_within_range:
            # Check if cable added to current conduit wouldn't violate free air space requirement
            if check_free_air_space(conduit, cable) == 0:
                find_open_space(conduit, cable)
            # else if cable can't fit, then create image for the current conduit and move onto next conduits
            else:
                print("Creating new conduit")

                # Draw image, reset draw queue, increment conduit number printed onto next image
                generate_cable_image(draw_queue)    # Create full conduit image
                draw_queue.clear()                  # Empty draw queue for next image
                conduit_number += 1                 # Identifier for image
                conduit_name = "conduit" + str(conduit_number)

                conduit = Conduit()
                conduits[conduit_name] = conduit

                conduit_free_air_space = 100 # Reset airspace in conduit

                # With the cable that failed to be placed into the previous conduit, place into next one
                check_free_air_space(conduit, cable)    # This function should always pass
                find_open_space(conduit, cable)         # Place next conduit at 0,0

        generate_cable_image(draw_queue)  # Create full conduit image
        draw_queue.clear()  # Empty draw queue for next image
        conduit_number += 1  # Identifier for image
        conduit_name = "conduit" + str(conduit_number)

    # # At this point, all cables within the stationing range have been assigned into a conduit.
    # # Create new conduit image
    # print("Pre clear")
    # for radius, angle_deg, cable in draw_queue:
    #     print("Radius:", radius)
    #     print("Angle (degrees):", angle_deg)
    #     print("Cable Information:", cable.pull_number, cable.stationing_start, cable.stationing_end)
    #     print("-------------------------------")
    # print ()
    # generate_cable_image(draw_queue)  # Create full conduit image
    # draw_queue.clear()  # Empty draw queue for next image
    # print("Post clear")
    # for radius, angle_deg, cable in draw_queue:
    #     print("Radius:", radius)
    #     print("Angle (degrees):", angle_deg)
    #     print("Cable Information:", cable.pull_number, cable.stationing_start, cable.stationing_end)
    #     print("-------------------------------")




    # conduit_name = "conduit" + str(conduit_number)
    # conduit = Conduit()
    # conduit.add_cable(cable_list[0], 0, 0)
    # add_to_draw_queue(cable_list[0], 0, 0)
    # print("First cable placed. Pull number: ", cable_list[0].pull_number)
    # conduits[conduit_name] = conduit

    # if not enough space, create new conduit and load next biggest cable to center
    # if enough space, trigger placement function
    # check_free_air_space(conduit, cable_list[1])
    # find_open_space(conduit, cable_list[1])
    # check_free_air_space(conduit, cable_list[2])
    # find_open_space(conduit, cable_list[2])

    # for cable in cable_list[1:]:
    #     if check_free_air_space(conduit, cable) == 0:
    #         find_open_space(conduit, cable)
    #     else:
    #         print("Creating new conduit")
    #         generate_cable_image(draw_queue) # Create full conduit imagae
    #         conduit_number += 1              # Identifier for image
    #         draw_queue.clear()               # Empty draw queue for next image
    #         conduit_name = "conduit" + str(conduit_number)
    #         conduit = Conduit()
    #         conduit_free_air_space = 100
    #         check_free_air_space(conduit, cable)
    #         find_open_space(conduit, cable)
    #         conduits[conduit_name] = conduit
    #         generate_cable_image(draw_queue)


def check_free_air_space(conduit, cable):
    global conduit_free_air_space
    total_area = 0
    for cable in conduit.cables:
        total_area += cable.cross_sectional_area

    # print("Total current area taken up in the conduit:", round(total_area, 2))
    total_area += cable.cross_sectional_area

    if total_area / (math.pi * (conduit_size/2) ** 2) < (1-free_air_space_requirement):
        # print("Conduit can fit next cable")
        # print("Updated total current area taken up in the conduit: ", round(total_area, 2))
        # print(f"Percent of air space taken up by cable: {round((total_area/113.1)*100, 2)}%")
        conduit_free_air_space = round((1 - (total_area / (math.pi * ((conduit_size/2) ** 2)))) * 100, 2)
        # print(f"Free Air Space: {conduit_free_air_space}%")

        return 0
    else:
        print("Conduit cannot fit next cable")
        # add logic to create another conduit
        # also generate cable image to have a blank conduit image for next cables
        return 1


def find_open_space(conduit, new_cable):
    radius_increment = 0.25  # Define the radius increment
    angle_increment = 1  # Define the angle increment
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
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Iterate through possible cable placements until a valid one is found or the conduit is full
    while True:
        # Initialize a flag to track cable overlap
        overlap = False

        # print()
        # Iterate through existing cables in the conduit
        for existing_cable, (cable_radius, cable_angle) in zip(conduit.cables, conduit.cable_data):
            # print(f"Existing Cable Pull Number: {existing_cable.pull_number}")
            # print(f"Cable Radius TO BE CHECKED: {(existing_cable.diameter) / 2}")
            # print(f"Proposed coordinates: Radius: {radius}, Angle: {angle}")
            distance = calculate_distance(radius, angle, cable_radius, cable_angle)  # Calculate distance between cables

            # print(f"The distance between Cable {existing_cable.pull_number} "
            #       f"and Cable {new_cable.pull_number} is {(round(distance), 2)}")
            #
            # print(f"The sum of Cable {existing_cable.pull_number} "
            #       f"and Cable {new_cable.pull_number} radii is "
            #       f"{round((new_cable.diameter / 2) + (existing_cable.diameter) / 2), 2}")
            # print()

            # If the cables are overlapping
            if distance < ((new_cable.diameter / 2) + (existing_cable.diameter / 2)):
                # print(f"FAIL - Coordinates:  {radius}, {angle}")
                overlap = True  # Set the overlap flag to True
                break  # Exit the loop since overlap is detected

        # If no overlap is detected, proceed with cable placement
        if not overlap:
            # print(f"PASS - Coordinates: {radius}, {angle}")  # Print successful placement message
            # print()
            # Call a function to add the new cable to the draw queue
            conduit.add_cable(new_cable, radius, angle)
            add_to_draw_queue(new_cable, radius, angle)
            return radius, angle  # Return the valid placement

        # Increment angle by angle_increment
        if radius == 0:
            radius += radius_increment
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


