import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(span, 'GODKÄNN')]")))
        accept_button.click()
    except Exception:
        pass

def send_to_google_sheets(name):
    url = 'https://script.google.com/macros/s/AKfycbxCZGHPvOhV4xshtmU2Z0f7WNSXkCS-lYEmWIoGp8WDkMD-pmbvVJMz6KdSNf36uw1_uQ/exec'
    headers = {'Content-Type': 'application/json'}
    data = {'type': 'Allabolag', 'name': name}
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            print("Data sent successfully to Google Sheets.")
        else:
            print(f"Failed to send data: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error sending data to Google Sheets: {e}")

def scrape_allabolag_se():
    chrome_options = Options()
    service = Service(executable_path='/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    page = 1
    previous_company_names = set()

    while True:
        url = f"https://www.allabolag.se/bransch/bokutgivning/3/376?page={page}"
        driver.get(url)
        
        if page == 1:
            accept_cookies(driver)
        
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h2.search-results__item__title")))
            company_elements = driver.find_elements(By.CSS_SELECTOR, "h2.search-results__item__title")

            current_page_company_names = set([element.text for element in company_elements])
            
            if not current_page_company_names or current_page_company_names.issubset(previous_company_names):
                break

            for company_name in current_page_company_names:
                send_to_google_sheets(company_name)

            previous_company_names.update(current_page_company_names)

        except Exception:
            break

        page += 1

    driver.quit()

if __name__ == "__main__":
    scrape_allabolag_se()
