from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from link2 import save_new_jobs_to_database
from link import simulate_typing
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
    simulate_typing(email_input, username)

    # Simulate typing the password
    password_input = driver.find_element(By.ID, "password")
    simulate_typing(password_input, password)

    # Click the login button
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()

    # Wait for the home page to load after login
    WebDriverWait(driver, 10).until(EC.url_contains("feed"))
    return driver
def get_jobs(job_title):
    driver = Driver()
    login(driver, username, password)  # Use the provided username and password here
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

        final = pd.DataFrame({
            "company_Names": company_names,
            "Location": location_names,
            "job_titles": job_titles
        })

        print(final)

        # Save new jobs to the database
        if not final.empty:
            save_new_jobs_to_database(final)
        else:
            print("No new jobs found")

    except TimeoutException as ex:
        print("Timeout while waiting for elements to load:", ex)


# LinkedIn credentials
username = "kolaquadry@gmail.com"
password = "Adebola@12345"

# Job title to search for
job_title = "Software"
#get_jobs(job_title)
