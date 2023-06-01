#!/usr/bin/env python3

import typing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import datetime
import pandas


#def linkgrabber(profileURLs):
#    for URL in profileURLs:
        





def getJsCode(path: str) -> str:
    with open(path) as file:
        content = file.read()
    return content

def launchFirefox(geckoPath: str): 
    #geckodriver 0.33 added to PATH
    #included in snap on linux distributions of firefox
    
    #creates Options obeject
    options = Options()
    #add option to launch firefox headless
    options.add_argument("--headless=new")
    #driver path given as Service object
    serv = Service(geckoPath)

    #creates driver object with specified options
    driver = webdriver.Firefox(options=options, service=serv)
    driver.set_window_size(800,600)
    print("Headless Firefox Initialized")
    return driver

def navigateToWebsite(driver, URL: str, elementToWaitFor: str):
    #visit website specified under URL    
    dt = datetime.datetime.now()
    dtstr = dt.strftime('%d/%m/%Y %H:%M:%S')
    try:
        driver.get(URL)
    except:
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tError: Page \""+URL
                       +"\" could not be loaded.]"+Exception+"\n")
        return driver
    delay = 30 #timeout delay
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, elementToWaitFor)))
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tPage \""+URL+"\" loaded successfully.\n")
    except TimeoutException:
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tError: Page \""+URL
                       +"\" loading timeout.\n")
    except:
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tError: Element \""+elementToWaitFor
                       +"\" could not be loaded."+Exception+"\n")
    finally:    
        return driver

def exejscode(driver, jscode: str):
    #call to execute js code on website
    #data type of result is only determined on runtime
    #maybe typeof in js can be used to set return type
    dt = datetime.datetime.now()
    dtstr = dt.strftime('%d/%m/%Y %H:%M:%S')
    try:
        result = driver.execute_script(jscode)
    except:
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tError while executing script. "+Exception+"\n")
    finally:
        with open('dataAcquisitionLog.txt','a') as file:
            file.write("["+dtstr+"]\tExtracted "+str(len(result))+" links.\n")
        return result

#extract names and ID from spreadsheet and create data frame with URLs
def getNamesAndURLs(df: pandas.DataFrame) -> pandas.DataFrame:
    names_IDs_URLs = df[["Vorname","Nachname","ID"]]
    return names_IDs_URLs

#main function for testing
def main():
    #js code to be converted
    linkgrabber = getJsCode("js_scripts/linkgrabber.js")
    spreadsheet = pandas.read_csv("../../data/ProfsGW-proflist.csv")
    sub_df = getNamesAndURLs(spreadsheet)
    print(sub_df.to_string())
    #geckodriver location can differ
    driver = launchFirefox('/snap/bin/firefox.geckodriver')
    #time to login and accept cookies etc.
    time.sleep(60)
    for ID in sub_df["ID"]:
        if str(ID) == "nan":
            continue
        URL = "https://www.webofscience.com/wos/author/record/"+str(ID)
        driver = navigateToWebsite(driver, URL, 'snProfilesPublicationsBottom')
        linklist = exejscode(driver, linkgrabber)
        print(str(ID)+"\t"+str(len(linklist)))
        #linklist = filterForRelevantLinks(linklist)
        with open(ID+'.txt','a') as file:
            file.write(sub_df.loc[sub_df.ID == ID, "Vorname"].values[0]
                       +" "
                       +sub_df.loc[sub_df.ID == ID, "Nachname"].values[0]
                       +" "+str(ID)+"\n\n")
            for link in linklist:
                file.write(link[0]+"\t"+link[1]+"\n\n")
    driver.quit()
    

if __name__ == "__main__":
    main()