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
import glob
import subprocess


def merge_pdfs():
    pdf_files = glob.glob("Conduit *.pdf")  # Find all PDF files matching the pattern

    output_pdf_path = "Conduit Optimization Results.pdf"

    # Create a PDF writer object
    pdf_writer = PdfWriter()

    for pdf_file in pdf_files:
        with open(pdf_file, "rb") as pdf:
            # Create a PDF reader object
            pdf_reader = PdfReader(pdf)

            # Add all the pages from the current PDF to the writer
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

    # Save the merged PDF
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    # Open the merged PDF using the default PDF viewer
    subprocess.Popen(["start", "", output_pdf_path], shell=True)


# Call the function
# merge_pdfs()

# user_interface()
get_cable_sizes()             # Excel of all cables and their parameters
get_cable_pull_sheet()        # Pull sheet excel
sort_stationing()             # List each stationing value in the pull sheet, ordered
optimize_for_conduit()        # Run conduit algorithm, generate conduit images
generate_output_file()        # Create output excel file with generated conduits
merge_pdfs()
