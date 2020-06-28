import argparse
import os
import re
import multiprocessing
import time

from functions import splitPdf

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing script')
    parser.add_argument('--dir', nargs='?', help='a directory-path to directory')

    args = parser.parse_args()
    if args.dir is None:
        raise FileNotFoundError

    start_time = time.time()
    pool = multiprocessing.Pool(2)

    for file in os.listdir(args.dir):
        if file.endswith(".pdf"):
            if not re.search(r"_done", file):
                pool.apply_async(splitPdf, args=(file,))

    pool.close()
    pool.join()

    print('DONE')
    print(time.strftime('%H:%M:%S',time.gmtime(time.time()-start_time)))
