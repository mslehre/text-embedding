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

    for i in range(totalPages):
        # creating a page object
        pageObj = pdfReader.pages[i]

        # extracting text from page
        pageText = pageObj.extract_text()

        #filter the junk text
        pageText = filterPageText(pageText) 
        
        #write the filtered text into a txt file
        fileText += pageText

    # closing the pdf file object
    pdfFileObj.close()

    #write the text from pdf to txt file
    output = open(txtname, 'w')
    output.write(fileText)

def filterPageText(pageText):
    #header
    x = re.search("^[nN]ichtamtliche Lesefassung.*", pageText)

    if x:
        #remove the found text
        pageText = re.sub(x[0], '', pageText)

    #TODO
    #filter the footer - common footer not found
    #filter the page number
    #filter the table of contents?
    #title and date at the firt page

    #filter out the page numbers
    #still at work
    y = re.search("^\s[0-9]", pageText)
        
    if y:
        #print('Possible page number found')
        #print(y[0])
        pageText = re.sub(y[0], '', pageText)

    return pageText


#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file and if it ends with '.pdf'
    if os.path.isfile(f) and f[-4:] == '.pdf':
        pdfToTxt(f)
