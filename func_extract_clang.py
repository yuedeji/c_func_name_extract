import os
import sys
import csv
import re

re_ansi = re.compile(r'\x1b[^m]*m')

def write_to_csv(file_list, output_file):

    with open(output_file, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ",")
        for one in file_list:
            csvwriter.writerow(one)
    print "The output file is written to", output_file


def get_ast(input_file, temp_file):

    cmd = "clang -Xclang -ast-dump -I /home/yuedeji/firmware/code_clone/bellon_c/postgresql/src/include/ " + input_file + " > " + temp_file
    os.system(cmd)

    ast_list = []
    with open(temp_file, "r") as fp:
        for line in fp:
            if "FunctionDecl" in line:
                line = line.strip()
                ast_list.append(re_ansi.sub('', line))

    result_list = []
    for func_str in ast_list:
        if func_str.endswith("extern"):
            continue
#        print func_str
#        m = re.findall(r"(\<.*>\s[a-zA-Z0-9_]*)", func_str)
        m = re.findall(r"(\<.*\,\sline.*\>\s[a-zA-Z0-9_]*)", func_str)
        if m:
            func_info = (re.sub('\'|\"', '', m[0])).split(' ')
#            print func_str
#            print func_info
            func_name = func_info[-1]
            start_line = int((func_info[0]).split(':')[1])
            end_line = int((func_info[1]).split(':')[1])
#            temp_line = [input_file, func_name, start_line, end_line, end_line - start_line + 1]
            result_list.append([input_file, func_name, start_line, end_line, end_line - start_line + 1])

    return result_list

#~/firmware/code_clone/bellon_c/postgresql/src/backend/nodes/equalfuncs.c > clang.log

def source_to_ast(input_file, output_file):

    func_list = get_ast(input_file, output_file)
    write_to_csv(func_list, output_file)

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print "python func_extract_clang.py <input_file> <output_file>"
        exit(-1)
    source_to_ast(sys.argv[1], sys.argv[2])
