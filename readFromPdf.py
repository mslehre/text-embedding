# importing required modules
import PyPDF2

def pdfToTxt(pdfname, txtname):
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

#test variables
pdfTestName = 'examination_regulations/GPO-BMS_Lesefassung_AendS-2021-2.pdf'
txtTestName = 'GPO-BMS_Lesefassung_AendS-2021-2.txt'

pdfToTxt(pdfTestName, txtTestName)