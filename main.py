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
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import math
from PyPDF2 import PdfReader, PdfWriter, PdfFileReader


def merge_pdfs():
    existing_pdf_path = "Conduit 1.pdf"
    output_pdf_path = "modified_file.pdf"

    with open(existing_pdf_path, "rb") as existing_pdf:
        # Create a PDF reader object
        pdf_reader = PdfReader(existing_pdf)

        # Create a PDF writer object
        pdf_writer = PdfWriter()

        # Add all the existing pages to the writer
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Open the PDF file to be inserted
        insert_pdf_path = "Conduit 2.pdf"
        with open(insert_pdf_path, "rb") as insert_pdf:
            # Create a PDF reader for the insert PDF
            insert_pdf_reader = PdfReader(insert_pdf)

            # Get the first page from the insert PDF
            insert_page = insert_pdf_reader.pages[0]

            # Add the page from the insert PDF to the writer
            pdf_writer.add_page(insert_page)

        # Save the modified PDF
        with open(output_pdf_path, "wb") as output_pdf:
            pdf_writer.write(output_pdf)

# Call the function
merge_pdfs()

# user_interface()
# get_cable_sizes()             # Excel of all cables and their parameters
# get_cable_pull_sheet()        # Pull sheet excel
# sort_stationing()             # List each stationing value in the pull sheet, ordered
# optimize_for_conduit()        # Run conduit algorithm, generate conduit images
# generate_output_file()        # Create output excel file with generated conduits

