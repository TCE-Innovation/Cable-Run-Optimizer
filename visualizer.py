from PIL import Image, ImageDraw, ImageFont
from cable_classes import *
import math
from PyPDF2 import PdfReader, PdfWriter
import os


# Define image size and dpi
image_size = (1000, 1000)  # Higher resolution image size
dpi = (121, 121)  # DPI to scale size of file, with the aim to not need to zoom in/out


# This function draws individual cables, and is called by generate_cable_image
# def draw_cable(draw, radius, angle_deg, cable, polar_center):
def draw_cable(draw, cable):

    # scaling factor determines how big the cables are going to be drawn.
    # scaling_factor = 82 * (6/max_bundle_diameter) + 3
    scaling_factor = 82         # Scaling factor of 82 for diameter of 6 inches
    distance_multiplier = 166   # Convert distance to be on the scale of the image
    text_margin_x = -50         # Cable info text x
    text_margin_y = -50         # Cable info text y
    text_color = "black"

    # Set the font size
    font_size = 14
    font = ImageFont.truetype("arial.ttf", font_size)

    # Convert the angle from degrees to radians
    # angle_rad = math.radians(360 - cable.radius)
    print(f"The cable's radius in degrees is {cable.angle}")
    angle_rad = math.radians(360 - cable.angle)
    print(f"The cable's radius in radians is {angle_rad}")
    # cable.angle = math.radians(360 - cable.radius)

    # Calculate the scaled radius based on the cable's diameter
    # cable_radius = cable.diameter * scaling_factor

    print(f"Cartesian x coordinate: {cable.radius * math.cos(angle_rad)}")
    print(f"Cartesian y coordinate: {cable.radius * math.sin(angle_rad)}")

    # Calculate the polar coordinates for the center of the circle
    center_x = 500 + distance_multiplier * cable.radius * math.cos(angle_rad)
    center_y = 500 + distance_multiplier * cable.radius * math.sin(angle_rad)
    # center_x = 500 + cable.radius * math.cos(cable.angle)
    # center_y = 500 + cable.radius * math.sin(cable.angle)

    # Calculate the polar coordinates for the center of the circle
    # center_x = polar_center[0] + cable.radius * math.cos(166*cable.angle)
    # print(f"CENTER_X IS A VALUE OF {center_x}")
    # center_y = polar_center[1] + cable.radius * math.sin(166*cable.angle)
    # print(f"CENTER_Y IS A VALUE OF {center_y}")
    # center_x = 500
    # center_y = 500

    # Draw the cable as a filled circle
    cable_color = "#20df35"  # Teal
    cable_radius = cable.diameter * scaling_factor

    cable_bbox = (
        center_x - cable_radius,
        center_y - cable_radius,
        center_x + cable_radius,
        center_y + cable_radius,
    )
    draw.ellipse(cable_bbox, fill=cable_color)

    # Draw a red circle at the center of the cable
    circle_radius = 1.5
    circle_color = "red"
    circle_center = (center_x, center_y)
    circle_bbox = (
        circle_center[0] - circle_radius,
        circle_center[1] - circle_radius,
        circle_center[0] + circle_radius,
        circle_center[1] + circle_radius,
    )
    draw.ellipse(circle_bbox, fill=circle_color, outline=circle_color)

    # Create a text label with the cable information
    # text_x = center_x - cable_radius - text_margin_x    # Add x-direction offset
    # text_y = center_y - cable_radius - text_margin_y    # Add y-direction offset
    text_x = center_x - text_margin_x    # Add x-direction offset
    text_y = center_y - text_margin_y    # Add y-direction offset

    text_lines = [
        f"P: {cable.pull_number}",
        f"E: {cable.express}",
        f"S: {cable.cable_size}",
        f"D: {cable.diameter} inches",
        f"W: {cable.weight}",
        # f"A: {cable.cross_sectional_area}",
        f"R, θ: {cable.radius}, {cable.angle}"
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 5  # Adjust the vertical spacing


# This function draws everything but the individual cables,
# including the graph and text at the top left
# This function calls draw_cable()
def generate_cable_image(bundle):
    print(f"\n[STATUS] Running Visualizer on Bundle {bundle.bundle_number}...")

    # global first_file_flag
    # first_file_flag = False

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
    # for radius, angle_deg, cable in draw_queue:
        # draw_cable(draw, radius * 166, angle_deg, cable, polar_graph_center)
    # 166 relates to spacing of cables apart from each other

    for cable in bundle.cables:
        # draw_cable(draw, cable.radius * 166, cable.angle, cable)
        draw_cable(draw, cable)


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

    # Draw red dot in the center
    dot_radius = 4
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



    # END DRAWING THE LINES OVER THE CABLES TO SEE SCALING PROPERLY


    # global conduit_number
    # Write "Scale: " text at the bottom left of the image
    scale_text = "Scale: 0.5 inches/radius increment"
    # conduit_size_text = f"Conduit Size: {conduit_size} inches"
    # conduit_number_text = f"Conduit: {conduit_number}"

    # from conduit_algorithm import stationing_start_text
    # from conduit_algorithm import stationing_end_text
    # stationing_start_text = f"Start: {stationing_start_text}"
    # stationing_end_text = f"End: {stationing_end_text}"

    # from conduit_algorithm import conduit_free_air_space
    # conduit_free_air_space_text = f"{conduit_free_air_space}"

    # from conduit_algorithm import express_text
    # from conduit_algorithm import conduit_free_air_space
    #
    text_color = "black"
    font_size = 15
    font = ImageFont.truetype("arial.ttf", font_size)

    # Text printed at the top left part of the image
    text_x = 5
    # text_y = image_size[1] - font_size - 10
    text_y = 5

    text_lines = [
        f"Scale: TEST inches/radius increment",
        # f"Conduit Size: {conduit_size} inches",
        # f"Conduit Fill: {round(100 - conduit_free_air_space, 2)}%",
        # f"Conduit Fill: {100 - conduit_free_air_space:.2f}%",
        # f"Start: {stationing_start_text}",
        # f"End: {stationing_end_text}",
        # f"Conduit: {conduit_number}",
        # express_text
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 5  # Adjust the vertical spacing

    # conduit_number += 1

    temp_pdf_file = "Conduit temp file.pdf"
    image.save(temp_pdf_file, dpi=dpi)  # Higher resolution

    if bundle.bundle_number != 1:
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
        file_path = r"C:\Users\roneill\OneDrive - Iovino Enterprises, LLC" \
                    r"\Documents 1\Code\Git Files\Cable-Run-Optimizer"
        file_name = "Optimization Results.pdf"
        full_file_path = os.path.join(file_path, file_name)
        image.save(full_file_path, dpi=dpi)  # Higher resolution


# def add_to_draw_queue(cable, radius, angle_deg):
#     draw_queue.append((radius, angle_deg, cable))
