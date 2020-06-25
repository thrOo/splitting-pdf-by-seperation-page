import argparse
import numpy as np
import os
import io
import pytesseract
from wand.image import Image as wi
import cv2


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

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--file', nargs='?', help='a directory-path to file')

    args = parser.parse_args()

    if args.file is None:
        raise FileNotFoundError

    pdf_path = args.file
    pdf=wi(filename = pdf_path,resolution=300)
    pdfImg = pdf.convert('jpeg')

    imgBlobs=[]
    extracted_text=[]

    for img in pdfImg.sequence:
        page = wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))

    print("Pages found: ", len(imgBlobs))

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
        extracted_text.append(text)
        print('start page', i)

    print(text)
