from file_handler import *
from user_interface import *
from messenger_algorithm import *
from conduit_algorithm import *
from cable_classes import *
from visualizer import get_cable_pull_sheet
from reportlab.platypus import SimpleDocTemplate, PageBreak
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, PageBreak
import subprocess
import math
import random

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math

# user_interface()
get_cable_sizes()               # Excel of all cables and their parameters
get_cable_pull_sheet()          # Pull sheet excel
sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit()        # Run conduit algorithm, generate conduit images
generate_output_file()        # Create output excel file with generated conduits


def draw_graph_common(c, center_x, center_y):
    # Define the polar graph radius
    polar_graph_radius = min(letter) / 3

    # Draw common graph elements
    dot_radius = 2
    c.setFillColorRGB(1, 0, 0)  # Red color
    c.circle(center_x, center_y, dot_radius, fill=1)

    num_lines = 12
    angle_spacing = 2 * math.pi / num_lines
    for i in range(num_lines):
        angle = i * angle_spacing
        line_start = (
            center_x + dot_radius * math.cos(angle),
            center_y + dot_radius * math.sin(angle),
        )
        line_end = (
            center_x + polar_graph_radius * math.cos(angle),
            center_y + polar_graph_radius * math.sin(angle),
        )
        c.line(line_start[0], line_start[1], line_end[0], line_end[1])

    num_grid_lines = 6
    radius_spacing = polar_graph_radius / num_grid_lines
    for i in range(num_grid_lines):
        radius = (i + 1) * radius_spacing
        c.circle(center_x, center_y, radius, stroke=1)

    for theta in range(0, 360, 10):
        theta_rad = math.radians(theta)
        line_start = (
            center_x + polar_graph_radius * math.cos(theta_rad),
            center_y + polar_graph_radius * math.sin(theta_rad),
        )
        line_end = (
            center_x + polar_graph_radius * math.cos(theta_rad),
            center_y + polar_graph_radius * math.sin(theta_rad),
        )
        c.line(line_start[0], line_start[1], line_end[0], line_end[1])


def draw_graph():
    pdf_file_path = "Conduit_Optimization.pdf"  # Define the PDF file path within the function

    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Define the polar graph radius and center
    center_x, center_y = letter[0] / 2, letter[1] / 2

    draw_graph_common(c, center_x, center_y)
    cable = cable_list[0]  # Assuming there's at least one cable in the list
    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.setLineWidth(2 * 34)  # Line width
    c.circle(center_x, center_y, cable.diameter / 2, stroke=1)
    c.showPage()  # Add a new blank page

    draw_graph_common(c, center_x, center_y)  # Call the common function again

    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.setLineWidth(2 * 34)  # Line width

    # Draw the second cable
    # cable = cable_list[1]  # Assuming there's at least two cables in the list

    for cable in cable_list:
        c.circle(center_x + random.randint(-150, 150), center_y + random.randint(-150, 150), cable.diameter / 2, stroke=1)

    c.save()

    # Open the generated PDF
    subprocess.Popen(["start", pdf_file_path], shell=True)


# draw_graph()
