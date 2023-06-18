from chunker import try_to_write_dir

#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations_2'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file and if it ends with '.pdf'
    if os.path.isfile(f) and f[-4:] == '.pdf':
        pdfToTxt(f)

def main():
    parser = argparse.ArgumentParser(description = 'Translates all PDF files' +
                        ' from a given folder into text files while' +
                        ' retaining the layout including table structures.' +
                        ' The new text files will be located in the same' +
                        '  directory as the PDF files.')
    parser.add_argument('-d', '--dir_path', type = try_to_write_dir, 
                        default = './',
                        help = 'Directory in which all PDF files are saved.')
    args = parser.parse_args()

    dir_path = os.path.join(args.dir_path, '')  # append '/' if not there
    for filename in os.listdir(directory):
        f = os.path.join(dir_path, filename)
        # checking if it is a file and if it ends with '.pdf'
        if os.path.isfile(f) and f[-4:] == '.pdf':
            pdfToTxt(f)

    exit(0)

if __name__ == "__main__":
    main()
