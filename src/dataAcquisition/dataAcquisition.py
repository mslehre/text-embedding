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
from os.path import exists

logPath = "../../data/publications/dataAcquisitionLog.txt"

def getJsCode(path: str) -> str:
    with open(path) as file:
        content = file.read()
    return content

def launchFirefox(geckoPath: str) -> webdriver.Firefox: 
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

#visit website specified under URL and wait for specific element
def navigateToWebsite(driver, URL: str,
                      elementToWaitFor: str) -> webdriver.Firefox:    
    dt = datetime.datetime.now()
    dtstr = dt.strftime('%d/%m/%Y %H:%M:%S')
    try:
        driver.get(URL)
    except:
        with open(logPath,'a') as file:
            file.write("["+dtstr+"]\tError: Page \""+URL
                       + "\" could not be loaded.]"
                       + type(Exception).__name_+"\n")
        return driver
    delay = 15 #timeout delay
    try:
        #wait for element to be loaded
        myElem = WebDriverWait(driver, delay).until(
                  EC.presence_of_element_located((By.ID, elementToWaitFor)))
        with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tPage \"" +URL
                       + "\" loaded successfully.\n")
    except TimeoutException:
        with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tError: Page \"" + URL
                       + "\" loading timeout.\n")
    except:
        with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tError: Element \"" + elementToWaitFor
                       + "\" could not be loaded."
                       + type(Exception).__name_ + "\n")
    finally:    
        return driver

#call to execute js code on website
#data type of result is only determined on runtime
#maybe typeof in js can be used to set return type
def exejscode(driver, jscode: str):
    dt = datetime.datetime.now()
    dtstr = dt.strftime('%d/%m/%Y %H:%M:%S')
    try:
        result = driver.execute_script(jscode)
    except:
        with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tError while executing script. "
                       + type(Exception).__name_ + "\n")
    finally:
        with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tExtracted " + str(len(result)) 
                       + " links.\n")
        return result

#extract names and ID from spreadsheet and create data frame with URLs
def getNamesAndURLs(df: pandas.DataFrame) -> pandas.DataFrame:
    names_IDs_URLs = df[["firstname","lastname","WoSID","id"]]
    return names_IDs_URLs

#function to filter for relevant links and return new list of links
def filterForRelevantLinks(linklist: list) -> list:
    dt = datetime.datetime.now()
    dtstr = dt.strftime('%d/%m/%Y %H:%M:%S')
    newLinklist = []
    for link in linklist:
        if "full-record" in link[1]:
            newLinklist.append(link)
    with open(logPath,'a') as file:
            file.write("[" + dtstr + "]\tFiltered to "
                       + str(len(newLinklist)) + " links.\n")
    return newLinklist

#main function for testing
def main():
    #js code to be converted
    linkgrabber = getJsCode("js_scripts/linkgrabber.js")
    spreadsheet = pandas.read_table("../../data/prof.tbl")
    sub_df = getNamesAndURLs(spreadsheet)
    #geckodriver location can differ
    driver = launchFirefox('/snap/bin/firefox.geckodriver')
    """
    Use time to:
    1. Make sure all sessions for WOS are ended in other browsers.
       Also close affected browsers.
    2. Use VPN of affiliated institution (not sure if necessary)
    3. After browser window is ready, visit webofscience.com
    4. Log in via your institution to gain full access to website
       make also sure to tick the box that says "Remember me for this session"
       When "Access denied" error occurs, delete cookies manually and resend
       the form (i.e. refresh page) afterwards.
    5. Accept cookies and dismiss other pop-ups
    6. Wait until program is finished and you regain control over shell
    """
    time.sleep(120)
    for ID in sub_df["id"]:
        WOSID = sub_df.loc[sub_df.id == ID,"WoSID"].values[0]
        if str(WOSID) == "nan":
            continue
        if exists("../../data/publications/" + str(ID) + ".txt"):
            continue
        #somehow the entries in the column are read as float, hence the cast
        URL = "https://www.webofscience.com/wos/author/record/"
        + str(int(WOSID))
        driver = navigateToWebsite(driver, URL, 'snProfilesPublicationsBottom')
        linklist = exejscode(driver, linkgrabber)
        linklist = filterForRelevantLinks(linklist)
        #write header
        with open(str(ID) + '.txt','a') as file:
            #sub_df.loc[...] returns "Vorname", "Nachname" from that row
            #where "ID" matches current ID in loop
            file.write(sub_df.loc[sub_df.id == ID, "firstname"].values[0]
                       + " "
                       + sub_df.loc[sub_df.id == ID, "lastname"].values[0]
                       + "," + str(int(WOSID)) + ";\n\n")
            #write links
            for link in linklist:
                file.write(link[0] + "\t" + link[1] + "\n\n")
    driver.quit()
    return 0

if __name__ == "__main__":
    main()
