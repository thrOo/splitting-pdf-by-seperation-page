import argparse
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--file', nargs='?', help='a directory-path to dataset')

    args = parser.parse_args()

    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[1]

    images = []
    final_text = []
    word_boxes = []
    line_boxes = []

    if args.file is None:
        raise FileNotFoundError

    image_pdf = Image(filename=args.file, resolution=300)
    print('pdf -> image')
    image_jpeg = image_pdf.convert('jpeg')

    for i, img in enumerate(image_jpeg.sequence):
        img.save('./temp/temp'+ i + '.jpeg')


    # for img in image_jpeg.sequence:
#
    #     img_page = PI.open(img)
    #     img_page = img_page.convert('L')
#
    #     req_image.append(img_page.make_blob('jpeg'))

    # print('image -> text')
    # for img in req_image:
    #     txt = tool.image_to_string(
    #         PI.open(io.BytesIO(img)),
    #         lang=lang,
    #         builder=pyocr.builders.TextBuilder()
    #     )
    #     final_text.append(txt)

    # print('image -> word_boxes')
    # for img in req_image:
    #     word_box = tool.image_to_string(
    #         PI.open(io.BytesIO(img)),
    #         lang=lang,
    #         builder=pyocr.builders.WordBoxBuilder()
    #     )
    #     word_boxes.append(word_box)
#
    # print('image -> line_boxes')
    # for img in req_image:
    #     line_box = tool.image_to_string(
    #         PI.open(io.BytesIO(img)),
    #         lang=lang,
    #         builder=pyocr.builders.LineBoxBuilder()
    #     )
    #     line_boxes.append(line_box)

    print('\n\nText:')
    for page in final_text:
        print(page)
        print('-----\n')

    # print('\n\n\nword Boxes:')
    # for wBoxes in word_boxes:
    #     for wbox in wBoxes:
    #         print(wbox)
    #     print('-----')
#
    # print('\n\n\nline Boxes:')
    # for lBoxes in line_boxes:
    #     for lbox in lBoxes:
    #         print(lbox)
    #     print('-----')
