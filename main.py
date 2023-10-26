from settings import *

# Running code on local machine
if local_code_flag:

    from conduit_algorithm import *
    from messenger_algorithm import *
    from file_handler import *
    from cable_classes import *

    print("[START] Running local code...")

    # Obtain list of cables that the tool can optimize for, from Cable Sizes.xlsx
    cable_sizes_list = get_cable_sizes()

    # Obtain list of cable from pull sheet to optimize
    cable_list = get_cable_pull_sheet(cable_list, cable_sizes_list)

    # Sort through stationing values in pull sheet, either numerical or simple text descriptors
    stationing_values_numeric, stationing_text_pairs = sort_stationing(cable_list)

    # Flag pulled from settings.py to choose which type of cable optimization to perform
    if run_conduit_optimization:
        # Perform optimization
        conduits = optimize_for_conduit(stationing_values_numeric, stationing_text_pairs, cable_list)

        # Create output Excel file with generated conduits
        generate_output_file_for_conduit(conduits)

    elif run_messenger_optimization:
        # Perform optimization
        bundles = optimize_for_messenger(stationing_values_numeric, stationing_text_pairs, cable_list)

        # Create output Excel file with generated bundles
        generate_output_file_for_messenger(bundles)

# Running code on TCIG.nyc website
elif server_code_flag:

    from .conduit_algorithm import *
    from .messenger_algorithm import *
    from .file_handler import get_cable_pull_sheet, get_cable_sizes, sort_stationing, generate_output_file
    from .cable_classes import *
    import logging

    def execute_CRO(pull_sheet, cable_sizes, bytes_flag):
        logging.info("Running execute_CRO main function.")

        # Obtain list of cables that the tool can optimize for, from Cable Sizes.xlsx
        logging.info("Running get_cable_sizes().")
        cable_sizes_list = get_cable_sizes(cable_sizes, bytes_flag)

        # Obtain list of cable from pull sheet to optimize
        logging.info("Running get_cable_pull_sheet().")
        cable_list = get_cable_pull_sheet(pull_sheet, cable_sizes_list)

        # Sort through stationing values in pull sheet, either numerical or simple text descriptors
        logging.info("Sorting stationing values.")
        stationing_values_numeric, stationing_text_pairs = sort_stationing(cable_list)

        if run_conduit_optimization:
            logging.info("Optimizing for conduit.")
            conduits = optimize_for_conduit(stationing_values_numeric, stationing_text_pairs, cable_list)
            logging.info("after opt con conduits list %s", len(conduits))

            logging.info("Generating output file.")
            sas_url = generate_output_file_for_conduit(conduits)

        elif run_messenger_optimization:
            logging.info("Optimizing for messenger.")
            bundles = optimize_for_messenger(stationing_values_numeric, stationing_text_pairs, cable_list)
            logging.info("after opt con conduits list %s", len(bundles))

            logging.info("Generating output file.")
            sas_url = generate_output_file_for_messenger(bundles)

        return sas_url