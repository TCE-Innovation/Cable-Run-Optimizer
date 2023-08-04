from cable_classes import stationing_values
from visualizer import *


# Take the stationing from the pull sheet and
# organize it into a numerically ordered list,
# where duplicate values are removed
def sort_stationing():
    global stationing_values

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


# With the sorted stationing, sort which cables
# are between each section between stationings
def stationing_sections():
    print()
    print("STATIONING SECTIONS")
    global stationing_values
    for i in range(len(stationing_values) - 1):
        start = stationing_values[i]
        end = stationing_values[i + 1]
        print(f"Cables between {start:.2f} and {end:.2f}:")
        for cable in cable_list:
            if (
                    (start <= float(cable.stationing_start.replace('+', '.')) < end)
                    or (start <= float(cable.stationing_end.replace('+', '.')) < end)
            ):
                print("-" + cable.pull_number)
        print()
