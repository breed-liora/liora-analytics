import time
import requests
import os
import pandas as pd
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from src.utils.reports.config import USERNAME, PASSWORD, EMA_LOGIN_URL, EMA_FINANCIALS_URL, REPORTS
from dagster import get_dagster_logger

logger = get_dagster_logger()

def wait_for_window(driver, timeout=2):
    time.sleep(round(timeout / 1000))
    wh_now = driver.window_handles
    wh_then = driver.window_handles[:]
    if len(wh_now) > len(wh_then):
        return set(wh_now).difference(set(wh_then)).pop()

def search_and_click_item(driver, search_string):
    def get_specific_item(driver, search_text):
        items = driver.find_elements(By.CSS_SELECTOR, ".lui-list__text")
        for item in items:
            if item.text.strip() == search_text:
                return item
        return None

    try:
        search_input_selector = "#dimensionSortable .cl-custom-search-input"
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, search_input_selector)))

        search_input.clear()
        search_input.send_keys(search_string)

        time.sleep(5)

        item = get_specific_item(driver, search_string)

        if item:
            logger.info(f"'{search_string}' item found. Clicking it now.")
            item.click()
            logger.info("Item clicked successfully.")
            return True
        else:
            logger.error(f"Error: Could not find '{search_string}' item.")
            visible_items = driver.find_elements(By.CSS_SELECTOR, ".lui-list__text")
            logger.info("\nVisible items after search:")
            for visible_item in visible_items:
                logger.info(visible_item.text)
            return False

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return False

def download_report(driver, report_config):
    try:
        driver.get(report_config['url'])
        logger.info(f"Navigated to {report_config['name']} page")

        main_window = driver.current_window_handle
        driver.switch_to.window(main_window)

        menu = WebDriverWait(driver, 60*10).until(EC.presence_of_element_located((By.XPATH, f"//h2[contains(text(), '{report_config['qlik_name']}')]")))
        logger.info(f"'{report_config['qlik_name']}' element found")
        time.sleep(10)

        deletes = driver.find_elements(By.CSS_SELECTOR, ".icon-vtabs-delete")
        for delete_button in deletes:
            wait = WebDriverWait(driver, 10)
            clickable_button = wait.until(EC.element_to_be_clickable(delete_button))
            clickable_button.click()
            time.sleep(10)
        logger.info("Cleared existing dimensions/measures")

        for item in report_config['dimensions'] + report_config['measures']:
            logger.info(f"Adding item: {item}")
            search_and_click_item(driver, item)
        logger.info("All dimensions and measures added")

        time.sleep(10)
        driver.find_element(By.CSS_SELECTOR, ".lui-icon--export").click()
        logger.info("Clicked export button")

        download_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, "Click here to download your data file."))
        ).get_attribute('href')
        logger.info("Got download link")

        selenium_cookies = driver.get_cookies()
        cookies = {cookie['name']: cookie['value'] for cookie in selenium_cookies}

        logger.info("Attempting to download file")
        response = requests.get(download_link, cookies=cookies)
        
        if response.status_code == 200:
            df = pd.read_excel(io.BytesIO(response.content))
            logger.info(f"File downloaded successfully and converted to DataFrame")
            return df
        else:
            logger.error(f"Failed to download file. Status code: {response.status_code}")
            return None

    except Exception as e:
        logger.error(f"An error occurred while downloading {report_config['name']}: {str(e)}")
        return None

def setup_driver():
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1500, 1600)
    return driver

def login(driver):
    driver.get(EMA_LOGIN_URL)
    logger.info("Navigated to EMA login page")
    driver.find_element(By.ID, "username").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "login").click()
    logger.info("Logged into EMA")
    driver.find_element(By.NAME, "redirectToNonPatientLoginPage").click()
    logger.info("Redirected to non-patient login page")
    driver.get(EMA_FINANCIALS_URL)
    logger.info("Navigated to EMA financials page")

def main():
    try:
        driver = setup_driver()
        logger.info("WebDriver initialized")
        
        login(driver)
        
        for report in REPORTS:
            download_report(driver, report)
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        logger.info("WebDriver closed")

if __name__ == "__main__":
    main()
