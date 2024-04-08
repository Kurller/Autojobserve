from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from link import simulate_typing
import time
from selenium.webdriver.common.keys import Keys
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
driver.get("https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3834669915&discover=recommended&discoveryOrigin=JOBS_HOME_JYMBII")
elements = driver.find_elements(By.XPATH, "//time")

# Iterate over the list of elements and access their text
for element in elements:
    print(element.text)  # 