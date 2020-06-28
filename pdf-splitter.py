import argparse
from functions import splitPdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--file', nargs='?', help='a directory-path to file')

    args = parser.parse_args()

    if args.file is None:
        raise FileNotFoundError

    splitPdf(args.file)

    print('DONE')
