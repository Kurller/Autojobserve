from link2 import save_new_jobs_to_database
from selenium import webdriver
from link import simulate_typing
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from link3 import parse_relative_time
from datetime import datetime, timedelta

def Linkedin_func():
    global scraped_job_ids
    scraped_job_ids = set()
    try:
        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Navigate to LinkedIn login page
        driver.get('https://www.linkedin.com/')
        driver.implicitly_wait(3)
        
        email = driver.find_element(By.XPATH, '//*[@id="session_key"]')
        simulate_typing(email, 'kolaquadry@gmail.com')

        email.send_keys(Keys.ENTER)
        time.sleep(1)
        password = driver.find_element(By.XPATH, '//*[@id="session_password"]')
        simulate_typing(password, 'Adebola@12345')

        password.send_keys(Keys.ENTER)
        time.sleep(5)  

        # Navigate to LinkedIn jobs page
        driver.get("https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3834669915&discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII")

        # Extract job titles, locations, and company names
        job_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__link')
        location_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__metadata-item')
        company_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__primary-description')
        relative_times = driver.find_elements(By.XPATH, '//span[contains(text(), "minutes ago")]')
        
        job_details = []
        for job_element, location_element, company_element, relative_time in zip(job_elements[:5], location_elements[:5], company_elements[:5], relative_times[:5]):
            job_title = job_element.text
            location = location_element.text
            company_name = company_element.text
            relative_time_text = relative_time.text  # Added this line
            print("Relative Time Text:", relative_time_text)  # Added this line
            job_time = parse_relative_time(relative_time_text)
            
            if job_time:
                print("Job time:", job_time)
                print("Difference:", datetime.now() - job_time)
                if datetime.now() - job_time < timedelta(days=1):
                    job_details.append({
                        "company_Names": company_name,
                        "job_titles": job_title,
                        "Location": location
                    })
                    
        # Create DataFrame from scraped data
        final = pd.DataFrame(job_details)

        # Save new jobs to the database
        save_new_jobs_to_database(final)
     

    except Exception as e:
        print(e)
    finally:
        # Close the WebDriver session
        driver.quit()

Linkedin_func()
