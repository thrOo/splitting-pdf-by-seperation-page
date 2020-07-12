import numpy as np
import os
import io
import pytesseract
from wand.image import Image as wi
import cv2
import re
from PyPDF2 import PdfFileReader, PdfFileWriter

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def splitPdfBySeparationPage(pdf_path, verbose, dir):
    filename = pdf_path[pdf_path.rfind('/')+1:-4]
    if verbose:
        print(filename,'starting')

    pdf=wi(filename = pdf_path,resolution=300)
    pdfImg = pdf.convert('jpeg')

    imgBlobs=[]
    separation_pages=[]

    for img in pdfImg.sequence:
        page = wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))

    if verbose:
        print(filename,"Pages found: ", len(imgBlobs))

    for i, imgBlob in enumerate(imgBlobs):
        image_stream = io.BytesIO(imgBlob)
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        im = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.medianBlur(im,5)
        im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        im = deskew(im)

        text = pytesseract.image_to_string(im, lang = 'eng')
        text = text.split('\n', 1)[0]
        if re.search(r"[TI]{3,12}", text):
            separation_pages.append(i)

    imgBlobs = []
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
        reader = PdfFileReader(infile)

        for seperation_page in separation_pages:
            start = current_page
            end = seperation_page - 1
            if start <= end:
                writer = PdfFileWriter()

                while start <= end:
                    writer.addPage(reader.getPage(start))
                    start += 1

                current_doc += 1
                with open( dir + '/output/' + filename + '_doc' + str(current_doc) + '.pdf', 'wb') as outfile:
                    writer.write(outfile)

            current_page = seperation_page + 1

        if current_page <= (len(imgBlobs) - 1):
            start = current_page
            end = len(imgBlobs) - 1
            writer = PdfFileWriter()

            while start <= end:
                writer.addPage(reader.getPage(start))
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
            writer = PdfFileWriter()
            writer.addPage(reader.getPage(page))

            with open( dir + '/output/' + filename + '_doc' + str(page+1) + '.pdf', 'wb') as outfile:
                writer.write(outfile)

    os.rename(pdf_path, pdf_path[:-4] + '_done.pdf')

    if verbose:
        print(filename,'ending')
