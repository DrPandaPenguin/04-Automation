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
import logging # 1. Import the logging module


log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# You can change level to logging.DEBUG for more verbose output during development
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    # filename='reupload_bot.log', # Uncomment to log to a file
    # filemode='a'                # 'a' = append, 'w' = overwrite
)

# 2. Set levels for known noisy libraries higher (e.g., WARNING)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
logging.getLogger('webdriver_manager').setLevel(logging.WARNING)
logging.getLogger('selenium.webdriver.common.driver_finder').setLevel(logging.WARNING)
logging.getLogger('WDM').setLevel(logging.WARNING)
logging.getLogger("selenium.webdriver.common.service").setLevel(logging.WARNING)
# Add others here if needed

# Get a logger for this main script
logger = logging.getLogger(__name__)

load_dotenv() # Load environment variables from .env file
USERNAME = os.environ.get("AD_USERNAME")
PASSWORD = os.environ.get("AD_PASSWORD")
PARTIAL_TITLE = os.environ.get("AD_PARTIAL_TITLE")





def setup_driver(): #done!!
    """Sets up the Chrome WebDriver with options."""
    logger.debug("Setting up Chrome WebDriver...")
    service = ChromeService(executable_path=ChromeDriverManager().install())# does this mean we down loead evrey time? 
    driver = webdriver.Chrome(service=service)
    logger.debug("Chrome WebDriver setup complete.")
    return driver

def reupload_ad():
    logger.info("Starting re-upload task...")
    driver = None # Initialize driver to None
    try:
        
        driver = setup_driver()
        # -- login to the website --
        logger.debug("Logging in to the website...")
        login_status = login_to_04uk(driver,USERNAME,PASSWORD)  # Log in to the website
        logger.info(f"Login status: {login_status}")
        if login_status != "login_success":
            logger.error("Login failed. Exiting...")
            return # Stop if login fails


        """Find the most recent ad and navigate to its page"""
        # logger.info("Finding the most recent ad...")
        logger.debug("Finding the most recent ad...")
        ad_url = get_most_recent_ad_link(driver, PARTIAL_TITLE)  # Example
        if not ad_url:
            logger.error("No ad found with the specified title.")
            return
        

        logger.info(f"Most recent ad URL: {ad_url}")
        driver.get(ad_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #waites untlle pages if fully loaded
        logger.debug("Successfully navigated to the ad page.")
        
        # -- Click the re-upload button --
        logger.debug("Clicking the re-upload button...")

        click_status = click_reupload_button(driver) # Renamed for clarity

        # --- Handle Alert (ONLY if button click succeeded) ---
        if click_status == "button_clicked_success":
            logger.info("Button clicked successfully, now handling alert...")
            alert_status = handle_alert(driver) # Call separate alert handler

            # Now evaluate the outcome based on alert handling
            if alert_status == "alert_accepted":
                logger.info("Re-upload process completed successfully!")
            elif alert_status == "alert_not_found":
                logger.warning("Re-upload Warning: Button clicked, but confirmation alert did not appear.")
            else: # Handles "unexpected_error_alert"
                logger.error(f"Re-upload Error: An error occurred while handling the alert: {alert_status}")

        elif click_status == "button_not_found":
            logger.error("Re-upload Failed: Re-upload button not found on the page.")

        else: # Handles "unexpected_error_clicking"
            logger.error(f"Re-upload Failed: An unexpected error occurred while clicking the button: {click_status}")


    except Exception as e:
        logger.error(f"An unexpected error occurred during the task: {e}")
    finally:
        if driver:
            logger.info("Closing browser.")
            driver.quit()
        logger.info("Re-upload task finished.")




def main():
    """Main function to schedule and run the ad re-upload."""


    reupload_ad()  



if __name__ == "__main__":
    main()