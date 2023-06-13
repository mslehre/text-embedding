# importing required modules
import PyPDF2
import os

def pdfToTxt(pdfname):
    #creating a txt output file
    txtname = pdfname[:-4]
    txtname += ".txt"

    # creating a pdf file object
    pdfFileObj = open(pdfname, 'rb')
    
    # creating a pdf reader object
    pdfReader = PyPDF2.PdfReader(pdfFileObj)

    # printing number of pages in pdf file
    #print(pdfReader.numPages)

    # creating a page object
    pageObj = pdfReader.pages[0]

    # extracting text from page
    fileText = pageObj.extract_text()

    # closing the pdf file object
    pdfFileObj.close()

    #write the text from pdf to txt file
    output = open(txtname, 'w')
    output.write(fileText)

#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file and if it is '.pdf' at the end
    if os.path.isfile(f) and f[-4:] == '.pdf':
        pdfToTxt(f)
