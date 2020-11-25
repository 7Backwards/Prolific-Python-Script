import smtplib
import requests
import json
import time

from time import gmtime, strftime  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


try:
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=")
    driver = webdriver.Chrome(options=options)
    last_study = 0
except:
    print("Error driver creation")


while(True):
    try:
        time.sleep(10) # Refreshes every 10s, i recommend not going any lower as there might be security methods implemented
        resp = requests.get('https://www.prolific.co/api/v1/studies/?current=1', data={}, auth=('', '')) # Prolific ID and Password
        print(strftime("%H:%M:%S", gmtime()))
        print(resp)
        wjson = resp.content
        wjdata = json.loads(wjson)
        results = wjdata['results']
        
    except :
        print("Error requesting to api")
        continue

    if len(results) > 0:

        study_id = results[0]['id']
        if study_id != last_study:
            
            last_study = study_id
            total_available_places = results[0]['total_available_places']
            places_taken = results[0]['places_taken']
            description = results[0]['description']

            url = "https://app.prolific.co/studies/" + study_id 
            print(url)
            driver.get(url)
            window_name = driver.window_handles[0]
            driver.switch_to.window(window_name=window_name)
            wait = WebDriverWait(driver, 10)
            while (True):
                try:
                    
                    search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-button--primary')))
                    search.click()
                    search1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-button--primary')))
                    search1.click()
                    
                    print("Button clicks done")
                    print('taking screenshot')
                    driver.save_screenshot('./' + study_id + '_survey_.png') #Capture the screen
                    if search != search1:
                        
                        try:
                            print("Sending email")
                            fromaddr = '' # From Email Address
                            toaddrs  = '' # To Email Address
                            msg = 'Prolific' + description + '\n URL: ' + url 
                            username = '' # From Email Address Username
                            password = '' # From Email Address Password
                            server = smtplib.SMTP('smtp.gmail.com:587')
                            server.ehlo()
                            server.starttls()   
                            server.login(username,password)
                            server.sendmail(fromaddr, toaddrs, msg)
                            server.quit()
                            print("Email sent")
                            break
                        except:
                            print("Error sending email")
                            break
                    else:
                        print("Button clicks not the same")
                        alertText = driver.find_element_by_class_name('el-notification__content').text
                        if alertText == "The study is no longer active. We apologise for the inconvenience. Your account is in good standing." or alertText == "The study is full and therefore submissions can't be accepted at this time. We apologise for the inconvenience. Your account is in good standing." or alertText == "Sorry we can't create a new submission for you at this time as you currently have an active submission. Please complete or return the submission associated with study A study about products before starting a new submission." or alertText =="Sorry, you cannot participate in this study at this time. Only one participant per household can take each study. Don't worry - the block is for this study only and does not apply in general. However, you may see it again if someone else in your household (or the same building) takes another study before you could. We will be implementing additional authentication to allow users to bypass this block in the near future. No action is required at this time" or alertText == "You are ineligible to take part in this study. We apologise for the inconvenience. Your account is in good standing.":
                            print("Study closed")
                            break
                        else:
                            driver.refresh()
                except :
                    print("Error")
                    break
                
