import os
from PIL import Image, ImageOps, ImageChops
from fpdf import FPDF
from tkinter import messagebox
def convert_images_to_pdf(images, output_path):
    # Create a new PDF object
    pdf = FPDF()

    # Loop through all the images and add them to the PDF
    for image_file in images:
        # Open the image file using Pillow
        image = Image.open(image_file)

        # Add a new page to the PDF
        pdf.add_page()

        # Resize the image to fit the page width
        pdf.image(image_file, x=0, y=0, w=pdf.w-1)

    # Save the PDF file to the specified path
    pdf.output(output_path, 'F')
    print(f'PDF file saved as {output_path}')

def images_to_pdf(images, output_path):
    pdf = FPDF()
    for image in images:
        cover = Image.open(image)
        pdf.add_page()
        pdf.image(image, 0, 0, w=pdf.w-1)
    pdf.output(output_path, "F")
    print(f'PDF file saved as {output_path}')

def crop(file_path):

    # Cropping white places in pdf
    print("Cropping....")

    import subprocess
    filename, ext = os.path.splitext(file_path)  # split filename and extension
    cropped_path = filename + "-cropped" + ext  # append "-cropped" to filename

        
    # Define the command to crop the PDF file using pdfcropper
    pdf_crop_path = os.path.join(os.getcwd(),"./pdfcrop.exe")
    cmd = f'{pdf_crop_path} {file_path} {cropped_path}'
    try:
        subprocess.run(cmd, shell=True, check=True)
    except:
        try:
            pdf_crop_path = "pdfcrop.exe"
            cmd = f'{pdf_crop_path} {file_path} {cropped_path}'
            subprocess.run(cmd, shell=True, check=True)
        except:
            current_path = os.getcwd()
            messagebox.showerror("ERROR", f"can't find pdfcrop.exe, confirm the 'pdfcrop.exe' is in your path or file exist in {current_path}\pdfcrop.exe")

def compress(file_path):
    # Compress the cropped pdf
    from PyPDF2 import PdfReader, PdfWriter

    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.add_metadata(reader.metadata)
    filename, ext = os.path.splitext(file_path)  # split filename and extension
    final_path = filename + "-final" + ext  # append "-cropped" to filename
    output_file = open(final_path, 'wb')
    writer.write(output_file)
    print(f'OK {final_path}')
    output_file.close()

def delete_files(cropped_path, output_path,final_path):
    # Delete the cropped file
    if os.path.exists(cropped_path):
        os.remove(cropped_path)

    # Delete the final file
    if os.path.exists(output_path):
        os.remove(output_path)        
        # specify the full path of the file you want to rename
    old_path = final_path
    new_name, ext = os.path.splitext(final_path)  # split filename and extension
    new_name = new_name.replace("-cropped-final","")
    print("ALLAH" + new_name)
    # get the directory path of the file
    dir_path = os.path.dirname(old_path)
    # create the new path for the file
    new_path = os.path.join(dir_path, new_name)
    # rename the file
    os.rename(old_path, new_path+ext)

def hebele(images_list,output_file):
    filename, ext = os.path.splitext(output_file)  # split filename and extension
    cropped_path = filename + "-cropped" + ext  # append "-cropped" to filename
    final_path = filename + "-cropped-final" + ext  # append "-cropped" to filename

    convert_images_to_pdf(images_list,output_file)
    crop(output_file)
    compress(cropped_path)
    delete_files(cropped_path,output_file,final_path)
    