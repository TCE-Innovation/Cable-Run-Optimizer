from cable_classes import *
from file_handler import generate_output_file
from visualizer import *
import math


def optimize_for_conduit():
    from file_handler import stationing_values

    # Loop through the stationing values and group cables within each stationing range
    print(len(stationing_values))
    for i in range(len(stationing_values) - 1):
        # define the two stationing values that cables will be optimized between
        start_stationing = stationing_values[i]
        end_stationing = stationing_values[i + 1]

        # Create a list to store cables within the current stationing range
        cables_within_range = []

        # Add all cables within stationing range to list
        for cable in cable_list:
            if cable.stationing_start <= start_stationing and cable.stationing_end >= end_stationing:
                cables_within_range.append(cable)

        # Sort cables within the range based on cross-sectional area (largest cable first)
        # cables_within_range.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        # Separate express and local cables
        express_cables = []
        local_cables = []
        for cable in cables_within_range:

            if cable.express.lower() == "express":
                # print("EXPRESS CABLE")
                # print(f"Cable Info: Pull Number={cable.pull_number}, Size={cable.cable_size}, "
                #       f"Diameter={cable.diameter}, Weight={cable.weight}, "
                #       f"Cross Sectional Area={cable.cross_sectional_area}, "
                #       f"Express={cable.express}")

                express_cables.append(cable)
            elif cable.express.lower() == "local":
                # print("LOCAL CABLE")
                # print(f"Cable Info: Pull Number={cable.pull_number}, Size={cable.cable_size}, "
                #       f"Diameter={cable.diameter}, Weight={cable.weight}, "
                #       f"Cross Sectional Area={cable.cross_sectional_area}, "
                #       f"Express={cable.express}")

                local_cables.append(cable)

        # Sort express and local cables separately based on cross-sectional area
        express_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        for cable in express_cables:
            print(f"Cable Info: Pull Number={cable.pull_number}, Size={cable.cable_size}, "
                  f"Diameter={cable.diameter}, Weight={cable.weight}, "
                  f"Cross Sectional Area={cable.cross_sectional_area}, "
                  f"Express={cable.express}")
        local_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        # Create conduits, express cables first, then local cables
        create_conduits(express_cables, start_stationing, end_stationing, 1)
        create_conduits(local_cables, start_stationing, end_stationing, 0)


def create_conduits(cables_within_range, start_stationing, end_stationing, express):
    global express_text
    global conduit_free_air_space
    global conduit_number
    global stationing_start_text
    global stationing_end_text
    from file_handler import stationing_values

    # Text for generated image
    stationing_start_text = f"{str(start_stationing)[:-2]}+{str(start_stationing)[-2:]}"
    stationing_end_text = f"{str(end_stationing)[:-2]}+{str(end_stationing)[-2:]}"

    if express:
        express_text = "Express"
    else:
        express_text = "Local"

    # Create initial conduit for stationing range
    conduit_name = "Conduit" + str(conduit_number)
    conduit = Conduit(start_stationing, end_stationing, conduit_free_air_space)
    conduits[conduit_name] = conduit

    # Go through all cables in the stationing range
    for cable in cables_within_range:
        # Check if cable added to current conduit wouldn't violate free air space requirement
        if check_free_air_space(conduit, cable) == 0:
            find_open_space(conduit, cable)
        # else if cable can't fit, then create image for the current conduit and move onto next conduits
        else:
            # Draw image, reset draw queue, increment conduit number printed onto next image
            generate_cable_image(draw_queue)    # Create full conduit image
            draw_queue.clear()                  # Empty draw queue for next image
            conduit_number += 1                 # Identifier for image
            conduit_name = "Conduit" + str(conduit_number)

            conduit = Conduit(start_stationing, end_stationing, conduit_free_air_space)
            conduits[conduit_name] = conduit

            conduit_free_air_space = 100 # Reset airspace in conduit

            # With the cable that failed to be placed into the previous conduit, place into next one
            check_free_air_space(conduit, cable)    # This function should always pass
            find_open_space(conduit, cable)         # Place next conduit at 0,0

    generate_cable_image(draw_queue)  # Create full conduit image
    draw_queue.clear()  # Empty draw queue for next image
    conduit_number += 1  # Identifier for image
    conduit_name = "Conduit" + str(conduit_number)


def check_free_air_space(conduit, cable):
    global conduit_free_air_space
    total_area = 0
    for cable in conduit.cables:
        total_area += cable.cross_sectional_area

    # print("Total current area taken up in the conduit:", round(total_area, 2))
    total_area += cable.cross_sectional_area

    # If area taken up by all cables in conduit is less than the maximum area that can be taken up by cable
    if total_area / (math.pi * (conduit_size/2) ** 2) < (1-free_air_space_requirement):
        # Update free airspace value
        conduit_free_air_space = round((1 - (total_area / (math.pi * ((conduit_size/2) ** 2)))) * 100, 2)
        conduit.conduit_free_air_space = conduit_free_air_space # update conduit value
        return 0
    else:
        # Logic in outer function to create next conduit
        return 1


def find_open_space(conduit, new_cable):
    radius_increment = 0.1  # Define the radius increment
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

        # Iterate through existing cables in the conduit
        for existing_cable, (cable_radius, cable_angle) in zip(conduit.cables, conduit.cable_data):
            # Calculate distance between cables
            distance = calculate_distance(radius, angle, cable_radius, cable_angle)

            # If the cables are overlapping
            if distance < ((new_cable.diameter / 2) + (existing_cable.diameter / 2)):
                overlap = True  # Set the overlap flag to True
                break           # Exit the loop since overlap is detected

        # If no overlap is detected, proceed with cable placement
        if not overlap:
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


