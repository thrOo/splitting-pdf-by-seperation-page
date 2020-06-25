import argparse
import PyPDF2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--file', nargs='?', help='a directory-path to dataset')

    args = parser.parse_args()

    if args.file is None:
        raise FileNotFoundError

    pdfFileObj = open(args.file , 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    print(pdfReader.numPages)

    pageObj = pdfReader.getPage(0)

    print(pageObj.extractText())

    pdfFileObj.close()
