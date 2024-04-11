from link2 import save_new_jobs_to_database
from selenium import webdriver
from link import simulate_typing
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def Linkedin_func():
    driver = None  # Initialize driver outside the try block
    try:
        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Navigate to LinkedIn login page
        driver.get('https://www.linkedin.com/')
        driver.implicitly_wait(5)  # Increase the implicit wait time
        
        # Simulate login
        email = driver.find_element(By.XPATH, '//*[@id="session_key"]')
        simulate_typing(email, 'bolaolad1@gmail.com')
        email.send_keys(Keys.ENTER)
        time.sleep(1)
        password = driver.find_element(By.XPATH, '//*[@id="session_password"]')
        simulate_typing(password, 'Kolawole@123')
        password.send_keys(Keys.ENTER)
        time.sleep(5)  

        # Navigate to LinkedIn jobs page
        driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3883409291&f_TPR=r86400&keywords=data%20scientist&origin=JOB_SEARCH_PAGE_JOB_FILTER")

        # Extract job titles, locations, and company names
        job_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__link')
        location_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__metadata-item')
        company_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__primary-description')

        job_details = []
        for job_element, location_element, company_element in zip(job_elements, location_elements, company_elements):
            job_title = job_element.text
            location = location_element.text
            company_name = company_element.text
            
            # Find the time element for the current job
            wait = WebDriverWait(driver, 10)
            time_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'hours ago')]")))

            #time_element = job_element.find_element(By.XPATH, '//span[contains(text(), "hours ago")]')
            posted_time_text = time_element.text.strip()  # Extract text directly
            if posted_time_text:
                # Parse the posted time
                hours_ago = int(posted_time_text.split()[0])  # Extract hours as integer
                posted_time = datetime.now() - timedelta(hours=hours_ago)  # Calculate the actual posted time
                print(posted_time)
                # Check if the job was posted within the last 24 hours
                if datetime.now() - posted_time < timedelta(days=1):
                    job_details.append({
                        "company_Names": company_name,
                        "job_titles": job_title,
                        "Location": location,
                        "posted_time":posted_time
                    })
                else:
                    raise Exception("Job posting is older than 24 hours")
            else:
                raise Exception("Posted time not found")

        # Create DataFrame from scraped data
        final = pd.DataFrame(job_details)

        # Save new jobs to the database
        if not final.empty:
            save_new_jobs_to_database(final)
        else:
            print("No new jobs posted within the last 24 hours")

    except Exception as e:
        print(e)
    finally:
        if driver:
            # Close the WebDriver session
            driver.quit()

Linkedin_func()
