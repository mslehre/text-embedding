import os
import re
import argparse
import subprocess

#Commeand from Lukasz
from chunker import try_to_write_dir

def filter_junk_text(txt_file):
    # helping file to get content of txt file
    filtered_document_text = ''
    document_content = open(txt_file, 'r')

    # check in every line of the text if there is junk text there
    for line in document_content:
        line = remove_line_if_junk(line)
        filtered_document_text += line

    # write filterd text into new directory
    file_name_index = txt_file.rfind('/')
    txt_file = txt_file[file_name_index+1:]
    f = open('../filteredDocuments/' + txt_file, 'w')
    f.write(filtered_document_text)
    f.close()

def remove_line_if_junk(line):
    junk_list_document = ['\s[nN]ichtamtliche Lesefassung.*']

    # check if the line includes any element of the list
    for i in junk_list_document:
        x = re.search(i, line)

        if x:
            # remove the found text
            # print(x[0]) # Debug
            line = re.sub(x[0], '', line)
        else:
            continue
        
    return line

def main():
    """Main to translate all PDF files in a specific folder into txt files that
    retain the layout, e.g. table
    """
    # Command from Lukasz
    parser = argparse.ArgumentParser(description = 'Translates all PDF files' +
                        ' from a given folder into text files while' +
                        ' retaining the layout including table structures.' +
                        ' The new text files will be located in the same' +
                        '  directory as the PDF files.')
    # Command from Lukasz
    parser.add_argument('-d', '--dir_path', type = try_to_write_dir, 
                       default = './',
                       help = 'Directory in which all PDF files are saved.')
    args = parser.parse_args()
    # Command from Lukasz
    dir_path = os.path.join(args.dir_path, '')  # append '/' if not there

    # convert pdf files in a dictionary into txt files
    # directory = '../data/examination_regulations_2'

    # dir_path = directory
    for filename in os.listdir(dir_path):
        f = os.path.join(dir_path, filename)
        # checking if it is a file and if it ends with '.pdf'
        if os.path.isfile(f) and f[-4:] == '.pdf':
            process = subprocess.Popen(["pdftotext", "-layout", f])
    

        # filter out the converted txt files
        # check if it is a txt file
        # check if it is a meta.txt file
        if os.path.isfile(f) and f[-4:] == '.txt' and f[-8:] != 'meta.txt':
            filter_junk_text(f)

    exit(0)

if __name__ == "__main__":
    main()
   
