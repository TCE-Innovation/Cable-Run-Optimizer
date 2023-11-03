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

        # Sort express and local cables separately, sorting by size
        ###################################################################################
        # EDIT THIS CODE SO THAT CABLES ARE SORTED BASED ON WHEN THEY WILL EXIT THE BUNDLE,
        # THEN FOR CABLES THAT HAVE SAME DROP OFF POINT, SORT BY SIZE
        ###################################################################################
        express_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)
        local_cables.sort(key=lambda cable: cable.cross_sectional_area, reverse=True)

        # Print the sorted express cables
        print("[INFO] Sorted Express Cables:")
        for cable in express_cables:
            print(f"Pull #: {cable.pull_number}, Cable Size: {cable.cable_size}")
        print()

        # Create bundles
        if len(express_cables):  # Checking if there are express cables to sort
            bundles = create_bundles(express_cables, start_stationing, end_stationing, bundles)
        if len(local_cables):    # Checking if there are local cables to sort
            bundles = create_bundles(local_cables, start_stationing, end_stationing, bundles)

    for start, end in stationing_text_pairs:
        print(f"Start: {start}, End: {end}")

    # Handle all text descriptors of stationing start and end
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
        logging.info("length of cable_list: %s", len(cable_list))

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
    print(f"[STATUS] Adding Cable {cable.pull_number} ({cable.cable_size}) to Bundle {bundle.bundle_number}...")
    bundle.add_cable(cable)            # Add cable to bundle
    bundle.calculate_bundle_diameter_and_weight()    # Update total diameter and weight

    # placed_cables.append(cable)         # Add cable to list of placed cables

    # return placed_cables


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
    if not find_open_space(bundle, cable):
        return 0

    # Indicate that cable can be added to bundle
    return 1


# Spiraling out from center to find placement
def find_open_space(bundle, cable):

    # Skip over this for two conductor cables
    # Just want to see this added to conduit, not interested in visualizing rn
    if cable.diameter is None:
        bundle.add_cable(cable, None, None)
    else:
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

            # Iterate through existing cables in the conduit
            for existing_cable in bundle.cables:
                # Calculate distance between cables
                distance = calculate_distance(radius, angle, existing_cable.radius, existing_cable.angle)

                # If the cables are overlapping
                if distance < ((cable.diameter / 2) + (existing_cable.diameter / 2)):
                    overlap = True  # Set the overlap flag to True
                    break           # Exit the loop since overlap is detected

            # If no overlap is detected, proceed with cable placement
            if not overlap:
                # Call a function to add the new cable to the draw queue
                # bundle.add_cable(radius, angle)
                cable.radius = round(radius , 5)
                cable.angle = angle
                bundle.bundle_diameter = 2 * (cable.radius + (cable.diameter/2))
                print(f"\nCable radius coordinate: {cable.radius}, cable radius: {cable.diameter/2}")
                print(f"Adding up cable.radius + (cable.diameter/2): {(cable.radius + (cable.diameter/2)) * 2}")
                print(f"[STATUS] Bundle {bundle.bundle_number} has an updated diameter of {bundle.bundle_diameter} inches")
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

    # Add logic checking if cable goes over radius requirement
    # If goes over, return 0, if it fits, return 1

    return 1