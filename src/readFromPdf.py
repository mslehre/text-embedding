import os
import re
import argparse
import subprocess

from src.chunker import try_to_write_dir

def pdfToTxt(pdfname):
    # creating a txt output file
    txtname = pdfname[:-4]
    txtname += ".txt"

    # creating a pdf file object
    pdfFileObj = open(pdfname, 'rb')
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # get total pages of pdf
    totalPages = len(pdfReader.pages)
    fileText = ''

    for i in range(totalPages):
        # creating a page object
        pageObj = pdfReader.pages[i]

        # extracting text from page
        pageText = pageObj.extract_text()

        # filter the junk text
        pageText = filterPageText(pageText) 
        
        # write the filtered text into a txt file
        fileText += pageText

    # closing the pdf file object
    pdfFileObj.close()

    # write the text from pdf to txt file
    output = open(txtname, 'w')
    output.write(fileText)

def filterPageText():
    # header
    x = re.search("\s[nN]ichtamtliche Lesefassung.*", pageText)

    if x:
        # remove the found text
        pageText = re.sub(x[0], '', pageText)

    # search title at the first page
    z = re.search("\s[0-9]?\sPrüfungs\s-\sund\sStudienordnung*", pageText)

    if z:
        # pageText = re.sub(z[0], '', pageText)
        pageText = ''
    
    # Titel Bachelor line
    bachelorLine = re.search("\sdes\sBachelor*studiengangs*", pageText)
    if bachelorLine:
        # pageText = re.sub(bachelorLine[0], '', pageText)
        pageText = ''

    masterLine = re.search("\sdes\sMasterstudiengangs*", pageText)
    if masterLine:
        # pageText = re.sub(masterLine[0], '', pageText)
        pageText = ''

    uniNameHeader = re.search("\sder\sErnst-Moritz-Arndt-Universität\sGreifswald", pageText)
    if uniNameHeader:
        # pageText = re.sub(uniNameHeader[0], '', pageText)
        pageText = ''

    dateHeader = re.search("\s[vV]om", pageText)
    if dateHeader:
        pageText = ''   # re.sub(dateHeader[0], '', pageText)

    promotionHeader = re.search("\sPromotionsordnung", pageText)
    if promotionHeader:
        # pageText = re.sub(promotionHeader[0], '', pageText)
        pageText = ''

    fakultaetHeader = re.search("\sder\sMathematisch*\s*", pageText)
    if fakultaetHeader:
        # pageText = re.sub(fakultaetHeader[0], '', pageText)
        pageText = ''

    psoHeader = re.search("\sPrüfungs- und Studienordnung", pageText)
    if psoHeader:
        # pageText = re.sub(psoHeader[0], '', pageText)
        pageText = ''

    psoHeader1 = re.search("Gemeinsame\sPrüfungsordnung\sfür", pageText)
    if psoHeader1:
        pageText = ''

    greifswaldHeader = re.search("\sder\sUniversität\sGreifswald", pageText)
    if greifswaldHeader:
        pageText = ''

    rpoHeader = re.search("\sRahmenprüfungsordnung", pageText)
    if rpoHeader:
        pageText = ''

    abPromoHeader = re.search("\sAusführungsbestimmungen\szum\sPromotionsverfahren", pageText)
    if abPromoHeader:
        pageText = ''

    return pageText

def filter_junk_text(txt_file):
    # helping file to get content of txt file
    filtered_document_text = ''
    document_content = open(txt_file, 'r')

    # check in every line of the text if there is junk text there
    for line in documentContent:
        line = filterPageText(line)
        # print(line)
        filtered_document_text += line

    # write filterd text into new directory
    file_name_index = txt_file.rfind('/')
    txt_file = txt_file[file_name_index+1:]
    f = open('filteredDocuments/' + txt_file, 'w')
    f.write(filtered_document_text)
    f.close()

def remove_line_if_junk():
    # check if it is not too specific
    junk_list = ['\s[nN]ichtamtliche Lesefassung.*', '\s[0-9]?\sPrüfungs\s-\sund\sStudienordnung*', '\sdes\sBachelor*studiengangs*',
                 '\sdes\sMasterstudiengangs*"', '\sder\sErnst-Moritz-Arndt-Universität\sGreifswald', '\s[vV]om', 
                 '\sPromotionsordnung', '\sder\sMathematisch*\s*', '\sPrüfungs- und Studienordnung', 'Gemeinsame\sPrüfungsordnung\sfür',
                 '\sder\sUniversität\sGreifswald', '\sRahmenprüfungsordnung', '\sAusführungsbestimmungen\szum\sPromotionsverfahren']

                
def filter_out_from_the_line(pattern, line):
    # header
    x = re.search(pattern, line)

    if x:
        # remove the found text
        line = re.sub(x[0], '', line)

    return line

    


# convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations_2'

# filtering out the junk text from the converted txt files
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # check if is a txt file
    if os.path.isfile(f) and f[-4:] == '.txt':
        filterJunkText(f)

def main():
    """Main to translate all PDF files in a specific folder into txt files that
    retain the layout, e.g. table
    """
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
    for filename in os.listdir(dir_path):
        f = os.path.join(dir_path, filename)
        # checking if it is a file and if it ends with '.pdf'
        if os.path.isfile(f) and f[-4:] == '.pdf':
            process = subprocess.Popen(["pdftotext", "-layout", f])

        # filter out the converted txt files
        # check if it is a txt file
        # check if it is a meta.txt file
        if os.path.isfile(f) and f[-4:] == '.txt' and f[-8:] != "meta.txt":
            filter




    exit(0)

if __name__ == "__main__":
    main()
   
