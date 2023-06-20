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
    x = re.search("\s?[nN]ichtamtliche Lesefassung.*", pageText)

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
    z = re.search("\s[0-9]?\sPrüfungs\s-\sund\sStudienordnung*", pageText)

    if z:
        #pageText = re.sub(z[0], '', pageText)
        #pageText = removeEmptyLine(pageText)
        pageText = ''
    

    

    #des Bachelorstudiengangs Biomathematik v
    #an der Ernst -Moritz -Arndt -Universität Greifswald (v)
    # Promotionsordnung v
    #der Mathematisch -Naturwissenschaftlichen Fakultät v
    #der Ernst -Moritz -Arndt -Universität Greifswald  v
    #des Masterstudiengangs Mathematik v
    # Vom 12. Februar 2018  (v) 
    #


    #Titel Bachelor line
    bachelorLine = re.search("\sdes\sBachelor*studiengangs*", pageText)
    if bachelorLine:
        #pageText = re.sub(bachelorLine[0], '', pageText)
        pageText = ''

    masterLine = re.search("\sdes\sMasterstudiengangs*", pageText)
    if masterLine:
        #pageText = re.sub(masterLine[0], '', pageText)
        pageText = ''

    uniNameHeader = re.search("\sder\sErnst-Moritz-Arndt-Universität\sGreifswald", pageText)
    if uniNameHeader:
        #pageText = re.sub(uniNameHeader[0], '', pageText)
        pageText = ''

    dateHeader = re.search("\s[vV]om", pageText)
    if dateHeader:
        pageText = ''   #re.sub(dateHeader[0], '', pageText)

    promotionHeader = re.search("\sPromotionsordnung", pageText)
    if promotionHeader:
        #pageText = re.sub(promotionHeader[0], '', pageText)
        pageText = ''

    fakultaetHeader = re.search("\sder\sMathematisch*\s*", pageText)
    if fakultaetHeader:
        #pageText = re.sub(fakultaetHeader[0], '', pageText)
        pageText = ''

    psoHeader = re.search("\sPrüfungs- und Studienordnung", pageText)
    if psoHeader:
        #pageText = re.sub(psoHeader[0], '', pageText)
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

def removeEmptyLine(string):
    newPageText = ''

    my_string = string.split('\n', 1)[0]
    if my_string.strip():
        newPageText += my_string

    return newPageText

def filterJunkText(txtFile):
    #helping file to get content of txt file
    filteredDocument = ''
    documentContent = open(txtFile, 'r')

    #check in every line of the text if there is junk text there
    for line in documentContent:
        line = filterPageText(line)
        #print(line)
        filteredDocument += line

    #write filterd text into new directory
    nameIndex = txtFile.rfind('/')
    txtFile = txtFile[nameIndex+1:]
    #print(txtFile)
    f = open('filteredDocuments/' + txtFile, 'w')
    f.write(filteredDocument)
    f.close()

#convert pdf files in a dictionary into txt files
directory = 'data/examination_regulations_2'

#filtering out the junk text from the converted txt files
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    #check if is a txt file
    if os.path.isfile(f) and f[-4:] == '.txt':
        filterJunkText(f)


#for filename in os.listdir(directory):
#    f = os.path.join(directory, filename)
#    # checking if it is a file and if it ends with '.pdf'
#    if os.path.isfile(f) and f[-4:] == '.pdf':
        #in this line you change the pdt file to the txt file
        #how do you convert them?
#        pdfToTxt(f)
