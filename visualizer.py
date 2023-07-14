# from cable_classes import *
# from user_interface import *
# from file_handler import *
# from PIL import Image, ImageDraw, ImageFont
#
#
# def generate_cable_image(cables):
#     # Define the image size and other parameters
#     image_size = (1000, 900)  # Higher resolution image size
#     text_margin = 50
#     font_size = 12  # Larger font size
#
#     # Calculate the quadrant size based on the image size
#     quadrant_size = (image_size[0] // 2, image_size[1] // 2)
#
#     # Create a new image with a white background
#     image = Image.new("RGB", image_size, "white")
#     draw = ImageDraw.Draw(image)
#
#     for i, cable in enumerate(cables):
#         # Calculate the scaled radius based on the cable's diameter
#         diameter = cable.diameter
#         scaling_factor = 150  # Increase the scaling factor
#         cable_radius = diameter * scaling_factor / 2  # Adjust the scaling factor here
#
#         # Calculate the coordinates for the center of the quadrant based on the index
#         center_x = (i % 2) * quadrant_size[0] + quadrant_size[0] // 2
#         center_y = (i // 2) * quadrant_size[1] + quadrant_size[1] // 2
#         center = (center_x, center_y)
#
#         # Draw the cable as a filled circle with a border
#         cable_color = "black"
#         cable_outline_color = "black"
#         cable_outline_width = 5  # Thicker outline
#         cable_bbox = (
#             center[0] - cable_radius,
#             center[1] - cable_radius,
#             center[0] + cable_radius,
#             center[1] + cable_radius,
#         )
#         draw.ellipse(cable_bbox, outline=cable_outline_color, width=cable_outline_width)
#
#         # Create a text label with the cable information
#         text_x = center_x - cable_radius
#         text_y = center_y + cable_radius + text_margin
#         text_color = "black"
#         font = ImageFont.truetype("arial.ttf", font_size)  # Set the font size
#         text_lines = [
#             f"Size: {cable.size}",
#             f"Diameter: {cable.diameter}",
#             f"Cable Weight: {cable.pounds_per_foot}",
#             f"Cross-Sectional Area: {cable.cross_sectional_area}",
#         ]
#         for line in text_lines:
#             draw.text((text_x, text_y), line, fill=text_color, font=font)
#             text_y += font_size + 10  # Adjust the vertical spacing
#
#     # Save the image to a file or display it
#     image.save("cable_image.png", dpi=(300, 300))  # Higher resolution (300 DPI)
#     image.show()
#
# get_cable_sizes()
# generate_cable_image(cable_sizes[7:11])  # Extract cables from indices 2 to 4 (inclusive)

from cable_classes import *
from user_interface import *
from file_handler import *
from PIL import Image, ImageDraw, ImageFont


def generate_cable_image(cables):
    # Define the image size and other parameters
    image_size = (1000, 900)  # Higher resolution image size
    text_margin = 10  # Decreased margin
    font_size = 12  # Larger font size
    offset_x = 40  # Offset in the x-direction
    offset_y = 40  # Offset in the y-direction

    # Calculate the quadrant size based on the image size
    quadrant_size = (image_size[0] // 2, image_size[1] // 2)

    # Create a new image with a white background
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    for i, cable in enumerate(cables):
        # Calculate the scaled radius based on the cable's diameter
        diameter = cable.diameter
        scaling_factor = 150  # Increase the scaling factor
        cable_radius = diameter * scaling_factor / 2  # Adjust the scaling factor here

        # Calculate the coordinates for the center of the quadrant based on the index
        center_x = (i % 2) * quadrant_size[0] + quadrant_size[0] // 2
        center_y = (i // 2) * quadrant_size[1] + quadrant_size[1] // 2
        center = (center_x, center_y)

        # Draw the cable as a filled circle with a border
        cable_color = "black"
        cable_outline_color = "black"
        cable_outline_width = 5  # Thicker outline
        cable_bbox = (
            center[0] - cable_radius,
            center[1] - cable_radius,
            center[0] + cable_radius,
            center[1] + cable_radius,
        )
        draw.ellipse(cable_bbox, outline=cable_outline_color, width=cable_outline_width)

        # Create a text label with the cable information
        text_x = center_x - cable_radius + offset_x  # Add x-direction offset
        text_y = center_y - cable_radius - text_margin + offset_y  # Add y-direction offset
        text_color = "black"
        font = ImageFont.truetype("arial.ttf", font_size)  # Set the font size
        text_lines = [
            f"S: {cable.size}",
            f"D: {cable.diameter}",
            f"CW: {cable.pounds_per_foot}",
            f"A: {cable.cross_sectional_area}",
        ]
        for line in text_lines:
            draw.text((text_x, text_y), line, fill=text_color, font=font)
            text_y += font_size + 10  # Adjust the vertical spacing

    # Save the image to a file or display it
    image.save("cable_image.png", dpi=(300, 300))  # Higher resolution (300 DPI)
    image.show()

get_cable_sizes()
generate_cable_image(cable_sizes[7:11])  # Extract cables from indices 7 to 10 (inclusive)
