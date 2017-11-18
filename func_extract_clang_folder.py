import os
import os.path
import re
import sys
import csv

from func_extract_clang import *

valid_ext = ['.c', '.cpp']
def func_name_extract_folder(work_folder):

    func_list_all = []
    temp_file = os.path.join(work_folder, "temp_clang.log")
    for dirpath, dirnames, filenames in os.walk(work_folder):
        for name in filenames:
            for ext in valid_ext:
                if name.endswith(ext):
                    file_path = os.path.join(dirpath, name)
#                    if name == "func_tbl.c":
#                        continue
                    print file_path
                    func_list_all = func_list_all + get_ast(file_path, temp_file)

    return func_list_all

def write_to_file(func_list, output_file):

    header = ["file_path", "func_name", "start_line", "end_line", "size"]
    with open(output_file, "w") as out_file:
        csv_write = csv.writer(out_file, delimiter = ",")

        csv_write.writerow(header)

        for one in func_list:
            csv_write.writerow(one)

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print '''Usage: python func_name_extract.py <file_path> <output_file>\n'''
        exit(-1)
    func_list = func_name_extract_folder(sys.argv[1])
    write_to_file(func_list, sys.argv[2])

