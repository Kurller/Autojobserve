from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from typing import List

app = FastAPI()

class Job(BaseModel):
    company_Names: str
    Location: str
    job_titles: str

def Driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disk-cache-size=0")
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    return driver

def login(driver, username, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)  # Let the page load

    # Simulate typing the username
    email_input = driver.find_element(By.ID, "username")
    email_input.clear()
    email_input.send_keys(username)

    # Simulate typing the password
    password_input = driver.find_element(By.ID, "password")
    password_input.clear()
    password_input.send_keys(password)

    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for the home page to load after login
    WebDriverWait(driver, 10).until(EC.url_contains("feed"))

def get_jobs(job_title, username, password):
    driver = Driver()
    login(driver, username, password)
    driver.get("https://www.linkedin.com/")

    # Enter job title
    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input'))
    )
    search_input.clear()
    search_input.send_keys(job_title)
    search_input.send_keys(Keys.RETURN)

    # Click on "Jobs" button
    jobs_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Jobs"]'))
    )
    jobs_button.click()

    # Click on the "Date Posted" filter
    try:
        # Wait for the "Date posted" dropdown to appear
        date_posted_dropdown = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'searchFilter_timePostedRange')))
        # Click on the "Date posted" dropdown
        date_posted_dropdown.click()

        # Click on "Past 24 hours"
        past_24_hours_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 't-14') and contains(@class, 't-black--light') and contains(@class, 't-normal') and text()='Past 24 hours']"))
        )
        past_24_hours_option.click()
        
        # Click on "Show results"
        show_results = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Apply current filter to show results']"))
        )
        show_results.click()

        # Wait for the search results to load
        time.sleep(5)  # Adjust as needed

        # Get job details
        job_elements = driver.find_elements(By.CLASS_NAME, "job-card-container__link")
        location_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__metadata-item ')
        company_elements = driver.find_elements(By.CLASS_NAME, 'job-card-container__primary-description ')

        # Ensure all arrays have the same length
        min_length = min(len(job_elements), len(location_elements), len(company_elements))
        job_titles = [x.text.strip() for x in job_elements[:min_length]]
        location_names = [y.text.strip() for y in location_elements[:min_length]]
        company_names = [z.text.strip() for z in company_elements[:min_length]]

        final = []

        for i in range(min_length):
            final.append({
                "company_Names": company_names[i],
                "Location": location_names[i],
                "job_titles": job_titles[i]
            })

        # Save new jobs to the database
        if final:
            return final
        else:
            raise Exception("No new jobs found")

    except TimeoutException as ex:
        raise Exception("Timeout while waiting for elements to load:", ex)
    finally:
        driver.quit()

@app.get("/jobs/", response_model=List[Job], tags=["jobs"])
def scrape_jobs(job_title: str = Query(..., description="The job title to search for")):
    # LinkedIn credentials
    username = "kolaquadry@gmail.com"
    password = "Adebola@12345"

    try:
        # Call your get_jobs function with the provided job title
        return get_jobs(job_title, username, password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
