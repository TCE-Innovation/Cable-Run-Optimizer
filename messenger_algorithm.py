from settings import *
import logging

if local_code_flag:
    import math
    from cable_classes import *


elif server_code_flag:
    from .cable_classes import *
    import math


def optimize_for_messenger(stationing_values_numeric, stationing_text_pairs, cable_list):
    if server_code_flag:
        logging.info("Running optimize_for_messenger function.")
        logging.info("length of cable_list: %s", len(cable_list))

    bundles = {}

    # Loop through the stationing values and group cables within each stationing range
    # HANDLE ONLY NUMERIC STATIONING VALUES
    for i in range(len(stationing_values_numeric) - 1):
        # define the two stationing values that cables will be optimized between
        start_stationing = stationing_values_numeric[i]
        end_stationing = stationing_values_numeric[i + 1]

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

        # Sort express and local cables separately
        # Sort first by cable length (stationing_end - stationing_start) in descending order
        # Then sort by cable size (cross_sectional_area) in descending order
        express_cables.sort(key=lambda cable: (
        int(cable.stationing_end.replace("+", "")) - int(cable.stationing_start.replace("+", "")),
        -cable.cross_sectional_area), reverse=True)

        local_cables.sort(key=lambda cable: (
        int(cable.stationing_end.replace("+", "")) - int(cable.stationing_start.replace("+", "")),
        -cable.cross_sectional_area), reverse=True)

        # Print the sorted express cables
        print("[INFO] Sorted Express Cables:")
        for cable in express_cables:
            print(f"Pull #: {cable.pull_number}, Cable Size: {cable.cable_size}, Area: {cable.cross_sectional_area}")
        print()

        # Create bundles
        if len(express_cables):  # Checking if there are express cables to sort
            bundles = create_bundles(express_cables, start_stationing, end_stationing, bundles)
        if len(local_cables):    # Checking if there are local cables to sort
            bundles = create_bundles(local_cables, start_stationing, end_stationing, bundles)

    for start, end in stationing_text_pairs:
        print(f"Start: {start}, End: {end}")

    # Handle all text descriptors of stationing start and end
    # HANDLE ONLY TEXT DESCRIPTORS
    for start, end in stationing_text_pairs:

        # Create a list to store cables within the current stationing range
        cables_within_range = []

        for cable in cable_list:
            if cable.stationing_start == start and cable.stationing_end == end:
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

        # Create bundles
        if len(express_cables):  # Checking if there are express cables to sort
            bundles = create_bundles(express_cables, start, end, bundles)
        if len(local_cables):    # Checking if there are local cables to sort
            bundles = create_bundles(local_cables, start, end, bundles)

    if server_code_flag:
        logging.info("End of optimize_for_messenger function.")
        # logging.info("length of cable_list: %s", len(cable_list))

    return bundles


def create_new_bundle(start_stationing, end_stationing, bundle_nmbr, bundles):
    bundle = Bundle(start_stationing, end_stationing,
                    bundle_diameter=0, bundle_weight=0, bundle_number=bundle_nmbr)
    # Bundle diameter and weight will be updated every time a new cable is added
    print(f"[STATUS] Bundle {bundle.bundle_number} has been created")

    # Add newly made bundle to list of bundles
    bundles["Bundle" + str(bundle_nmbr)] = bundle

    if server_code_flag:
        logging.info("in create new bundle, length of bundles %s", len(bundles))

    return bundle, bundles


def add_cable_to_bundle(bundle, cable):
    # print(f"[STATUS] Adding Cable {cable.pull_number} ({cable.cable_size}) to Bundle {bundle.bundle_number}...")
    bundle.add_cable(cable)            # Add cable to bundle
    bundle.calculate_bundle_diameter_and_weight()    # Update total diameter and weight

    if cable.two_conductor is False:
        cable.x = cable.radius * math.cos(math.radians(cable.angle))
        cable.y = cable.radius * math.sin(math.radians(cable.angle))
    elif cable.two_conductor is True:
        cable.x = (cable.radius[0] * math.cos(math.radians(cable.angle[0])), cable.radius[1] * math.cos(math.radians(cable.angle[1])))
        cable.y = (cable.radius[0] * math.sin(math.radians(cable.angle[0])), cable.radius[1] * math.sin(math.radians(cable.angle[1])))


def create_bundles(cables_to_place, start_stationing, end_stationing, bundles):
    # Initialize a list to keep track of which cables are being placed in a bundle
    # to avoid double counting cables across bundles
    placed_cables = []
    global bundle_number

    if len(bundles) == 0:
        bundle_number = 1

    bundle, bundles = create_new_bundle(start_stationing, end_stationing, bundle_number, bundles)  # Create first bundle

    if server_code_flag:
        logging.info("bundle %s", bundle.bundle_number)

    # While there are cables to place
    while cables_to_place:
        cable = cables_to_place[0]  # Take the biggest cable from the list

        # If cable fits the conduit
        if check_diameter_and_weight(bundle, cable):
            add_cable_to_bundle(bundle, cable)      # Place cable into cable
            cables_to_place.remove(cable)           # Remove cable from list of cables to place
        # Else cable does not fit the conduit
        else:
            cable_placed = False

            # Go through the rest of the cables to place, to see if a smaller cable fits
            for cable in cables_to_place:
                # If a smaller cable fits
                if check_diameter_and_weight(bundle, cable):
                    add_cable_to_bundle(bundle, cable)    # Place cable into cable
                    cables_to_place.remove(cable)         # Remove cable from list of cables to place
                    cable_placed = True                   # Set flag to true that cable was placed
                    break
            # If no cables were able to be placed into the conduit
            if cable_placed is not True:
                # See if conduit can be smaller while maintaining 40% fill
                # tightly_resize_conduit(conduit)

                # Create a new bundle
                bundle, bundles = create_new_bundle(start_stationing, end_stationing, bundle.bundle_number + 1, bundles)
    # After all cables are placed, tighten the size of the last conduit made
    # tightly_resize_conduit(conduit)
    bundle_number = bundle.bundle_number + 1

    return bundles


def check_diameter_and_weight(bundle, cable):

    global max_bundle_weight

    bundle.bundle_weight += cable.weight

    # If added cable would make bundle overweight
    if bundle.bundle_weight > max_bundle_weight:
        bundle.bundle_weight -= cable.weight
        return 0

    # Find open space to place cable, do a check if that would have the bundle go over maximum diameter requirement
    # If added cable would not fit within diameter requirement
    if not find_open_space(bundle, cable):
        return 0

    # Indicate that cable can be added to bundle
    return 1


# Spiraling out from center to find placement
def find_open_space(bundle, cable):
    print(f"[STATUS] Finding open space for Cable {cable.pull_number}")

    # The radis and angle increments are how much you spiral out from the center
    radius_increment = 0.1  # Define the radius increment
    angle_increment = 5     # Define the angle increment

    # Initial placement at (radius=0, angle=0)
    radius = 0
    angle = 0

    max_radius = max_bundle_diameter/2

    # Function to calculate distance between two polar coordinates
    def calculate_distance(r1, a1, r2, a2):
        x1 = r1 * math.cos(math.radians(a1))
        y1 = r1 * math.sin(math.radians(a1))
        x2 = r2 * math.cos(math.radians(a2))
        y2 = r2 * math.sin(math.radians(a2))
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # Iterate through possible cable placements until a valid one is found or the bundle is full
    while True:
        # Initialize a flag to track cable overlap
        overlap = False

        # Check is prospective cable placement (radius, angle) would not cause overlap
        # with already placed cables in the bundle
        overlap = check_overlap(cable, bundle, radius, angle)

        # If no overlap is detected, proceed with cable placement
        if not overlap:
            # If two conductor cable, check if the second conductor of the two conductor cable can fit
            if cable.two_conductor is True:
                print(f"[STATUS] Placement found for first conductor. Coordinates: {round(radius, 2)}, {angle}"
                      f"\n          Finding placement for second conductor...")

                if place_second_conductor(cable, bundle, radius, angle):
                    # Second conductor was placed, return 1 to add cable to bundle
                    return 1
                else:
                    # Need to find new placement for first conductor
                    pass

            # Otherwise, whole cable was already placed, proceed updating coordinates for cable
            elif cable.two_conductor is False:
                # Call a function to add the new cable to the draw queue
                # bundle.add_cable(radius, angle)
                cable.radius = round(radius, 5)
                cable.angle = angle
                # Update bundle diameter to be the outermost point of outermost cable
                bundle.bundle_diameter = 2 * (cable.radius + (cable.diameter/2))
                print(f"\nCable {cable.pull_number} radius coordinate: {cable.radius}, cable radius: {cable.diameter/2}")
                # print(f"Adding up cable.radius + (cable.diameter/2): {(cable.radius + (cable.diameter/2)) * 2}")
                # print(f"[STATUS] Bundle {bundle.bundle_number} has an "
                #       f"updated diameter of {bundle.bundle_diameter} inches")
                # add_to_draw_queue(new_cable, (6/conduit_size) * radius, angle)
                print(f"[STATUS] Cable {cable.pull_number} was placed at {cable.radius}, {cable.angle}")
                return 1  # Return that a cable was placed

        # Increment angle by angle_increment
        if radius == 0:
            radius += radius_increment
        else:
            angle += angle_increment

        # Check if angle has completed a full circle (360 degrees)
        if angle >= 360:
            angle = angle % 360  # Reset angle to 0
            radius += radius_increment  # Increment radius, EDITED FROM += TO -= TO FIT CABLES VISUALLY

        # Check if the conduit is full, if the cable added would have the bundle go beyond 6 inches in diameter
        if radius + (cable.diameter/2) > max_radius:
            print(f"Failed: Bundle is full. Radius coordinate {radius} + Cable radius {cable.radius} > {max_radius}")
            return 0


def check_overlap(cable, bundle, radius, angle):

    def calculate_distance(r1, a1, r2, a2):
        x1 = r1 * math.cos(math.radians(a1))
        y1 = r1 * math.sin(math.radians(a1))
        x2 = r2 * math.cos(math.radians(a2))
        y2 = r2 * math.sin(math.radians(a2))
        # print(f"{math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)}")
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    for existing_cable in bundle.cables:
        # print(f"\nCable {cable.pull_number} is being compared against Cable {existing_cable.pull_number}")

        if existing_cable.two_conductor:
            # Calculate distance between cables
            distance = calculate_distance(radius, angle, existing_cable.radius[0], existing_cable.angle[0])

            # If the cables are overlapping
            if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                # Set overlap flag to true
                return True

            # Calculate distance between cables
            distance = calculate_distance(radius, angle, existing_cable.radius[1], existing_cable.angle[1])

            # If the cables are overlapping
            if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                # Set overlap flag to true
                return True
        else:
            # Calculate distance between cables
            distance = calculate_distance(radius, angle, existing_cable.radius, existing_cable.angle)

            # If the cables are overlapping
            if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                # Set overlap flag to true
                return True

    # If no overlap detected
    return False


def place_second_conductor(cable, bundle, radius, angle):
    print(f"\n---------------------------------------------------------------")
    print(f"[STATUS] Function place_second_conductor called for Cable {cable.pull_number}")

    # Distance multiplier for converting between absolute and relative coordinate system
    distance_multiplier = 166

    # Absolute radius, angle
    cable.radius = round(radius, 5)
    cable.angle = angle

    # Getting relative cartesian coordinates
    cable.x = round(radius * math.cos(math.radians(angle)), 5)
    cable.y = round(radius * math.sin(math.radians(angle)), 5)

    # Calculate x and y offset of the first conductor
    # First part of equation is the conversion to absolute (pdf) coordinates
    # For example, if a cable was placed at relative x,y of 1,0
    # then the absolute coordinates would be 666,500
    # x_offset would be 166, y_offset would be 0
    # x_offset_absolute = (500 + 166 * cable.x) - 500
    # y_offset_absolute = (500 + 166 * cable.y) - 500
    # x_offset_relative = None
    # y_offset_relative = None

    # Relative angle, have it facing inward to start, based on the absolute angle
    # Realistically there won't be clearance on the inner part,
    # But this function will incrementally move out on both directions
    # to find the next open space for the second conductor
    print(f"[STATUS] First conductor angle is {angle}, setting start angle to {angle + 180}")
    angle = cable.angle + 180    # start at 180
    # angle = cable.angle     # Start with angle that will definitely work for testing

    # Spacing of the second conductor away from the first conductor
    # Relative radius, relative to the first conductor
    # radius = radius + (cable.length-cable.width)
    radius = round((cable.length-cable.width), 4)

    # Overlap flag that will be set/reset by the check_overlap function
    overlap = True
    angle_increment = 0

    # While there isn't a second conductor placement
    while overlap is True:

        # Initialize to false; second conductor is good until it conflicts with another cable
        overlap = False

        # Convert the radius, angle of second conductor x and y,
        # where x and y will be relative to 0,0 aka the other placed cables
        x = round(radius * math.cos(math.radians(angle + angle_increment)) + cable.x, 5)    # Factor in x offset
        y = round(radius * math.sin(math.radians(angle + angle_increment)) + cable.y, 5)    # Factor in y offset
        print(f"R: {round(math.sqrt(x ** 2 + y ** 2), 2)}, θ: {round(math.degrees(math.atan2(y, x)), 4)}")

        r = math.sqrt(x ** 2 + y ** 2)
        theta = math.degrees(math.atan2(y, x))

        radius_convert = round(math.sqrt(x**2 + y**2), 4)
        angle_convert = round(math.degrees(math.atan2(y, x)), 4)

        for existing_cable in bundle.cables:
            if existing_cable.two_conductor is False:
                # Distance between second conductor and already placed cable
                distance = math.sqrt((x - existing_cable.x) ** 2 + (y - existing_cable.y) ** 2)
                print(f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x**2 + y**2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                      f"will work for placement against Cable {existing_cable.pull_number}...")
                print(f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable. y}")

                # If the cables are overlapping
                if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                    # The second conductor overlaps with a previously placed cable
                    print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                          f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                    overlap = True
                    break
                else:
                    print(f"[STATUS] Second conductor placement at {x}, {y} successful!")
            elif existing_cable.two_conductor is True:
                #  FIRST CONDUCTOR
                # Distance between second conductor and already placed cable
                distance = math.sqrt((x - existing_cable.x[0]) ** 2 + (y - existing_cable.y[0]) ** 2)
                print(
                    f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x ** 2 + y ** 2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                    f"will work for placement against Cable {existing_cable.pull_number}...")
                print(
                    f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable.y}")

                # If the cables are overlapping
                if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                    # The second conductor overlaps with a previously placed cable
                    print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                          f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                    overlap = True
                    break
                else:
                    print(f"[STATUS] Second conductor placement at {x}, {y} successful!")

                # SECOND CONDUCTOR
                # Distance between second conductor and already placed cable
                distance = math.sqrt((x - existing_cable.x[1]) ** 2 + (y - existing_cable.y[1]) ** 2)
                print(
                    f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x ** 2 + y ** 2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                    f"will work for placement against Cable {existing_cable.pull_number}...")
                print(
                    f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable.y}")

                # If the cables are overlapping
                if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                    # The second conductor overlaps with a previously placed cable
                    print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                          f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                    overlap = True
                    break
                else:
                    print(f"[STATUS] Second conductor placement at {x}, {y} successful!")

        # Conductor failed to place at angle + angle_increment, try at angle - angle_increment
        if overlap is True:
            # Initialize to false; second conductor is good until it conflicts with another cable
            overlap = False

            # Convert the radius, angle of second conductor x and y,
            # where x and y will be relative to 0,0 aka the other placed cables
            x = round(radius * math.cos(math.radians(angle - angle_increment)) + cable.x, 8)  # Factor in x offset
            y = round(radius * math.sin(math.radians(angle - angle_increment)) + cable.y, 8)  # Factor in y offset

            for existing_cable in bundle.cables:
                if existing_cable.two_conductor is False:
                    # Distance between second conductor and already placed cable
                    distance = math.sqrt((x - existing_cable.x) ** 2 + (y - existing_cable.y) ** 2)
                    print(
                        f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x ** 2 + y ** 2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                        f"will work for placement against Cable {existing_cable.pull_number}...")
                    print(
                        f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable.y}")
                    # If the cables are overlapping
                    if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                        # The second conductor overlaps with a previously placed cable
                        print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                              f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                        overlap = True
                        break
                    else:
                        print(f"[STATUS] Second conductor placement at {x}, {y} successful!")
                elif existing_cable.two_conductor is True:
                    # FIRST CONDUCTOR
                    # Distance between second conductor and already placed cable
                    distance = math.sqrt((x - existing_cable.x[0]) ** 2 + (y - existing_cable.y[0]) ** 2)
                    print(
                        f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x ** 2 + y ** 2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                        f"will work for placement against Cable {existing_cable.pull_number}...")
                    print(
                        f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable.y}")
                    # If the cables are overlapping
                    if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                        # The second conductor overlaps with a previously placed cable
                        print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                              f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                        overlap = True
                        break
                    else:
                        print(f"[STATUS] Second conductor placement at {x}, {y} successful!")

                    # SECOND CONDUCTOR
                    # Distance between second conductor and already placed cable
                    distance = math.sqrt((x - existing_cable.x[1]) ** 2 + (y - existing_cable.y[1]) ** 2)
                    print(
                        f"[STATUS] Testing if {x}, {y} \n            (Polar: {round(math.sqrt(x ** 2 + y ** 2), 4)}, {round(math.degrees(math.atan2(y, x)), 4)}) "
                        f"will work for placement against Cable {existing_cable.pull_number}...")
                    print(
                        f"[STATUS] Cable {existing_cable.pull_number} has coordinates {existing_cable.x}, {existing_cable.y}")
                    # If the cables are overlapping
                    if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                        # The second conductor overlaps with a previously placed cable
                        print(f"[STATUS] Cable placement at {x}, {y} failed\n"
                              f"Distance: {round(distance, 4)} < {((cable.diameter / 2) + (existing_cable.diameter / 2))}\n")
                        overlap = True
                        break
                    else:
                        print(f"[STATUS] Second conductor placement at {x}, {y} successful!")

        # If the second conductor placement would overlap with a cable already placed in the bundle
        if overlap is True and angle_increment is 360:
            # Second conductor was not able to be placed and the first conductor needs a new placement
            return False
        elif overlap is True:
            # Add 5 degrees to angle increment
            angle_increment += 15
        # If the placement of the second conductor would not conflict with previously placed cables
        elif overlap is False:
            # Set the radius,angle pairs for the two conductors of the cables,
            # adding the new radius and angle
            cable.radius = cable.radius, round(math.sqrt(x**2 + y**2), 4)

            second_conductor_angle = round(math.degrees(math.atan2(y, x)), 4)
            if x < 0:
                second_conductor_angle += 180

            cable.angle = cable.angle, second_conductor_angle
        # Second conductor was able to be placed
        return True

    print(f"---------------------------------------------------------------\n")
