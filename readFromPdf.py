# importing required modules
import PyPDF2
import os
import re

def pdfToTxt(pdfname):
    #creating a txt output file
    txtname = pdfname[:-4]
    txtname += ".txt"

    # creating a pdf file object
    pdfFileObj = open(pdfname, 'rb')
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # get total pages of pdf
    totalPages = len(pdfReader.pages)
    fileText = ''

    #get document info
    info = pdfReader.metadata

    #test got metadata
    #print(info.author)
    #print(info.creator)
    #print(info.producer)
    #print(info.subject)
    #print(info.title)
    #print('==================================')

    for i in range(totalPages):
        # creating a page object
        pageObj = pdfReader.pages[i]

        # extracting text from page
        pageText = pageObj.extract_text()

        #create test string to find distinguish features of header
        #without newlines to be able to check it with regex
        fileTextRegex = pageText.replace('\n', '_')

        #print(fileTextRegex)

        #search pattern Nichtamtliche ... 20xx
        #x = re.search("^Nichtamtliche.*20[0-9][0-9]", fileTextRegex)
        y = re.search("^Nichtamtliche Lesefassung.*", pageText)

        #if x:
        #    print('Header with "Nichtamliche ... 20xx" found ')

        if y:
            #print(y[0])
            pageText = re.sub(y[0], '', pageText)

        #write the filtered text into a txt file
        fileText += pageText


    # closing the pdf file object
    pdfFileObj.close()

    #write the text from pdf to txt file
    output = open(txtname, 'w')
    output.write(fileText)

#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file and if it ends with '.pdf'
    if os.path.isfile(f) and f[-4:] == '.pdf':
        pdfToTxt(f)
