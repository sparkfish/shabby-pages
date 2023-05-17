import os
import argparse

import sys
import subprocess
import pkg_resources

def convert_pdf(file_path, dpi=300, output_path="", output_format="PNG", page=-1):
    """ Main function to convert pdf file into images
    
    param file_path: Path of the input pdf file.
    type file_path: string
    param dpi: DPI value of the converted images.
    type dpi: int, optional
    param output_path: Path of the output images
    type output_path: string
    param output_format: Output image format.
    type output_format: string, optional
    param page: For single page conversion. Page nubmer starts with 0.
    type page: int, optional
    """
    
    # check if pymupdf is installed, if not install it on the spot
    check_package()
    
    # import within the function because pymupdf might not be installed
    import fitz

    # check validity of file path
    if file_path is None or not os.path.isfile(file_path):
        print("Invalid file path!")
        return
    pdf_document = fitz.open(file_path)
 
    # set current directory as output path is no path is provided
    if output_path is None:
        output_path = os.path.abspath(os.getcwd())
    
    # generate page number based on pdf file
    if page == -1:
        pages = [n for n in range(pdf_document.page_count)]
    else:
        pages =[page]
    
    # get pdf file name
    filename_ext = os.path.basename(file_path)
    filename, file_extension = os.path.splitext(filename_ext)
    
    # check for valid pdf file
    if file_extension != ".pdf":
        print("Invalid pdf file!")
        return
    
    # convert pdf into images
    print("Converting pdf...")
    for page in pages:
        single_page = pdf_document.load_page(page)
        pixel_map = single_page.get_pixmap(dpi=dpi)
        image_filename = (filename+"_{:04d}."+output_format.lower()).format(single_page.number)
        merged_output_path = output_path+"/"+image_filename
        pixel_map.pil_save(merged_output_path, format=output_format, dpi=(dpi,dpi))
        print("Converted "+merged_output_path)
        
    print("Done!")
        
def check_package():
    """Function to check if the required pymupdf is installed or not."""

    required_library = {"pymupdf"}
    installed_libraries = {pkg.key for pkg in pkg_resources.working_set}
    missing_library = required_library - installed_libraries

    if missing_library:
        print("pymupdf is not installed. Installing ...")
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", *missing_library], stdout=subprocess.DEVNULL)
        print("Installation done!")
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", type=str, help="Path of the input pdf file")
    parser.add_argument("--dpi", type=int, default=300, help="DPI value of the image")
    parser.add_argument("--output_path", type=str, default=None, help="Path of the output images")
    parser.add_argument("--output_format", type=str, default="PNG", help="Types of output image")
    parser.add_argument("--page", type=int, default=-1, help="Set value here to enable single page conversion. Page number starts with 0")
    opt = parser.parse_args()

    convert_pdf(opt.file_path, opt.dpi, opt.output_path, opt.output_format, opt.page)