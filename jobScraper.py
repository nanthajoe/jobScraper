import time
import pandas as pd
import requests

# Import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import json

# Setting driver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")

# Import chromedriver 
import chromedriver_binary
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Navigate 
url = 'https://www.cermati.com/karir/'
driver.get(url)

# Navigate to view all job
search = driver.find_element(By.XPATH, '//*[@id="career-landing"]/div/div[4]/div/a')
search.click()

#Create global variable to store the scraped jobs
jobsList = []

# Scraping function
def detailScraper():
        # Count Job List
        count_of_divs = len(driver.find_elements(By.CLASS_NAME, 'page-job-list-wrapper'))
        # Loop every job list
        for i in range(count_of_divs):
                try:
                        # Wait to scrap Department and Title
                        time.sleep(1)
                        driver.switch_to.window(driver.window_handles[0])
                        
                        # Department Name
                        departmentName = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[' + str(i+1) + ']/p[1]').text
                        # Job Title 
                        jobTitle = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[' + str(i+1) + ']/div[1]/strong').text

                        time.sleep(1)
                        #Click Apply Button
                        applyButton = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[' + str(i+1) + ']/a')
                        applyButton.click()

                        # Posted on
                        jobPosted = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[' + str(i+1) + ']/p[2]').text

                        # Wait until full load
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(2)

                        if jobPosted == "Indodana":
                                # Job Location
                                jobLocation = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/main/ul/li[1]/span/spl-job-location').text
                                jobType = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]/main/ul/li[2]').text
                        else:
                                # Job Location
                                jobLocation = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/main/ul/li[1]/span/spl-job-location').text
                                
                                # Job Type
                                jobType = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[1]/main/ul/li[2]').text

                        # Job Description
                        jobDescriptionList = []
                        html_list = driver.find_element(By.XPATH, '//*[@id="st-jobDescription"]/div[2]/ul')
                        items = html_list.find_elements(By.TAG_NAME, "li")
                        for item in items:
                                jobDescriptionList.append(item.text)

                        # Job Qualification
                        jobQualificationList = []
                        html_list = driver.find_element(By.XPATH, '//*[@id="st-qualifications"]/div[2]/ul')
                        items = html_list.find_elements(By.TAG_NAME, "li")
                        for item in items:
                                jobQualificationList.append(item.text)

                        # Store the scraped job
                        jobDict = {
                                departmentName: {
                                "title": jobTitle,
                                "location": jobLocation,
                                "description": jobDescriptionList,
                                "qualification": jobQualificationList,
                                "job_type": jobType,
                                }
                        }
                        jobsList.append(jobDict)
                        driver.close()
                except:
                       pass
                       driver.close()

        driver.switch_to.window(driver.window_handles[0])
        nextPage()

# Function to click next page
def nextPage():
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[11]/div/button[9]/i')))
        nextButton = driver.find_element(By.XPATH, '//*[@id="career-jobs"]/div/div[6]/div/div[11]/div/button[9]/i')
        nextButton.click()
        time.sleep(2)
        detailScraper()
    except:
        pass

# Main function
def main():
       detailScraper()
       # Write to json
       with open('solution.json', 'w') as f:
              json.dump(jobsList, f)
              
main()