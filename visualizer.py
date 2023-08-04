from PIL import Image, ImageDraw, ImageFont
from cable_classes import *
from file_handler import *
from cable_classes import *
import math

# Define image size and dpi
image_size = (1000, 1000)  # Higher resolution image size
dpi = (1000, 1000)  # Higher DPI (dots per inch)


def draw_cable(draw, radius, angle_deg, cable, cable_info, polar_center):
    radius = radius * 50
    scaling_factor = 166.6667  # Increase the scaling factor
    offset_radius = 20  # Offset in the radial direction
    offset_angle_deg = 0  # No angle offset
    text_margin = 10  # Decreased margin
    font_size = 12  # Larger font size
    text_color = "black"
    font = ImageFont.truetype("arial.ttf", font_size)  # Set the font size

    # Convert the angle from degrees to radians
    angle_rad = math.radians(360 - angle_deg)

    # Extract cable data attributes
    size = cable_info.size
    diameter = cable_info.diameter
    pounds_per_foot = cable_info.pounds_per_foot
    cross_sectional_area = cable_info.cross_sectional_area

    # Calculate the scaled radius based on the cable's diameter
    cable_radius = diameter * scaling_factor / 2

    # Calculate the polar coordinates for the center of the circle
    center_x = polar_center[0] + radius * math.cos(angle_rad)
    center_y = polar_center[1] + radius * math.sin(angle_rad)

    # Draw the cable as a filled circle
    cable_color = "#B2ABB3"  # Darker shade of gray
    cable_bbox = (
        center_x - cable_radius,
        center_y - cable_radius,
        center_x + cable_radius,
        center_y + cable_radius,
    )
    draw.ellipse(cable_bbox, fill=cable_color)

    # Create a text label with the cable information
    text_x = center_x - cable_radius  # No x-direction offset
    text_y = center_y - cable_radius - text_margin  # Add y-direction offset

    text_lines = [
        f"S: {size}",
        f"D: {diameter}",
        f"CW: {pounds_per_foot}",
        f"A: {cross_sectional_area}",
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 10  # Adjust the vertical spacing


def generate_cable_image(draw_queue):
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
    for radius, angle_deg, cable, cable_info in draw_queue:
        draw_cable(draw, radius, angle_deg, cable, cable_info, polar_graph_center)

    # Write "Scale: " text at the bottom left of the image
    scale_text = "Scale: 0.5 inches/radius increment"
    text_color = "black"
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)
    text_x = 10
    text_y = image_size[1] - font_size - 10
    draw.text((text_x, text_y), scale_text, fill=text_color, font=font)

    # Save the image to a file or display it
    image.save("cable_image.png", dpi=dpi)  # Higher resolution
    image.show()


def add_to_draw_queue(cable, radius, angle_deg):
    # Iterate through the list of cable objects
    for cable_obj in cable_list:
        # Check if the current cable object matches the provided cable
        if cable_obj == cable:
            # Initialize a variable to store cable information
            cable_info = None
            # Iterate through the list of cable size information
            for info in cable_sizes:
                # Check if the cable size matches the size of the current cable object
                if info.size == cable_obj.cable_size:
                    # If a match is found, store the cable size information
                    cable_info = info
                    # Exit the loop since we found the relevant cable size
                    break
            # Check if cable information was found
            if cable_info is not None:
                # Add cable information to the draw queue
                # This includes the radius, angle, cable object, and cable size details
                draw_queue.append((radius, angle_deg, cable_obj, cable_info))
            # Exit the loop since we found the relevant cable object
            break


# Draw each cable with specified coordinates, radius, angle
# add_to_draw_queue(cable_list[5], 5, 30)
# add_to_draw_queue(cable_list[6], 0, 0)

# Generate the final image
# generate_cable_image(draw_queue)
