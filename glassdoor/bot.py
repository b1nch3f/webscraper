import os
import time
import random

from seleniumbase import Driver
from selenium import webdriver
from selenium.webdriver.common.by import By

from dotenv import load_dotenv

load_dotenv()


def click_submit_button(driver):
    submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
    submit_button.click()


def login(driver, login_url):
    url = login_url
    driver.uc_open_with_reconnect(url, random.uniform(30, 45))
    driver.uc_gui_click_captcha()

    driver.find_element(By.ID, "inlineUserEmail").send_keys(os.getenv("EMAIL"))
    click_submit_button(driver)
    time.sleep(random.uniform(5, 10))

    driver.find_element(By.ID, "inlineUserPassword").send_keys(os.getenv("PASSWORD"))
    click_submit_button(driver)
    time.sleep(random.uniform(5, 10))


def get_salary_data(driver, salary_url, run_id, page, data_dir):
    url = salary_url
    driver.uc_open_with_reconnect(url, random.uniform(30, 45))
    driver.uc_gui_click_captcha()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
    time.sleep(random.uniform(5, 10))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.6);")
    time.sleep(random.uniform(5, 10))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(5, 10))

    # Find salary sections
    sections = driver.find_elements(By.CLASS_NAME, "SalariesList_SalariesList__S8vdZ")

    # Extract from second section if available
    if len(sections) > 1:
        salary_info = sections[1].text
        # print("\nExtracted Salary Info:\n", salary_info)

        file_name = f"{run_id}_{page}.txt"
        file_path = os.path.join(data_dir, file_name)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(salary_info + "\n\n" + "-" * 40 + "\n\n")
            print(f"Salary info written to '{file_path}'.")
    else:
        print("Salary section not found (less than 2 sections found).")


if __name__ == "__main__":
    RUN_ID = "65c479"

    DATA_DIR = "data"
    os.makedirs(DATA_DIR, exist_ok=True)

    BASE_URL = "https://www.glassdoor.co.in"
    LOGIN_URL = f"{BASE_URL}/profile/login_input.htm"

    proxy_username = os.getenv("PROXY_USERNAME")
    proxy_password = os.getenv("PROXY_PASSWORD")
    proxy = f"{proxy_username}:{proxy_password}@gate.nodemaven.com:8080"

    driver = Driver(uc=True)
    login(driver, LOGIN_URL)
    time.sleep(random.uniform(5, 10))
    for page in range(142, 1305):
        salary_url = f"{BASE_URL}/Salaries/india-lead-data-scientist-salary-SRCH_IL.0,5_KO6,25_IP{page}.htm"
        get_salary_data(driver, salary_url, RUN_ID, page, DATA_DIR)
    driver.quit()
