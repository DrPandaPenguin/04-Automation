import schedule
import time
import os  # <<<--- Added import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from dotenv import load_dotenv
from utils.ad_automation import (
    login_to_04uk,
    get_most_recent_ad_link,
    click_reupload_button,
    handle_alert
)

load_dotenv() # Load environment variables from .env file
USERNAME = os.environ.get("AD_USERNAME")
PASSWORD = os.environ.get("AD_PASSWORD")
PARTIAL_TITLE = os.environ.get("AD_PARTIAL_TITLE")
print(f"USERNAME: {USERNAME}")
print(f"PASSWORD: {PASSWORD}")

def setup_driver(): #done!!
    """Sets up the Chrome WebDriver with options."""
    service = ChromeService(executable_path=ChromeDriverManager().install())# does this mean we down loead evrey time? 
    driver = webdriver.Chrome(service=service)
    return driver

def reupload_ad():
    print("Re-uploading ad...")
    driver = None # Initialize driver to None
    try:
        driver = setup_driver()  # Set up the WebDriver
        login_status = login_to_04uk(driver,USERNAME,PASSWORD)  # Log in to the website
        if login_status != "login_success":
            print(f"Login failed with status: {login_status}. Aborting task.")
            return # Stop if login fails


        """Find the most recent ad and navigate to its page"""
        ad_url = get_most_recent_ad_link(driver, PARTIAL_TITLE)  # Example
        if not ad_url:
            print("Ad not found or does not match the partial title.")
            return
        
        print(f"Most recent ad URL: {ad_url}")
        driver.get(ad_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #waites untlle pages if fully loaded
        print("Successfully navigated to the ad page.")

        click_reupload_button(driver)  # Click the re-upload button
        result = handle_alert(driver)  # Handle the alert if it appears

        # Handle the result of the button click
        if result == "button_clicked":
            print("Re-upload process completed successfully!")
        elif result == "button_not_found":
            print("Re-upload button not found.")
        elif result == "alert_not_found":
            print("Re-upload button clicked, but no alert appeared.")
        elif result == "unexpected_error":
            print("An unexpected error occurred during re-upload.")
        
    except Exception as e:
        print(f"An unexpected error occurred during the task: {e}")
    finally:
        if driver:
            print("Closing browser.")
            driver.quit()
        print("Re-upload task finished.")




def main():
    """Main function to schedule and run the ad re-upload."""


    reupload_ad()  

    # schedule.every().day.at("10:30").do(reupload_ad)
    # schedule.every().tuesday.at("13:15").do(reupload_ad) # Another example

    # Run the scheduler in a loop
    # return
    # while True: #
    #     schedule.run_pending() 
    #     time.sleep(60)  # Check every minute 


if __name__ == "__main__":
    main()