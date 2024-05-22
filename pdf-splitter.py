import argparse
import os
import re
import multiprocessing
import time
from functions import splitPdfByBarCodeSeparationPage, splitPdfEachPage

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Splitting script')
    parser.add_argument('-d', nargs='?', help='a directory-path to directory')
    parser.add_argument('-t', nargs='?', help='number of proccesses/threads')
    parser.add_argument('-v', action='store_true', help='enable some more output')
    parser.add_argument('-single', action='store_true', help='splits after each page')

    args = parser.parse_args()
    if args.d is None:
        raise FileNotFoundError

    if args.single and args.ocr:
        raise NotImplementedError

    print(args.d)
    output_path = args.d + '/output'
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    start_time = time.time()
    file_list = os.listdir(args.d)

    threads = 2
    if args.t is not None:
        threads = int(args.t)

    pool = multiprocessing.Pool(threads)
    file_count = 0
    for file in file_list:
        if file.lower().endswith(".pdf"):
            if not re.search(r"_done", file):
                file_count += 1
                file_path =  args.d + '/' + file
                if args.single :
                    result = pool.apply_async(splitPdfEachPage, args=(file_path, args.v, args.d,))
                    result.get()
                else :
                    result = pool.apply_async(splitPdfByBarCodeSeparationPage, args=(file_path, args.v, args.d,))
                    result.get()

    pool.close()
    pool.join()

    print('proccessed',file_count,'files')
    print('DONE',time.strftime('%H:%M:%S',time.gmtime(time.time()-start_time)))
