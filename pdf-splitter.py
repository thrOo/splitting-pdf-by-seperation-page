import argparse
import os
import re
from functions import splitPdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--dir', nargs='?', help='a directory-path to directory')

    args = parser.parse_args()
    if args.dir is None:
        raise FileNotFoundError

    for file in os.listdir(args.dir):
        if file.endswith(".pdf"):
            if not re.search(r"_done", text):
                splitPdf(file)

    print('DONE')
