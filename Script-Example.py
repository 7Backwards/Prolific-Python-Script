import smtplib
import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

while(True):
    try:
        time.sleep(10) # Refreshes every 10s, i recommend not going any lower as there might be security methods implemented
        resp = requests.get('https://www.prolific.co/api/v1/studies/?current=1', data={}, auth=('', '')) # Prolific ID and Password
        print(resp)
        wjson = resp.content
        wjdata = json.loads(wjson)
        results = wjdata['results']
    except :
        print("Error requesting to api")
        continue

    if len(results) > 0:

        study_id = results[0]['id']
        total_available_places = results[0]['total_available_places']
        places_taken = results[0]['places_taken']
        description = results[0]['description']

        url = "https://app.prolific.co/studies/" + study_id 
        print(url)
        while (True):
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("user-data-dir=") # Google Chrome User Data Folder
                #options.add_argument('-headless') # Comment if you want to see chrome appearing
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                wait = WebDriverWait(driver, 10)
                
                search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-button--primary')))
                search.click()
                search1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'el-button--primary')))
                search1.click()
                
                print("Button clicks done")
                if search != search1:
                    
                    print("Sending email")
                    fromaddr = '' # From Email Address
                    toaddrs  = '' # To Email Address
                    msg = description + '\n URL: ' + url 
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
                else:
                    print("Button clicks not the same")
                    alertText = driver.find_element_by_class_name('el-notification__content').text
                    if alertText == "The study is no longer active. We apologise for the inconvenience. Your account is in good standing.":
                        driver.close()
                        break
            except :
                print("Error")
                
            driver.close()