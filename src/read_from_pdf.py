import os
import re
import argparse
import subprocess
import numpy as np

from chunker import try_to_write_dir

def filter_junk_text(txt_file: str, output_dir: str):
    # helping file to get content of txt file
    filtered_document_text = ''
    document_content = open(txt_file, 'r')

    # check in every line of the text if there is junk text there
    for line in document_content:
        line = remove_line_if_junk(line)
        filtered_document_text += line

    # write filtered text into new directory
    file_name_index = txt_file.rfind('/')
    txt_file = txt_file[file_name_index+1:]

    f = open(output_dir + txt_file, 'w')
    f.write(filtered_document_text)
    f.close()

def remove_line_if_junk(line: str) -> str:
    junk_list_document = ['\s[nN]ichtamtliche Lesefassung.*']

    # check if the line includes any element of the list
    for i in junk_list_document:
        x = re.search(i, line)

        if x:
            # remove the found text
            # print(x[0]) # Debug
            line = re.sub(x[0], '', line)
        
    return line

def main():
    """Main to translate given PDF files after argument '-c' in a specific folder 
    into txt files that retain the layout, e.g. table
    """

    # default list of the files if arguments '-c' or '-o' not given
    files_to_convert = []
    files_to_filter = []

    parser = argparse.ArgumentParser(description = 'Translates all PDF files' +
                        ' from a given folder into text files while' +
                        ' retaining the layout including table structures.' +
                        ' The new text files will be located in the same' +
                        '  directory as the PDF files.')

    parser.add_argument('-d', '--dir_path', type = try_to_write_dir, 
                       default = './',
                       help = 'Directory in which all output text files are written.')

    # if argument c given it will be converted
    parser.add_argument('-c', '--files_to_convert', action = 'append', nargs = '+',
                        help = 'The list of files which should be be converted (pdf -> txt).')  

    
    parser.add_argument('-o', '--output_directory',
                        default = '../data/filtered_documents/', 
                        help = 'Directory where the filtered files should be saved.')

    
    # add list of files should be filtered as argument
    parser.add_argument('-f', '--files_to_filter', action = 'append', nargs = '+', 
                    help = 'The list of files which should be filtered.')
    
    args = parser.parse_args()

    dir_path = os.path.join(args.dir_path, '')  # append '/' if not there
    output_dir = os.path.join(args.output_directory, '')

    # convert pdf files in a dictionary into txt files
    if args.files_to_convert:
        # flat the nested list
        files_to_convert = list(np.concatenate(args.files_to_convert))

        for filename in files_to_convert: 
            f = os.path.join(dir_path, filename)
            try: 
                process = subprocess.Popen(["pdftotext", "-layout", f])
            except:
               print("Error: The necessary packages to convert pdf into txt are not installed properly!")

    # filter out the (converted txt) files
    if args.files_to_filter:
        # flat the nested list
        files_to_filter = list(np.concatenate(args.files_to_filter))

        for filename in files_to_filter:
            f = os.path.join(dir_path, filename)

            # it has to be txt file, otherwise there occurs an error
            if os.path.isfile(f):
               filter_junk_text(f, output_dir)

    exit(0)

if __name__ == "__main__":
    main()
   
