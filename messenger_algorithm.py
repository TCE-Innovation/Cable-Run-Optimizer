from cable_classes import cable_list

# Take the stationing from the pull sheet and
# organize it into a numerically ordered list,
# where duplicate values are removed
def sort_stationing():
    # Initialize an empty set to store unique stationing values
    stationing_values = set()

    for cable in cable_list:
        if cable.stationing_start:
            start_value = float(cable.stationing_start.replace('+', '.'))
            stationing_values.add(start_value)

        if cable.stationing_end:
            end_value = float(cable.stationing_end.replace('+', '.'))
            stationing_values.add(end_value)

    # Sort the values numerically
    stationing_values = sorted(stationing_values)

    # Print the stationing values with two decimal places
    print("Stationing Values:")
    for value in stationing_values:
        print(f"{value:.2f}")