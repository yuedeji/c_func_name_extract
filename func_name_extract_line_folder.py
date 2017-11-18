import os
import os.path
import pickle
import re
import sys
import csv
import re
type_list = ['int', 'char', 'float', 'double', 'bool', 'void', 'short', 'long', 'signed', 'struct']

valid_ext = [".c", ".cpp"]

re_removed = "(\'.*\')|(\".*\")|(/\*.*\*/)|(//.*)"

keyword_set = set(type_list + ['sizeof'])

def pickle_dump(root_path, data, file_name):
    os.chdir(root_path)
    fp = open(file_name, "w")
    pickle.dump(data, fp)
    fp.close()

def pickle_load(root_path, file_name):
    os.chdir(root_path)
    fp_case = open(file_name, "r")
    dict_case = pickle.load(fp_case)
    fp_case.close()
    return dict_case


def is_valid_name(name):
    if re.match("[a-zA-Z_][a-zA-Z0-9_]*", name) == None:
        return False
    if name in keyword_set:
        return False
    return True

def is_func(line):
#int, __int64, void, char*, char *, struct Node, long long int, (void *)
#int func(int a, int *b, (char *) c)
    line = line.strip()
    if len(line) < 2:
        return None
# Rule 1: assume the function name line must ends with ) or {;
#    if line[-1] != ')' and line[-1] != '{':
#        return None
# Rule 2: (*) must in
    if '(' not in line: #or ')' not in line:
        return None
# Rule 3: # stands for #include or other primitives; / start a comment
    if line[0] == '#' or line[0] == '/':
        return None
# Rule 4: ends with ;
    if line.endswith(';'):
        return None
    if line.startswith('static'):
        line = line[len('static'):]
# replace pointer * and & as space
    line = re.sub('\*', ' ', line)
    line = re.sub('\&', ' ', line)


# replace '(' as ' ('
    #re.sub('(', ' ( ', line)
    line = re.sub('\(', ' \( ', line)
    line_split = line.split()

    if len(line_split) < 2:
        return None

    bracket_num = 0
    for ch in line:
        if ch == '(':
            bracket_num += 1

    has_type = False
    for type_a in type_list:
        if type_a in line_split[0]:
            has_type = True
#    if has_type == False:
#        return None
#    print line
    if bracket_num == 1:
        for index in xrange(len(line_split)):
            if '(' in line_split[index]:
                return line_split[index - 1]
    else:
        line = re.sub('\(', ' ', line)
        line = re.sub('\)', ' ', line)
        line_split = line.split()
        index = 0
        for one in line_split:
            if is_valid_name(one):
                index += 1
                if index == 2:
                    return one
        return None

def get_line_type(line):
    line = line.strip()
    if line.startswith("/*"):
#        print line
        return "comment_paragraph"
    elif line.startswith("//"):
        return "comment_line"
    elif line.startswith("#"):
        return "macro"
    return "other"

#def is_comment_begin(line):
#    if line.startswith("/*"):
#        return True
#    return False

def is_comment_end(line):
    #print line
    line = line.strip()
    if line.endswith('*/'):
        return True
    return False

def is_func_end(line, left_brack_num):
    line = line.strip()
    left_brack_num += line.count("{")
    if "}" in line:
        left_brack_num -= line.count("}")
        if left_brack_num == 0:
            return True
    return False

def func_name_extract(file_path):

    if not os.path.isfile(file_path):
        return


    file_list = []
    with open(file_path, "r") as fp:
        for line in fp.readlines():
            file_list.append(line)

    func_list = []

    i = -1
    while i < len(file_list) - 1:
        i += 1
        line = file_list[i]
        line_type = get_line_type(line)
        if line_type == "comment_line" or line_type == "macro":
            continue
        elif line_type == "comment_paragraph":
            while not is_comment_end(file_list[i]):
                i += 1
        else:
            line = re.sub(re_removed, "", line)
            if len(line) == 0:
                continue
            func_name = is_func(line)
            if func_name != None:
#                print i, func_name
                start_line = i
                left_brack_num = 0
                effective_line = 1
                while True and i < len(file_list):
#                    print i
#                    print line
                    line = (file_list[i]).strip()
                    line_type = get_line_type(line)
                    if line_type == "comment_line":
                        continue

#                    elif line_type == "comment_paragraph":
#                        continue
#                        while not is_comment_end(file_list[i]):
#                            i += 1
                    left_brack_num += line.count('{')
                    effective_line += 1
                    if "}" in line:
                        left_brack_num -= line.count("}")
                        if left_brack_num < 1:
                            break
#                    print left_brack_num
                    i += 1
                end_line = i
               # if func_name != None:
                func_list.append([file_path, func_name, start_line + 1, end_line + 1, end_line - start_line + 1])
#                print func_name
    return func_list

def func_name_extract_folder(work_folder):

    func_list_all = []
    for dirpath, dirnames, filenames in os.walk(work_folder):
        for name in filenames:
            for ext in valid_ext:
                if name.endswith(ext):
                    file_path = os.path.join(dirpath, name)
#                    if name == "func_tbl.c":
#                        continue
                    print file_path
                    func_list_all = func_list_all + func_name_extract(file_path)

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

