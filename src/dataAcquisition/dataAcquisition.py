#!/usr/bin/env python3

import typing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time



#def linkgrabber(profileURLs):
#    for URL in profileURLs:
        











def getJsCode(path: str) -> str:
    with open(path) as file:
        content = file.read()
    print("Executing code: \n" + content)
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

def navigateToWebsite(driver, URL: str):
    #visit website specified under URL    
    driver.get(URL)
    #rudimentary wait function
    #should be implemented to wait for specific objects to be ready
    return driver

def exejscode(driver, jscode: str):
    #call to execute js code on website
    #data type of result is only determined on runtime
    #maybe typeof in js can be used to set return type
    result = driver.execute_script(jscode)
    return result

#main function for testing
def main():
    #js code to be converted
    cookies = getJsCode("js_scripts/wos_cookieClicker.js")
    gotIt = getJsCode("js_scripts/wos_gotItClicker.js")
    linkgrabber = getJsCode("js_scripts/linkgrabber.js")
    URL = "https://www.webofscience.com/wos/author/record/1177820"
    driver = launchFirefox('/snap/bin/firefox.geckodriver')
    time.sleep(10)
    driver = navigateToWebsite(driver, URL)
    time.sleep(15)
    bla = exejscode(driver, cookies)
    time.sleep(10)
    bla2 = exejscode(driver, gotIt)
    time.sleep(5)
    linklist = exejscode(driver, linkgrabber)
    driver.quit()
    for link in linklist:
        print(link[0]+"\t"+link[1]+"\n")
    

if __name__ == "__main__":
    main()