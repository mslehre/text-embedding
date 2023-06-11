# importing required modules
import PyPDF2

# creating a pdf file object
pdfFileObj = open('examination_regulations/GPO-BMS_Lesefassung_AendS-2021-2.pdf', 'rb')


# creating a pdf reader object
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# printing number of pages in pdf file
#print(pdfReader.numPages)

# creating a page object
pageObj = pdfReader.pages[0]

# extracting text from page
print(pageObj.extract_text())

# closing the pdf file object

pdfFileObj.close()
