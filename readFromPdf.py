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


#An ganze txt-Datei anwenden
def filterPageText(pageText):
    #header
    x = re.search("^\s?[nN]ichtamtliche Lesefassung.*", pageText)

    if x:
        #remove the found text
        pageText = re.sub(x[0], '', pageText)

    #TODO
    #filter the footer - common footer not found
    #filter the page number - remove the number at the beginning - dangerous
    #filter the table of contents?
    #title and date at the firt page

    #filter out the page numbers
    #still at work
    #y = re.search("^\s[0-9]", pageText)
        
    #if y:
        #print('Possible page number found')
        #print(y[0])
        #pageText = re.sub(y[0], '', pageText)

    #search title at the first page
    z = re.search("[0-9]\sPrüfungs\s-\sund\sStudienordnung*", pageText)

    if z:
        pageText = re.sub(z[0], '', pageText)
        pageText = removeEmptyLine(pageText)
    

    

    #des Bachelorstudiengangs Biomathematik v
    #an der Ernst -Moritz -Arndt -Universität Greifswald (v)
    # Promotionsordnung 
    #der Mathematisch -Naturwissenschaftlichen Fakultät  
    #der Ernst -Moritz -Arndt -Universität Greifswald  v
    #des Masterstudiengangs Mathematik v
    # Vom 12. Februar 2018  (v) 
    #


    #Titel Bachelor line
    bachelorLine = re.search("des\sBachelor*studiengangs*", pageText)
    if bachelorLine:
        pageText = re.sub(bachelorLine[0], '??', pageText)

    masterLine = re.search("des\sMasterstudiengangs*", pageText)
    if masterLine:
        pageText = re.sub(masterLine[0], '', pageText)

    uniNameHeader = re.search("an\sder\sErnst*Greifswald", pageText)
    if uniNameHeader:
        pageText = re.sub(uniNameHeader[0], '', pageText)

    dateHeader = re.search("^Vom.20[0-9][0-9]", pageText)
    if dateHeader:
        pageText = re.sub(dateHeader[0], '', pageText)

    promotionHeader = re.search("Promotionsordnung", pageText)
    if promotionHeader:
        pageText = re.sub(promotionHeader[0], '', pageText)

    fakultaetHeader = re.search("der\sMathematisch.Fakultät", pageText)
    if fakultaetHeader:
        pageText = re.sub(fakultaetHeader[0], '', pageText)



    return pageText

def removeEmptyLine(string):
    newPageText = ''

    my_string = string.split('\n', 1)[0]
    if my_string.strip():
        newPageText += my_string

    return newPageText

#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations'

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file and if it ends with '.pdf'
    if os.path.isfile(f) and f[-4:] == '.pdf':
        pdfToTxt(f)
