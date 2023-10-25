from settings import local_code_flag
from settings import server_code_flag
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
    # Initialize a list to keep track of which cables are being placed in a conduit
    # to avoid double counting cables across conduits
    placed_cables = []
    global bundle_number

    if len(bundles) == 0:
        bundle_number = 1

    bundle, bundles = create_new_bundle(start_stationing, end_stationing, bundle_number, bundles)  # Create first conduit

    if server_code_flag:
        logging.info("bundle %s", bundle.bundle_number)

    # While there are cables to place
    while cables_to_place:
        cable = cables_to_place[0]  # Take the biggest cable from the list

        # If cable fits the conduit
        if check_free_air_space(bundle, cable):
            add_cable_to_bundle(bundle, cable)    # Place cable into cable
            cables_to_place.remove(cable)           # Remove cable from list of cables to place
        # Else cable does not fit the conduit
        else:
            cable_placed = False

            # Go through the rest of the cables to place, to see if a smaller cable fits
            for cable in cables_to_place:
                # If a smaller cable fits
                if check_free_air_space(bundle, cable):
                    add_cable_to_bundle(bundle, cable)    # Place cable into cable
                    cables_to_place.remove(cable)                # Remove cable from list of cables to place
                    cable_placed = True                     # Set flag to true that cable was placed
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


# Work backwards, compare conduit fill of potential downsized conduits
# Keep working until before fill of 40% or higher is reached
def tightly_resize_conduit(conduit):
    pass


def check_free_air_space(conduit, cable):
    pass
