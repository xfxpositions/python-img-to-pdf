import os
from PIL import Image, ImageOps, ImageChops
from fpdf import FPDF
import argparse

# create an argument parser
parser = argparse.ArgumentParser(description='Convert images to PDF')

# add an optional argument for output file name
parser.add_argument('-n', '--name', default='çıktı', help='output PDF file name')
parser.add_argument('-mode', '--name', default='çıktı', help='output PDF file name')
parser.add_argument('output', default=os.getcwd(), help="output path of pdf file")
# parse the command line arguments
args = parser.parse_args()

# access the output file name
output_file_name = args.name


input_folder_name = input("girdiler icin klasor ismi giriniz:\n")
output_folder_name = input("ciktilar icin klasor ismi giriniz:\n")
input_folder_path = os.path.join(f'./{input_folder_name}',)
output_folder_path = args.output


if not os.path.exists(input_folder_path):
    os.makedirs(input_folder_name)

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_name)

# Define a function to convert images to PDF
def convert_images_to_pdf(image_folder_path, pdf_file_path):
    # Get all image files in the specified folder
    image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.jpg') or f.endswith('.png')]

    # Create a new PDF object
    pdf = FPDF()

    # Loop through all the images and add them to the PDF
    for image_file in image_files:
        # Open the image file using Pillow
        image = Image.open(os.path.join(image_folder_path, image_file))

        # Add a new page to the PDF
        pdf.add_page()

        # Resize the image to fit the page width
        pdf.image(os.path.join(image_folder_path, image_file), x=0, y=0, w=pdf.w-1)

    # Save the PDF file to the specified path
    pdf.output(pdf_file_path, 'F')

# Find the next available output PDF file name
i = 1
dirs = os.listdir(output_folder_path)
for file in dirs:
    if file.startswith(output_file_name):
        i += 1

pdf_file_name = f'{output_file_name}{i}.pdf'
pdf_file_path = os.path.join(output_folder_path, pdf_file_name)

# Convert all images in the input folder to a PDF file
convert_images_to_pdf(input_folder_path, pdf_file_path)

print(f'PDF file saved as {pdf_file_path}')

# Cropping white places in pdf
print("Cropping....")

import subprocess

# Define the command to crop the PDF file using pdfcropper
cropped_path = os.path.join(output_folder_path, f'cikti{i}_cropped.pdf')
cmd = f'pdfcrop.exe {pdf_file_path} {cropped_path}'

# Run the command using subprocess
subprocess.run(cmd, shell=True, check=True)

# Compress the cropped pdf
from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader(cropped_path)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.add_metadata(reader.metadata)

# Writing final
with open(os.path.join(output_folder_path, f"{pdf_file_name}_final.pdf"), "wb") as fp:
    writer.write(fp)

# Deleting cropped and first files
cropped_name = os.path.splitext(pdf_file_path)[0] + '_cropped.pdf'
final_name = os.path.splitext(pdf_file_path)[0] + '_final.pdf'
try:
    os.remove(os.path.join(output_folder_path, f'{pdf_file_name}'))
    os.remove(cropped_name)
except OSError as e:
    print(f'error deleting file: {e.filename} - {e.strerror}')
finally:
    print(f"DONE {final_name}")
    

