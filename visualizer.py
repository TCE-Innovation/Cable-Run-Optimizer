from PIL import Image, ImageDraw, ImageFont
from file_handler import *
from cable_classes import *

def draw_cable(draw, x, y, cable, cable_info):
    scaling_factor = 50  # Increase the scaling factor
    offset_x = 20  # Offset in the x-direction
    offset_y = 20  # Offset in the y-direction
    text_margin = 10  # Decreased margin
    font_size = 12  # Larger font size
    text_color = "black"
    font = ImageFont.truetype("arial.ttf", font_size)  # Set the font size

    # Extract cable data attributes
    size = cable_info.size
    diameter = cable_info.diameter
    pounds_per_foot = cable_info.pounds_per_foot
    cross_sectional_area = cable_info.cross_sectional_area

    # Calculate the scaled radius based on the cable's diameter
    cable_radius = diameter * scaling_factor / 2

    # Calculate the coordinates for the center of the cable
    center_x = x
    center_y = y

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
    text_x = center_x - cable_radius + offset_x  # Add x-direction offset
    text_y = center_y - cable_radius - text_margin + offset_y  # Add y-direction offset

    text_lines = [
        f"S: {size}",
        f"D: {diameter}",
        f"CW: {pounds_per_foot}",
        f"A: {cross_sectional_area}",
    ]
    for line in text_lines:
        draw.text((text_x, text_y), line, fill=text_color, font=font)
        text_y += font_size + 10  # Adjust the vertical spacing


def generate_cable_image(cable_list):
    # Define the image size and other parameters
    image_size = (1000, 1000)  # Higher resolution image size
    dpi = (1000, 1000)  # Higher DPI (dots per inch)

    # Create a new image with a white background
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    # Loop through the cable_list and draw each cable
    for x, y, cable in cable_list:
        # Find the cable information from cable_sizes using cable's size as the key
        cable_info = None
        for info in cable_sizes:
            if info.size == cable.cable_size:
                cable_info = info
                break

        if cable_info is not None:
            # Call the draw_cable function to draw the cable and create the text label
            draw_cable(draw, x, y, cable, cable_info)

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
    num_grid_lines = 10  # Adjust the number of grid lines
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

    # Save the image to a file or display it
    image.save("cable_image.png", dpi=dpi)  # Higher resolution
    image.show()

    # Append cables to the cable_list


# Get the cable sizes
get_cable_sizes()

cable_list = [
    Cable('1.160', '500+00', '600+00', '7C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E'),
    Cable('1.161', '500+00', '600+00', '19C#14', 'E')
]

generate_cable_image(cable_list[0], 500, 500)