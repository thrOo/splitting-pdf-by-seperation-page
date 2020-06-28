import argparse
import os
import re
import multiprocessing

from functions import splitPdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--dir', nargs='?', help='a directory-path to directory')

    args = parser.parse_args()
    if args.dir is None:
        raise FileNotFoundError

    jobs = []
    for file in os.listdir(args.dir):
        if file.endswith(".pdf"):
            if not re.search(r"_done", file):
                p = multiprocessing.Process(target=splitPdf, args=(file,))
                jobs.append(p)
                p.start()

    for j in jobs:
        j.join()

    print('DONE')
