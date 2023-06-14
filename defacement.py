from argparse import Action
from os.path import exists
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from selenium import webdriver
from PIL import Image
from PIL import ImageChops
import requests
import json
import sys
import time
from datetime import date
import requests
import hashlib
import logging
import sys
import multiprocessing
import configparser
import subprocess, sys
import os

configFilePath = r'E:\Defacement\config_file.txt'
parser=configparser.ConfigParser()
parser.read(configFilePath)
allurls=parser.get("config","Allurls").split("\n")
Tolerance=parser.get("config","Tolerance").split("\n")
sitehash=parser.get("config","Hash").split("\n")
hashblacklist=parser.get("config","Hashblacklist").split("\n")
defacechannelwebhook=parser.get("config","Defacechannelwebhook")
healthcheckwebhook=parser.get("config","Healthcheckwebhook")
screenshotblacklists=parser.get("config","Screenshotblacklists")

'''
mylogs = logging.getLogger(__name__)
fieldstyle = {'asctime': {'color': 'green'},
              'levelname': {'bold': True, 'color': 'black'},
              'filename':{'color':'cyan'},
              'funcName':{'color':'blue'}}                                 
levelstyles = {'critical': {'bold': True, 'color': 'red'},
               'debug': {'color': 'green'}, 
               'error': {'color': 'red'}, 
               'info': {'color':'magenta'},
               'warning': {'color': 'yellow'}}
coloredlogs.install(level=logging.DEBUG,
                    logger=mylogs,
                    fmt='%(asctime)s [%(levelname)s] - [%(filename)s > %(funcName)s() > %(lineno)s] - %(message)s',
                    datefmt='%H:%M:%S',
                    field_styles=fieldstyle,
                    level_styles=levelstyles)
'''
class ImageCompareException(Exception):
    """
    Custom Exception class for imagecompare's exceptions.
    """
    pass


log_file = open('logpro.txt', "a+")
def print_element(text):
    print(text)
    log_file.write(text + '\n')

def pixel_diff(image_a, image_b):

    if image_a.size != image_b.size:
        raise ImageCompareException(
            "different image sizes, can only compare same size images: A=" + str(image_a.size) + " B=" + str(
                image_b.size))

    if image_a.mode != image_b.mode:
        raise ImageCompareException(
            "different image mode, can only compare same mode images: A=" + str(image_a.mode) + " B=" + str(
                image_b.mode))

    diff = ImageChops.difference(image_a, image_b)
    diff = diff.convert('L')

    return diff


def total_histogram_diff(pixel_diff):
   
    return sum(i * n for i, n in enumerate(pixel_diff.histogram()))


def image_diff(image_a, image_b):

    histogram_diff = total_histogram_diff(pixel_diff(image_a, image_b))

    return histogram_diff


def is_equal(image_a, image_b, tolerance):
   
    return image_diff_percent(image_a, image_b) <= tolerance


def image_diff_percent(image_a, image_b):

    close_a = False
    close_b = False
    if isinstance(image_a, str):
        
        image_a = Image.open(image_a)
        close_a = True
        
    if isinstance(image_b, str):
            
        image_b = Image.open(image_b)
        close_b = True
    
    try:
        input_images_histogram_diff = image_diff(image_a, image_b)
        black_reference_image = Image.new('RGB', image_a.size, (0, 0, 0))
        white_reference_image = Image.new('RGB', image_a.size, (255, 255, 255))
        worst_bw_diff = image_diff(black_reference_image, white_reference_image)
        percentage_histogram_diff = (input_images_histogram_diff / float(worst_bw_diff)) * 100
    
    finally:
        if close_a:
            image_a.close()
        if close_b:
            image_b.close()

    return percentage_histogram_diff

def send_email(FDB1,FDB2):
    setup_script = 'E:\\Defacement\\email.ps1'
    p = subprocess.run([
        "powershell.exe", 
        "-File", 
        setup_script,
        FDB1,
        FDB2
        ],
        stdout=sys.stdout)
    print("Email Sent")

def slack_alert(message,url,channelname):
    message = str(message)
    title = (f"New Incoming Message :zap:")
    slack_data = {
        "username": "DefaceBot",
        "icon_emoji": ":satellite:",
        "channel" : channelname,
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

def sendRequest(url):
        resUrl = requests.get(url)
        resultUrl = str(resUrl.content)
        return resultUrl

def convertRequestToHash(content):
        hashUrl = hashlib.md5(content.encode())
        resApp = hashUrl.hexdigest()
        return resApp

def hashcheck(url,hashed):
     global non_match
     non_match=[]
     reqUrl = url
     hashUrl = hashed
     hashResult = convertRequestToHash(sendRequest(reqUrl))
     print("*****************************************")
     print(f"Http response code = {requests.get(reqUrl).status_code}")
     if url in hashblacklist:
         return True
     elif hashUrl == hashResult:  
            return True
            '''
        #enable if only you had body curl data
         list_a = sendRequest(reqUrl)
         asp=list_a.split()
         list_b = sendRequest(reqUrl)
         bsp=list_b.split()
         non_match = list(set(asp)-set(bsp))
            '''
         #print("No match elements:", non_match)
     return False


def slack_alert(message,url,channelname):
    message = str(message)
    title = (f"New Incoming Message :zap:")
    slack_data = {
        "username": "DefaceBot",
        "icon_emoji": ":satellite:",
        "channel" : channelname,
        "attachments": [
            {
                "color": "#9733EE",
                "fields": [
                    {
                        "title": title,
                        "value": message,
                        "short": "false",
                    }
                ]
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url,data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

def sendRequest(url):
        resUrl = requests.get(url,verify=False,timeout=30)
        resultUrl = str(resUrl.content)
        return resultUrl

def convertRequestToHash(content):
        hashUrl = hashlib.md5(content.encode())
        resApp = hashUrl.hexdigest()
        return resApp

def hashcheck(url,hashed):
     global non_match
     non_match=[]
     reqUrl = url
     hashUrl = hashed
     hashResult = convertRequestToHash(sendRequest(reqUrl))
     print("*****************************************")
     print(f"Http response code = {requests.get(reqUrl,verify=False,timeout=30).status_code}")
     if url in hashblacklist:
         return True
     elif hashUrl == hashResult:  
            return True
            '''
        #enable if only you had body curl data
         list_a = sendRequest(reqUrl)
         asp=list_a.split()
         list_b = sendRequest(reqUrl)
         bsp=list_b.split()
         non_match = list(set(asp)-set(bsp))
            '''
         #print("No match elements:", non_match)
     return False


def screenshot(url,filename):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(r"E://Defacement//chromedriver.exe", options=chrome_options)


    try:
        driver.get(url)
        body = driver.find_element_by_tag_name("body")
        time.sleep(60)
        body_ss = body.screenshot(filename)
        driver.execute_script("window.open('')")  # Create a separate tab than the main one
        driver.switch_to.window(driver.window_handles[-1])  # Switch window to the second tab
        driver.get('chrome://settings/clearBrowserData')  # Open your chrome settings.
        actions=ActionChains(driver)
        actions.send_keys(Keys.TAB * 2 + Keys.DOWN * 4 + Keys.TAB * 5 + Keys.ENTER)
        #time.sleep(1)
        actions.perform()
        driver.close()  # Close that window
        driver.quit()
        print("success")
    except:
        print("Can not found page")
        logging.warning(url+"Down")
        driver.close()
        driver.quit()
        return False
    

def Im_alive():
    slack_alert("Service Health Checked ^--^",healthcheckwebhook,"deface-healthcheck")
    print("I am Alive :)")
    #mylogs.info("I am Alive :)")


def processString(txt):
    specialChars = "!#$%^&*()/.:" 
    specialCharset=['https','www']
    for specialChar in specialChars:
        txt = txt.replace(specialChar,'')
    for specialChar in specialCharset:
        txt = txt.replace(specialChar,'')
    return(txt)

def file_check(filename):
    if exists(filename):
        existence=True
        return(existence)
    else :
        existence=False
        return(existence)

def url_check(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(r"E://Defacement//chromedriver.exe", options=chrome_options)
    try:
        driver.get(url)
        driver.find_element_by_tag_name("body")#find_element(by=By.TAG_NAME, value=body)
        driver.close()
        driver.quit()
        return True

    except:
        print("Can not found page")
        driver.close()
        driver.quit()
        return False

def counter(allurls):
    return len(allurls)

def resize(pic1,pic2):
    img1 = Image.open(pic1)
    img2 = Image.open(pic2)
    n_img1 = img1.resize((1920,916))
    n_img2 = img2.resize((1920,916))
    n_img1.save(pic1)
    n_img2.save(pic2)
    img1.close()
    img2.close()

def save_poc(time,file,url):
    Image.open(file)

def screenshotblackchcker(url):
    if url in screenshotblacklists:
        return False 
    else:
        return True

def main(counter):
    sturl=allurls[counter]
    stolerance=float(Tolerance[counter])
    shash=sitehash[counter]
    clrurl = processString(sturl)
    filename1="E:\\Defacement\\"+clrurl+"FDBshot.png"
    filename2="E:\\Defacement\\"+clrurl+"Secshot.png"
    url_tick=url_check(sturl)
    screenshotblacklist=screenshotblackchcker(sturl)
    if (url_tick):
        if(screenshotblacklist):    
            if (file_check(filename1)):
                screenshot(sturl,filename2)
                resize(filename2,filename2)
            else:
                screenshot(sturl,filename1)
                screenshot(sturl,filename2)
                resize(filename1,filename2)
            
            same = is_equal(filename1,filename2, stolerance)
            percentage = image_diff_percent(filename1,filename2)
        else:
            same=True
            percentage=0
    
        hashresult=hashcheck(sturl,shash)
        print(percentage,same,hashresult,sturl)
        if (
            (
                ( percentage>stolerance ) and ( same is not True )
                ) or ( hashresult is not True )
            ):
            
            evipath="E:\\Defacement\\defacedshotpoc\\"+clrurl + processString(str(datetime.now())) + "Evishot.png"
            if(screenshotblacklist):
                img=Image.open(filename2)
                img.save(evipath)
            else:
                evipath=""
                pass
            slack_alert("Critical : The " +sturl+ "  Is Defaced , Changes : "+str(percentage) + evipath,defacechannelwebhook,"deface-alert")
            send_email(filename1,evipath)
            #mylogs.warning("Critical : The " +sturl+ "  Is Defaced , Changes : "+str(percentage) + evipath)
            #slack_alert("Critical : The " +sturl+ "  Is Defaced , Changes : "+str(percentage) + evipath+" HTML Body Change Detail:"+str(non_match) ,defacechannelwebhook,"deface-alert")
            #mylogs.warning("Critical : The " +sturl+ "  Is Defaced , Changes : "+str(percentage) + evipath+" HTML Body Change Detail:"+str(non_match))
            
    elif (url_tick==False):
        #slack_alert("Warning : The "+sturl+" Is Down or Not Working Properly",defacechannelwebhook,"deface-alert")
        pass
if __name__ == "__main__":   
    pool = multiprocessing.Pool()
    start_time = time.perf_counter()
    processes = [pool.apply_async(main, args=(x,)) for x in range(counter(allurls))]
    result = [p.get() for p in processes]
    finish_time = time.perf_counter()
    Im_alive()
    print(f"Program finished in {finish_time-start_time} seconds")
    print(result)
    #mylogs.info("end"+str(finish_time-start_time))
    os.system('cmd /c "taskkill /F /IM chrome.exe /T > nul"')  
    exit()
