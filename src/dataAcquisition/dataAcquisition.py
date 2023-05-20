#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time



#def linkgrabber(profileURLs):
#    for URL in profileURLs:
        











def getJsCode(path):
    print("hallo2")
    with open(path) as file:
        content = file.read()
    print("Executing code: \n" + content)
    return content

def exejscode(jscode, URL): #geckodriver 0.33 added to PATH
    
    options = Options()
    options.add_argument("--headless=new")
    serv = Service('/snap/bin/firefox.geckodriver') #driver path
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.cookie.cookieBehavior", 2) #option 2 (no cookies allowed) will make the page not load properly

    driver = webdriver.Firefox(options=options, service=serv, firefox_profile=fp)
    driver.set_window_size(800,600)
    driver.get(URL)
    print ("Headless Firefox Initialized")
    time.sleep(30)
    result = driver.execute_script(jscode)
    driver.quit()
    return result



def main():
    #js code to be converted
    print("Hallo")
    jscode = getJsCode("linkgrabber.js")
    URL = "https://www.webofscience.com/wos/author/record/1177820"
    linklist = exejscode(jscode, URL)
    print(linklist)

if __name__ == "__main__":
    main()