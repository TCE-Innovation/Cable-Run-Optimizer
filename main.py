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

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math

# user_interface()
get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
# sort_stationing()             # List each stationing value in the pull sheet, ordered
# optimize_for_conduit()        # Run conduit algorithm, generate conduit images
# generate_output_file()        # Create output excel file with generated conduits


def draw_graph(pdf_file_path):
    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Define the polar graph radius and center
    polar_graph_radius = min(letter) / 3
    center_x, center_y = letter[0] / 2, letter[1] / 2

    # Draw red dot in the center
    dot_radius = 2
    c.setFillColorRGB(1, 0, 0)  # Red color
    c.circle(center_x, center_y, dot_radius, fill=1)

    # Draw lines extending from the center
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

    # Draw grid lines
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


def draw_polar_graph(pdf_file_path):
    c = canvas.Canvas(pdf_file_path, pagesize=letter)

    # Define the polar graph radius and center
    polar_graph_radius = min(letter) / 3
    center_x, center_y = letter[0] / 2, letter[1] / 2

    # Draw red dot in the center
    dot_radius = 2
    c.setFillColorRGB(1, 0, 0)  # Red color
    c.circle(center_x, center_y, dot_radius, fill=1)

    # Draw lines extending from the center
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

    # Draw grid lines
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

    cable = cable_list[0]  # Assuming there's at least one cable in the list
    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.setLineWidth(2*34)  # Line width
    c.circle(center_x, center_y, cable.diameter / 2, stroke=1)


    c.showPage()  # Add a new blank page

    # Define the polar graph radius and center
    polar_graph_radius = min(letter) / 3
    center_x, center_y = letter[0] / 2, letter[1] / 2

    # Draw red dot in the center
    dot_radius = 2
    c.setFillColorRGB(1, 0, 0)  # Red color
    c.circle(center_x, center_y, dot_radius, fill=1)

    # Draw lines extending from the center
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

    # Draw grid lines
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

    # draw_graph("polar_graph.pdf")

    # Draw the same image with the second cable on the new page
    cable = cable_list[1]  # Assuming there's at least two cables in the list
    c.setStrokeColorRGB(0, 0, 1)  # Blue color
    c.setLineWidth(2*34)  # Line width
    c.circle(center_x, center_y, cable.diameter / 2, stroke=1)

    # CHAT GPT ADD CODE AFTER THIS COMMENT

    # CHAT GPT ADD CODE BEFORE THIS COMMENT

    c.save()

    # Open the generated PDF
    subprocess.Popen(["start", pdf_file_path], shell=True)

draw_polar_graph("polar_graph.pdf")

