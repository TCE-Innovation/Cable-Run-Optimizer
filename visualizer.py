from PIL import Image, ImageDraw, ImageFont
from cable_classes import *
import math
from PyPDF2 import PdfReader, PdfWriter
import os


# Define image size and dpi
image_size = (1000, 1000)  # Higher resolution image size
dpi = (121, 121)  # DPI to scale size of file, with the aim to not need to zoom in/out


# This function draws individual cables, and is called by generate_cable_image
def draw_cable(draw, radius, angle_deg, cable, polar_center):
    # scaling_factor = 82                   # Increase the scaling factor
    scaling_factor = 82 * (6/conduit_size) + 3  # Increase the scaling factor
    text_margin_x = -40                     # Cable info text x
    text_margin_y = -40                     # Cable info text y
    text_color = "black"

    # Set the font size
    font_size = 12
    font = ImageFont.truetype("arial.ttf", font_size)

    # Convert the angle from degrees to radians
    angle_rad = math.radians(360 - angle_deg)

    # Extract cable data attributes
    pull_number = cable.pull_number
    size = cable.cable_size
    diameter = cable.diameter
    pounds_per_foot = cable.weight
    cross_sectional_area = cable.cross_sectional_area
    express = cable.express

    # Calculate the scaled radius based on the cable's diameter
    cable_radius = diameter * scaling_factor

    # Calculate the polar coordinates for the center of the circle
    center_x = polar_center[0] + radius * math.cos(angle_rad)
    center_y = polar_center[1] + radius * math.sin(angle_rad)

    # Draw the cable as a filled circle
    cable_color = "#3dbac2"  # Teal
    cable_bbox = (
        center_x - cable_radius,
        center_y - cable_radius,
        center_x + cable_radius,
        center_y + cable_radius,
    )
    draw.ellipse(cable_bbox, fill=cable_color)

    # Create a text label with the cable information
    text_x = center_x - cable_radius - text_margin_x    # Add x-direction offset
    text_y = center_y - cable_radius - text_margin_y    # Add y-direction offset

    text_lines = [
        f"P: {pull_number}",
        f"E: {express}",
        f"S: {size}",
        f"D: {diameter}",
        f"CW: {pounds_per_foot}",
        f"A: {cross_sectional_area}",
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 5  # Adjust the vertical spacing


# This function draws everything but the individual cables,
# including the graph and text at the top left
# This function calls draw_cable()
def generate_cable_image(draw_queue):
    global first_file_flag
    # Create a new image with a white background
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    # Overlay polar coordinate graph
    polar_graph_radius = min(image_size) // 2
    polar_graph_center = (image_size[0] // 2, image_size[1] // 2)

    # Draw red dot in the center
    dot_radius = 5
    draw.ellipse(
        (
            polar_graph_center[0] - dot_radius,
            polar_graph_center[1] - dot_radius,
            polar_graph_center[0] + dot_radius,
            polar_graph_center[1] + dot_radius,
        ),
        fill="red",
        outline="red",
    )

    # Draw lines extending from the center
    num_lines = 12  # Adjust the number of lines
    angle_spacing = 2 * math.pi / num_lines  # Calculate the angle spacing between lines
    for i in range(num_lines):
        angle = i * angle_spacing
        line_start = (
            polar_graph_center[0] + dot_radius * math.cos(angle),
            polar_graph_center[1] + dot_radius * math.sin(angle),
        )
        line_end = (
            polar_graph_center[0] + polar_graph_radius * math.cos(angle),
            polar_graph_center[1] + polar_graph_radius * math.sin(angle),
        )
        draw.line([line_start, line_end], fill="black", width=1)

    # Draw grid lines
    num_grid_lines = 6  # Adjust the number of grid lines
    radius_spacing = polar_graph_radius / num_grid_lines  # Calculate the spacing between grid lines
    for i in range(num_grid_lines):
        radius = (i + 1) * radius_spacing
        draw.ellipse(
            (
                polar_graph_center[0] - radius,
                polar_graph_center[1] - radius,
                polar_graph_center[0] + radius,
                polar_graph_center[1] + radius,
            ),
            outline="black",
            width=1,
        )

    for theta in range(0, 360, 10):
        theta_rad = math.radians(theta)
        line_start = (
            polar_graph_center[0] + polar_graph_radius * math.cos(theta_rad),
            polar_graph_center[1] + polar_graph_radius * math.sin(theta_rad),
        )
        line_end = (
            polar_graph_center[0] + polar_graph_radius * math.cos(theta_rad),
            polar_graph_center[1] + polar_graph_radius * math.sin(theta_rad),
        )
        draw.line([line_start, line_end], fill="black", width=1)

    # Loop through the draw_queue and draw each cable
    for radius, angle_deg, cable in draw_queue:
        draw_cable(draw, radius * 166, angle_deg, cable, polar_graph_center)
    # 166 relates to spacing of cables apart from each other


    # DRAWING THE LINES OVER THE CABLES TO SEE SCALING PROPERLY
    # Draw grid lines
    num_grid_lines = 6  # Adjust the number of grid lines
    radius_spacing = polar_graph_radius / num_grid_lines  # Calculate the spacing between grid lines
    for i in range(num_grid_lines):
        radius = (i + 1) * radius_spacing
        draw.ellipse(
            (
                polar_graph_center[0] - radius,
                polar_graph_center[1] - radius,
                polar_graph_center[0] + radius,
                polar_graph_center[1] + radius,
            ),
            outline="black",
            width=1,
        )

    num_lines = 12  # Adjust the number of lines
    angle_spacing = 2 * math.pi / num_lines  # Calculate the angle spacing between lines
    for i in range(num_lines):
        angle = i * angle_spacing
        line_start = (
            polar_graph_center[0] + dot_radius * math.cos(angle),
            polar_graph_center[1] + dot_radius * math.sin(angle),
        )
        line_end = (
            polar_graph_center[0] + polar_graph_radius * math.cos(angle),
            polar_graph_center[1] + polar_graph_radius * math.sin(angle),
        )
        draw.line([line_start, line_end], fill="black", width=1)
    # END DRAWING THE LINES OVER THE CABLES TO SEE SCALING PROPERLY


    global conduit_number
    # Write "Scale: " text at the bottom left of the image
    scale_text = "Scale: 0.5 inches/radius increment"
    conduit_size_text = f"Conduit Size: {conduit_size} inches"
    conduit_number_text = f"Conduit: {conduit_number}"

    from conduit_algorithm import stationing_start_text
    from conduit_algorithm import stationing_end_text
    stationing_start_text = f"Start: {stationing_start_text}"
    stationing_end_text = f"End: {stationing_end_text}"

    # from conduit_algorithm import conduit_free_air_space
    # conduit_free_air_space_text = f"{conduit_free_air_space}"

    from conduit_algorithm import express_text
    from conduit_algorithm import conduit_free_air_space
    #
    text_color = "black"
    font_size = 15
    font = ImageFont.truetype("arial.ttf", font_size)

    # Text printed at the top left part of the image
    text_x = 5
    # text_y = image_size[1] - font_size - 10
    text_y = 5

    text_lines = [
        f"Scale: {conduit_size/12} inches/radius increment",
        f"Conduit Size: {conduit_size} inches",
        # f"Conduit Fill: {round(100 - conduit_free_air_space, 2)}%",
        f"Conduit Fill: {100 - conduit_free_air_space:.2f}%",
        f"Start: {stationing_start_text}",
        f"End: {stationing_end_text}",
        f"Conduit: {conduit_number}",
        express_text
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 5  # Adjust the vertical spacing

    conduit_number += 1

    temp_pdf_file = "Conduit temp file.pdf"
    image.save(temp_pdf_file, dpi=dpi)  # Higher resolution

    if first_file_flag:
        output_pdf_file = "Optimization Results.pdf"
        # input_pdf_file = "Conduit.pdf"

        # Create a PDF writer object
        pdf_writer = PdfWriter()

        # Open the existing PDF file and add its pages to the writer object
        with open(output_pdf_file, "rb") as existing_pdf:
            pdf_reader = PdfReader(existing_pdf)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)  # Add the existing page

        # Open the temporary PDF and add its pages to the writer object
        with open(temp_pdf_file, "rb") as temp_pdf:
            pdf_reader = PdfReader(temp_pdf)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

        # Save the merged PDF
        with open(output_pdf_file, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

    else:
        first_file_flag = True
        file_path = r"C:\Users\roneill\OneDrive - Iovino Enterprises, LLC" \
                    r"\Documents 1\Code\Git Files\Cable-Run-Optimizer"
        file_name = "Optimization Results.pdf"
        full_file_path = os.path.join(file_path, file_name)
        image.save(full_file_path, dpi=dpi)  # Higher resolution


def add_to_draw_queue(cable, radius, angle_deg):
    draw_queue.append((radius, angle_deg, cable))