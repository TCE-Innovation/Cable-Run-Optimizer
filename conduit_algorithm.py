from visualizer import *
import math


def optimize_for_conduit():
    from file_handler import stationing_values

    # Loop through the stationing values and group cables within each stationing range
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

        # Separate express and local cables
        express_cables = []
        local_cables = []

        for cable in cables_within_range:

            if cable.express.lower() == "express":
                express_cables.append(cable)
            elif cable.express.lower() == "local":
                local_cables.append(cable)

        # Sort express and local cables separately based on cross-sectional area
        express_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)
        local_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        print()
        # Create conduits, express cables first, then local cables
        if len(express_cables):
            print("Function call of create_conduits to create conduits from express cables...")
            create_conduits(express_cables, start_stationing, end_stationing, True)
        if len(local_cables):
            print("Function call of create_conduits to create conduits from local cables...")
            create_conduits(local_cables, start_stationing, end_stationing, False)


def create_conduits(cables_within_range, start_stationing, end_stationing, express):
    global express_text
    global conduit_free_air_space
    global conduit_number
    global stationing_start_text
    global stationing_end_text

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

    # Initialize a list to keep track of which cables are being placed in a conduit
    # to avoid double counting cables across conduits
    placed_cables = []

    print("Pull Numbers of Cables within the stationing range to create conduits from:")
    pull_numbers = ", ".join(str(cable.pull_number) for cable in cables_within_range)
    print(pull_numbers)
    print()

    # Go through all cables in the stationing range
    for cable in cables_within_range:
        print()
        print(f"Cable in outermost for loop: {cable.pull_number}")

        if cable in placed_cables:
            continue

        # Check if cable added to current conduit wouldn't violate free air space requirement
        if check_free_air_space(conduit, cable):
            find_open_space(conduit, cable)
            placed_cables.append(cable)
            print(f"Cable {cable.pull_number} was placed.")
            print(f"Conduit {conduit_number} Fill: {100 - conduit.conduit_free_air_space:.2f}%")
            print()

        # else if cable can't fit, then try other cables before creating new conduit image
        else:
            print(f"Cable {cable.pull_number} NOT placed. Cable Area: {cable.cross_sectional_area}")
            print("Checking if a smaller cable can fit into the conduit...")
            # Create a list of smaller cables that can fit into the conduit
            smaller_cables = [c for c in cables_within_range if
                              c not in placed_cables and c.cross_sectional_area < cable.cross_sectional_area]

            print("Small cables that will be tested if they fit:")
            for small_cable in smaller_cables:
                print(f"Pull #: {small_cable.pull_number}, Area: {small_cable.cross_sectional_area}")

            # Iterate through the smaller cables
            for smaller_cable in smaller_cables:
                print(f"Small cable being tested: {smaller_cable.pull_number}...")
                # Check if the smaller cable can fit without violating free air space
                if check_free_air_space(conduit, smaller_cable):
                    print(f"Pass. Cable {smaller_cable.pull_number} can into Conduit {conduit_number}")
                    # If it can fit, find an open space in the conduit for the smaller cable
                    find_open_space(conduit, smaller_cable)

                    # Add the smaller cable to the list of placed cables to avoid double placement
                    placed_cables.append(smaller_cable)
                else:
                    print(f"Fail. Cable {smaller_cable.pull_number} cannot fit into Conduit {conduit_number}")


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
    for existing_cable in conduit.cables:
        total_area += existing_cable.cross_sectional_area

    print(f"Testing if cable {cable.pull_number} can fit into Conduit {conduit_number}...")

    total_area += cable.cross_sectional_area
    # print(f'Area: {total_area}')

    # If area taken up by all cables in conduit is less than the maximum area that can be taken up by cable
    if total_area / (math.pi * (conduit_size/2) ** 2) < (1-free_air_space_requirement):
        # Update free airspace value for conduit
        conduit_free_air_space = round((1 - (total_area / (math.pi * ((conduit_size/2) ** 2)))) * 100, 2)
        conduit.conduit_free_air_space = conduit_free_air_space
        # print(f"Conduit Fill: {100 - conduit.conduit_free_air_space:.2f}%")
        return 1
    else:
        # Return 0 for outside of if statement to check other cables/make next conduit
        # print(f"Area failed for adding cable {cable.pull_number}. Theoretical Fill: {100*(total_area / (math.pi * (conduit_size/2) ** 2)):.2f}%")
        return 0


# Spiraling out from center
def find_open_space(conduit, new_cable):
    radius_increment = 0.1          # Define the radius increment
    angle_increment = 1             # Define the angle increment
    # max_radius = conduit_size/2     # Maximum radius for placement
    max_radius = 6 # for testing purposes
    # Initial placement at (radius=0, angle=0    )
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
            add_to_draw_queue(new_cable, (6/conduit_size) * radius, angle)
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