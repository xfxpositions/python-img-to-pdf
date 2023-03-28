import os
from PIL import Image, ImageOps, ImageChops
from fpdf import FPDF

input_folder_name = input("girdiler icin klasor ismi giriniz:\n")
output_folder_name = input("ciktilar icin klasor ismi giriniz:\n")
input_folder_path = os.path.join(f'./{input_folder_name}',)
output_folder_path = os.path.join(f'./{output_folder_name}',)


if not os.path.exists(input_folder_path):
    os.makedirs(input_folder_name)

if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_name)

for filename in os.listdir(output_folder_path):
    # Print the filename
    print(filename)


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


        # def trim(im):
        #     bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        #     diff = ImageChops.difference(im, bg)
        #     diff = ImageChops.add(diff, diff, 2.0, -100)
        #     bbox = diff.getbbox()
        #     if bbox:
        #         return im.crop(bbox)
        # # Crop the image to remove any whitespace
        # trim(image)
        
        # cropped_image_path = os.path.join(input_folder_path, 'cropped', image_file)
        # image.save(cropped_image_path)

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
    if file.startswith("cikti") and os.path.isfile(file):
        i += 1

pdf_file_name = f'cikti{i}.pdf'
pdf_file_path = os.path.join(output_folder_path, pdf_file_name)

# Convert all images in the input folder to a PDF file
convert_images_to_pdf(input_folder_path, pdf_file_path)

print(f'PDF file saved as {pdf_file_path}')
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
cropped_name = os.path.splitext(pdf_file_path)[0] + '_cropped.pdf'
a = os.path.join(output_folder_path, cropped_name)
final_name = os.path.splitext(pdf_file_path)[0] + '_final.pdf'
final_path = os.path.join(output_folder_path, final_name)
pdf_file_path = os.path.join(output_folder_path, cropped_name)

print(os.path.join(output_folder_path, f'{pdf_file_name}'))
print(os.path.join(output_folder_path, cropped_name))

with open(os.path.join(output_folder_path, f"{pdf_file_name}_final.pdf"), "wb") as fp:
    writer.write(fp)
    os.remove(os.path.join(output_folder_path, f'{pdf_file_name}'))
    os.remove(cropped_name)
print(f"DONE {final_name}")
