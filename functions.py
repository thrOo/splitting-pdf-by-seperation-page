import os
import re
from PyPDF2 import PdfReader, PdfWriter

from pyzbar.pyzbar import decode
from pdf2image import convert_from_path
from PIL import Image


def splitPdfByBarCodeSeparationPage(pdf_path, verbose, dir):
    filename = pdf_path[pdf_path.rfind('/')+1:-4]
    if verbose:
        print(filename,'starting')

    separation_pages=[]
    images = convert_from_path(pdf_path)
    for i, img in enumerate(images):
        detected_barcodes = decode(img)
        
        for barcode in detected_barcodes:
            if barcode.data != "":
                if re.search(r"separator_page", str(barcode.data)):
                    separation_pages.append(i)
    
    if verbose:
        print(filename,"separation_pages:", separation_pages)

    current_doc = 0
    current_page = 0

    #for each seperation page
    #interval current_page to seperationpage - 1
    #if end of interval is equal or greater than start
    #   the create a pdf with those pages
    #set current_page to seperation+1
    #after last seperationpage should be the last document
    #if current_page equal or greater than

    with open(pdf_path, 'rb') as infile:
        reader = PdfReader(infile)

        for seperation_page in separation_pages:
            start = current_page
            end = seperation_page - 1
            if start <= end:
                writer = PdfWriter()

                while start <= end:
                    writer.add_page(reader.pages[start])
                    start += 1

                current_doc += 1
                with open( dir + '/output/' + filename + '_doc' + str(current_doc) + '.pdf', 'wb') as outfile:
                    writer.write(outfile)

            current_page = seperation_page + 1

        if current_page <= (len(images) - 1):
            start = current_page
            end = len(images) - 1
            writer = PdfWriter()

            while start <= end:
                writer.add_page(reader.pages[start])
                start += 1

            current_doc += 1
            with open( dir + '/output/' + filename + '_doc' + str(current_doc) + '.pdf', 'wb') as outfile:
                writer.write(outfile)

    os.rename(pdf_path, pdf_path[:-4] + '_done.pdf')
    if verbose:
        print(filename,'ending')

def splitPdfEachPage(pdf_path, verbose, dir):
    filename = pdf_path[pdf_path.rfind('/')+1:-4]
    if verbose:
        print(filename,'starting')

    with open(pdf_path, 'rb') as infile:
        reader = PdfFileReader(infile)
        for page in range(reader.getNumPages()):
            writer = PdfWriter()
            writer.add_page(reader.pages[page])

            with open( dir + '/output/' + filename + '_doc' + str(page+1) + '.pdf', 'wb') as outfile:
                writer.write(outfile)

    os.rename(pdf_path, pdf_path[:-4] + '_done.pdf')

    if verbose:
        print(filename,'ending')