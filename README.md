# Extract Function Name and Begin/End Line Number in C/C++ Source Codes

This is a simple project to extract the function names in C/C++ source codes. It should work well for C codes, but may have problems for C++ codes. It is written in Python. Please let me know if you find any bugs.

1. func_name_extract.py
Usage:
    
    command line: python func_name_extract.py <file_path> <output_file>

    <file_path> is the source code file (e.g. helloWorld.c) you want to extract.

    <output_file> is the file to store the result

Example:
    
    python func_name_extract.py sample_codes/pow_related_errors.c result.txt 

2. func_name_extract_line.py
Extend to support begin/end line number of a function.

3. func_name_extract_line.py
Extend to support a folder iteration

**Future Works:
The size of a function includes the comments "/* */" made by this way. Will try to eliminate this case in near future.

