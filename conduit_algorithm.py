###############
#### Local ####
###############

from visualizer import *
import math

###############
#### Server ###
###############
'''
from .cable_classes import *
import math
'''


def optimize_for_conduit(stationing_values):
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

        # Sort express and local cables separately, sorting by size
        express_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)
        local_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        # Create conduits
        if len(express_cables):  # Checking if there are express cables to sort
            create_conduits(express_cables, start_stationing, end_stationing, True)
        if len(local_cables):    # Checking if there are local cables to sort
            create_conduits(local_cables, start_stationing, end_stationing, False)


def create_new_conduit(start_stationing, end_stationing, conduit_nmbr):
    conduit = Conduit(start_stationing, end_stationing,
                      conduit_area=0, conduit_fill=0, conduit_size=3.5, conduit_number=conduit_nmbr)
    # Conduit area will be updated every time a new cable is added (add_cable_to_conduit function)
    # Conduit size + fill will be updated when the optimal conduit size is determined (tightly_resize_conduit function)

    # Add newly made conduit to list of conduits
    conduits[f"Conduit {conduit_nmbr}"] = conduit

    return conduit


def add_cable_to_conduit(conduit, cable, placed_cables):
    print(f"[STATUS] Adding Cable {cable.pull_number} ({cable.cable_size}) to conduit {conduit.conduit_number}...")
    conduit.add_cable(cable)            # Add cable to conduit
    conduit.calculate_conduit_area()    # Update total area of cables in conduit
    print(f"[STATUS] Cable added successfully. Updated total cable area: {conduit.conduit_area}")

    placed_cables.append(cable)         # Add cable to list of placed cables

    return placed_cables


def create_conduits(cables_within_range, start_stationing, end_stationing, express):
    # global express_text
    # global conduit_free_air_space
    # global conduit_number
    # global stationing_start_text
    # global stationing_end_text

    # Text for generated image
    # stationing_start_text = f"{str(start_stationing)[:-2]}+{str(start_stationing)[-2:]}"
    # stationing_end_text = f"{str(end_stationing)[:-2]}+{str(end_stationing)[-2:]}"

    # if express:
    #     express_text = "Express"
    # else:
    #     express_text = "Local"

    # Create initial conduit for stationing range
    # conduit = Conduit(start_stationing, end_stationing,
    #                   conduit_area=0, conduit_fill=0, conduit_size=3.5, conduit_number=1)
    # conduits["Conduit1"] = conduit

    conduit = create_new_conduit(start_stationing, end_stationing, 1)   # Create first conduit
    print(f"[STATUS] Conduit {conduit.conduit_number} has been created")

    # Initialize a list to keep track of which cables are being placed in a conduit
    # to avoid double counting cables across conduits
    placed_cables = []

    # Go through all cables in the stationing range
    for cable in cables_within_range:

        # If the cable was already placed in a conduit,
        # skip iteration of loop to avoid double counting cables
        if cable in placed_cables:
            continue

        # Check if cable added to current conduit wouldn't violate free air space requirement
        if check_free_air_space(conduit, cable):
            # find_open_space(conduit, cable)
            # conduit.add_cable(cable, None, None) # Temp adding cable to conduit this way to skip dealing with visualizer
            # conduit.conduit_area += cable.cross_sectional_area
            placed_cables = add_cable_to_conduit(conduit, cable, placed_cables)

        # else if cable can't fit, then try other cables before creating new conduit image
        else:
            # Create a list of smaller cables to potentially fit into the conduit
            # Logic is checking that:
            # a) cable is within stationing range
            # b) cable wasn't placed yet
            # c) cable is smaller than the cable that couldn't fit
            smaller_cables = [c for c in cables_within_range if
                              c not in placed_cables and c.cross_sectional_area < cable.cross_sectional_area]

            # Iterate through the smaller cables to check if they would fit
            for smaller_cable in smaller_cables:
                # Check if the smaller cable can fit without violating free air space
                if check_free_air_space(conduit, smaller_cable):
                    # If it can fit, find an open space in the conduit for the smaller cable
                    # find_open_space(conduit, smaller_cable)

                    placed_cables = add_cable_to_conduit(conduit, cable, placed_cables)
                else:
                    # Go through next iterations of the for loop to potentially get a smaller cable to fit
                    # If all smaller cables are exhausted, then create a new conduit
                    pass

        # See if the generated conduit can be smaller while maintaining conduit fill under 40%
        tightly_resize_conduit(conduit)

        # Create new conduit for remainder of cables
        create_new_conduit(start_stationing, end_stationing, conduit.conduit_number + 1)

        # Draw image, reset draw queue, increment conduit number printed onto next image
        # Create new conduit
        # generate_cable_image(draw_queue)    # Create full conduit image
        # draw_queue.clear()                  # Empty draw queue for next image


# Work backwards, compare conduit fill of potential downsized conduits
# Keep working until before fill of 40% or higher is reached
def tightly_resize_conduit(conduit):
    print(f"[STATUS] Checking if Conduit {conduit.conduit_number} can be resized...")

    # List of potential conduit sizes
    from cable_classes import conduit_sizes

    size = len(conduit_sizes) - 1 # Biggest conduit size (4 inches)

    # While conduit fill is less than 40% with smaller size
    while (100*conduit.conduit_area / (math.pi * ((conduit_sizes[size - 1]/2) ** 2))) < 40:
        # print(f"Tighten call: {100*conduit.conduit_area / (math.pi * ((conduit_sizes[size - 1]/2) ** 2))}")
        # watch = conduit.conduit_area / (math.pi * ((conduit_sizes[size - 1]/2) ** 2))
        size -= 1 # Size down conduit

    # Set conduit's size to calculated smallest size
    conduit.conduit_size = conduit_sizes[size]

    # Calculate conduit fill based on optimized size
    conduit.conduit_fill = conduit.conduit_area / ( math.pi * ( (conduit.conduit_size/2) ** 2)  )

    if conduit.conduit_size == 3.5:
        print(f"[STATUS] Conduit {conduit.conduit_number} is at smallest size already")
    else:
        print(f"[STATUS] Conduit {conduit.conduit_number} has been resized to {conduit.conduit_size} inches")


def check_free_air_space(conduit, cable):
    global conduit_free_air_space
    global max_conduit_size

    # print(f"Conduit {conduit_number} has a pre-check conduit fill of "
    #       f"{100 * conduit.conduit_area / (math.pi * ((max_conduit_size / 2) ** 2)):.2f}%")

    # Add area of cable to test if it would fit into conduit
    conduit.conduit_area += cable.cross_sectional_area
    # print(f"Cable {cable.pull_number}: {cable.cable_size} has an area of {cable.cross_sectional_area}")

    # print(f'Area: {total_area}')
    # print(round((conduit.conduit_area  / (math.pi * ((max_conduit_size/2) ** 2))) * 100, 2))
    # If area taken up by all cables in conduit is less than the maximum area that can be taken up by cable
    if conduit.conduit_area / (math.pi * (max_conduit_size/2) ** 2) < (1-free_air_space_requirement):
        # Update free airspace value for conduit
        conduit_free_air_space = round((1 - (conduit.conduit_area  / (math.pi * ((max_conduit_size/2) ** 2)))) * 100, 2)
        conduit.conduit_free_air_space = conduit_free_air_space
        # print(f"Conduit {conduit_number} has a post-check conduit fill of "
        #       f"{100 * conduit.conduit_area / (math.pi * ((max_conduit_size / 2) ** 2)):.2f}%")

        return 1
    else:
        # Return 0 for outside of if statement to check other cables/make next conduit
        conduit.conduit_area -= cable.cross_sectional_area
        return 0


# Spiraling out from center
def find_open_space(conduit, new_cable):

    # Skip over this for two conductor cables
    # Just want to see this added to conduit, not interested in visualizing rn
    if new_cable.diameter is None:
        conduit.add_cable(new_cable, None, None)
    else:

        radius_increment = 0.1         # Define the radius increment
        angle_increment = 5             # Define the angle increment
        # max_radius = conduit_size/2     # Maximum radius for placement
        max_radius = 6 # for testing purposes
        # Initial placement at (radius=0, angle=0    )
        radius = 0 # EDITED FROM RADIUS = 0 TO FIT CABLES VISUALLY
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
                # add_to_draw_queue(new_cable, (6/conduit_size) * radius, angle)
                return radius, angle  # Return the valid placement

            # Increment angle by angle_increment
            if radius == 0:
                radius += radius_increment
            else:
                angle += angle_increment

            # Check if angle has completed a full circle (360 degrees)
            if angle >= 360:
                angle = angle % 360  # Reset angle to 0
                radius += radius_increment  # Increment radius, EDITED FROM += TO -= TO FIT CABLES VISUALLY

            # Check if the conduit is full
            if radius > max_radius:
                print("Failed: Conduit is full.")
                break