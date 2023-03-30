import os
from PIL import Image, ImageOps, ImageChops
from fpdf import FPDF
def convert_images_to_pdf(images, output_path):
    # Create a new PDF object
    pdf = FPDF()

    # Loop through all the images and add them to the PDF
    for image_file in images:
        # Open the image file using Pillow
        image = Image.open(os.path.join(images, image_file))

        # Add a new page to the PDF
        pdf.add_page()

        # Resize the image to fit the page width
        pdf.image(os.path.join(images, image_file), x=0, y=0, w=pdf.w-1)

    # Save the PDF file to the specified path
    pdf.output(output_path, 'F')
    print(f'PDF file saved as {output_path}')

def crop(file_path):

    # Cropping white places in pdf
    print("Cropping....")

    import subprocess
    filename, ext = os.path.splitext(file_path)  # split filename and extension
    cropped_path = filename + "-cropped" + ext  # append "-cropped" to filename

    # Define the command to crop the PDF file using pdfcropper
    cmd = f'pdfcrop.exe {file_path} {cropped_path}'

    subprocess.run(cmd, shell=True, check=True)

def compress(file_path):
    # Compress the cropped pdf
    from PyPDF2 import PdfReader, PdfWriter

    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)

def write(output_path):
    # Writing final
    with open(output_path), "wb" as fp:
        os.write(fp)
    print(f'OK {output_path}')

def start(images_list,output_file):
    convert_images_to_pdf(images_list,output_file)
    crop(output_file)
    compress(output_file)
    write(output_file)
    