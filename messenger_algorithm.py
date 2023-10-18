from cable_classes import *
from file_handler import *
from visualizer import *

# 6 inches diameter, 20 lb/ft weight

# Check if next cable placement will overlap with currently placed cables
def check_for_overlap(cable, radius, angle):
    overlap = False

    if not overlap:
        add_to_draw_queue(cable, radius, angle)
    else:
        return 1


def find_open_space():
    pass