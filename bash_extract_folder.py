#! /usr/bin/
import os
import sys
import csv

working_folder = "./"
output_folder = "./"
valid_ext = [".c"]

def dump_to_csv():

for dirpath, dirnames, filenames in os.walk(working_folder):
    for name in filenames:
        for ext in valid_ext:
            if name.endswith(ext):
                file_path = os.path.join(dirpath, name)
                cmd = "python func_name_extract_line.py " + file_path
