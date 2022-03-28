import argparse
import os
import re
import time
import subprocess

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Renaming script')
    parser.add_argument('-d', nargs='?', help='a directory-path to directory')

    args = parser.parse_args()
    if args.d is None:
        raise FileNotFoundError

    start_time = time.time()
    file_list = os.listdir(args.d)

    file_count = 0
    for file in file_list:
        if file.endswith(".pdf"):
            if not re.search(r"_done", file):
                file_count += 1
                file_path =  args.d + '/' + file
                print(file_path)
                p = subprocess.Popen(['evince', file_path])
                new_name = input ("Rename to:")
                if len(new_name) > 0:
                    os.rename(file_path, args.d + '/' + new_name+ '.pdf')
                p.terminate()



    print('proccessed',file_count,'files')
    print('DONE',time.strftime('%H:%M:%S',time.gmtime(time.time()-start_time)))
