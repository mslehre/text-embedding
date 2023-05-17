#!/usr/bin/env python3

from selenium import webdriver
import time



#def linkgrabber(profileURLs):
#    for URL in profileURLs:
        











def getJsCode(path):
    print("hallo2")
    with open(path) as file:
        content = file.read()
    return content

def exejscode(jscode, URL): #PhantomJS binary might be needed to be added to PATH
    
    driver = webdriver.PhantomJS()
    driver.get(URL)
    time.sleep(10)
    result = driver.execute_script(jscode)
    driver.quit()
    return result



def main():
    #js code to be converted
    print("Hallo")
    jscode = getJsCode("linkgrabber.js")
    URL = "https://www.google.com"
    linklist = exejscode(jscode, URL)
    print(linklist)

if __name__ == "__main__":
    main()