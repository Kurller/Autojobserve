from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import json

EMAIL = "seyiidowu24@yahoo.com"
# SEARCH = input("what job are you searching for: ").lower()
# PRICE = int(input("what is the least price you are looking out for in pounds: "))
CV = "/Users/mac/PycharmProjects/jobs/seyifunmi_idowu.docx"
STATUS = ""
SALARY = ""


def job_title():
    global job_pos
    # checking for job title
    job_position = driver.find_element_by_id('td_jobpositionlink')
    job_pos = job_position.text
    return job_pos


def job_post():
    global posted_by
    # job posted by
    poster = driver.find_element_by_id('td_posted_by')
    posted = poster.text.split(":")
    posted_by = posted[1].lstrip()
    return posted_by


def salary():
    global least_salary
    # checking salary range
    try:
        salary = driver.find_element_by_id('td_location_salary').text
        salary_re = re.findall("\d+", salary)
        least_salary = int(salary_re[0])
    except IndexError:
        least_salary = 0
    return least_salary


def job_apply():
    # applying for the job
    driver.find_element_by_link_text("Apply").click()

    #filling in the forms
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#appFrame")))
    email = driver.find_element_by_css_selector(".questionblock2>.questionInput>input")
    email.send_keys(EMAIL)
    Select(driver.find_element_by_id("Q0133_ans")).select_by_visible_text("Sponsorship Required")
    driver.find_element_by_id('filCV').send_keys("/Users/mac/PycharmProjects/jobs/seyifunmi_idowu.docx")
    driver.find_element_by_class_name('AppButton').click()
    #closing the form
    driver.switch_to.default_content()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="frm1"]/div[9]/div[1]/a').click()


def save_database(num):
    # saving to database
    jobs_dict = {
        f"job{num}": {
            "Job_title": job_pos,
            "Salary": SALARY,
            "Status": STATUS,
            "Posted_by": posted_by
        }
    }

    try:
        with open("jobs.json", "r") as file:
            # reading the data
            data = json.load(file)

    except FileNotFoundError:
        with open("jobs.json", "w") as file:
            # writing into the data
            json.dump(jobs_dict, file, indent=4)

    else:
        # updating the data
        data.update(jobs_dict)

        with open("jobs.json", "w") as file:
            # writing into the data
            json.dump(data, file, indent=4)

    print("successfully saved")


PATH ="/Library/chromedriver"
driver = webdriver.Chrome(PATH)
wait = WebDriverWait(driver, 100)
driver.maximize_window()
# driver.get("https://www.jobserve.com/gb/en/Job-Search/")

# driver.find_element_by_xpath('//*[@id="txtKey"]').send_keys("python developer")
# Select(driver.find_element_by_id("selAge")).select_by_visible_text("Within 7 days")
# driver.find_element_by_id("btnSearch").click()

driver.get("https://www.jobserve.com/gb/en/JobSearch.aspx?shid=AB5F55996470F7F7D9E8")

time.sleep(2)

job_title()
print(job_pos)

job_post()
print(posted_by)

salary()
print(least_salary)

#checking for salary range
if least_salary >= 50:

    # job_apply()

    STATUS = "Applied"
    SALARY = least_salary

else:
    #not applied cause lesser salary
    STATUS = "Not Applied"
    SALARY = least_salary

save_database(num=1)


#all the other jobs
jobs = driver.find_elements_by_class_name("newjobsum")

for x in range(3):

    jobs[x].click()

    time.sleep(5)

    job_title()
    print(job_pos)

    job_post()
    print(posted_by)

    salary()
    print(least_salary)

    #checking job description
    data = driver.find_element_by_id("td_jobpositionlink")

    # #checking if job description is in  the job
    # if "data science" in data.text:
    #
    #checking for salary range
    if least_salary >= 50:

        # job_apply()

        STATUS = "Applied"
        SALARY = least_salary

    else:
        #not applied cause lesser salary
        STATUS = "Not Applied"
        SALARY = least_salary

    save_database(num=x+2)

# driver.close()
# index = "IndexError"







#
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# import re
#
# EMAIL = "seyiidowu24@yahoo.com"
# PATH ="/Library/chromedriver"
# driver = webdriver.Chrome(PATH)
# driver.maximize_window()
# wait = WebDriverWait(driver, 20)
# # driver.get("https://www.jobserve.com/gb/en/Job-Search/")
# # driver.find_element_by_xpath('//*[@id="txtKey"]').send_keys("Data Scientist")
# # driver.find_element_by_id("btnSearch").click()
#
#
# driver.get("https://www.jobserve.com/gb/en/JobSearch.aspx?shid=AB5F55996470F7F7D9E8")
# jobs = driver.find_elements_by_class_name("newjobsum")
#
# time.sleep(3)
# for x in range(4):
#     jobs[x].click()
#     time.sleep(5)
#     job_position = driver.find_element_by_id('td_jobpositionlink')
#     print(job_position.text)
#
#     salary = driver.find_element_by_id('td_location_salary').text
#     salary_re = re.findall("\d+", salary)
#     least_salary = salary_re[0]
#     print(least_salary)
#
#     posted_by = driver.find_element_by_id('td_posted_by')
#     posted = posted_by.text.split(":")
#     print(posted[1])
#     print("===========================")
#
#
# # if "data scientist" in job_position.text.lower():
# #     driver.find_element_by_link_text("Apply").click()
# #     wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#appFrame")))
# #     email = driver.find_element_by_css_selector(".questionblock2>.questionInput>input")
# #     email.send_keys(EMAIL)
# #     Select(driver.find_element_by_id("Q0133_ans")).select_by_visible_text("Sponsorship Required")
# #     driver.find_element_by_id('filCV').send_keys("/Users/mac/PycharmProjects/jobs/seyifunmi_idowu.docx")
# #     driver.find_element_by_class_name('AppButton').click()
# #     driver.switch_to.default_content()
# #
# #     driver.find_element_by_xpath('//*[@id="frm1"]/div[9]/div[1]/a').click()
#
#
# # for x in range(2):
# #     jobs[x].click()
# #     time.sleep(5)
# #     data = driver.find_element_by_id("td_jobpositionlink")
# #     if "data scientist" in data.text.lower():
# #         driver.find_element_by_link_text("Apply").click()
# #         wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#appFrame")))
# #         email = driver.find_element_by_css_selector(".questionblock2>.questionInput>input")
# #         email.send_keys(EMAIL)
# #         Select(driver.find_element_by_id("Q0133_ans")).select_by_visible_text("Sponsorship Required")
# #         driver.find_element_by_id('filCV').send_keys("/Users/mac/PycharmProjects/jobs/seyifunmi_idowu.docx")
# #         driver.find_element_by_class_name('AppButton').click()
#
#