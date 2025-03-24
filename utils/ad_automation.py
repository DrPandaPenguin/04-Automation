# utils/ad_automation.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
from selenium.webdriver.chrome.service import Service as ChromeService  # Import Service
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager
import os  # Import os for environment variables
from dotenv import load_dotenv # load_dotenv as arry or dictionary? 



# --- Configuration (Using environment variables) ---
load_dotenv() # Load environment variables from .env file
USERNAME = os.environ.get("AD_USERNAME")
PASSWORD = os.environ.get("AD_PASSWORD")
AD_URL = os.environ.get("AD_URL", "https://www.04uk.com/your_ad_page") #Default value
REUPLOAD_BUTTON_XPATH = "//button[contains(text(), 'Reupload')]"  # Example

if not USERNAME or not PASSWORD:
    raise ValueError("AD_USERNAME and AD_PASSWORD environment variables must be set.")

def get_most_recent_ad_link(driver, partial_title):
    """Finds and returns the URL of the most recent ad (first row in table) using XPath."""
    try:
        # 1. Wait for the table
        table_locator = (By.XPATH, "//table")  # Or a more specific locator
        table_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(table_locator)
        )
        if table_element:
            print("Table found.")

        # 2. Find the *first* row in the table using XPath
        first_row = table_element.find_element(By.CSS_SELECTOR, "tr:first-child")
        if first_row:
            print("First row found.")

        # 3. Find the link within that row using XPath
        title_link_locator = (By.XPATH, "//div[@class='tbl_head01 tbl_wrap']/table/tbody/tr[1]//td[@class='td_subject']/div[@class='bo_tit']/a")
        title_link = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(title_link_locator)
        )
        if title_link:
            print("title link found")
            print(title_link)

        # 4. Check if the link's text contains the partial title
        if partial_title in title_link.text:
             # 5. Get the href attribute (the URL)
            link_url = title_link.get_attribute("href")
            return link_url
        else:
            print(f"First row does not contain title '{partial_title}'")
            return None

    except TimeoutException:
        print("Timed out waiting for the table or row.")
        return None
    except NoSuchElementException:
        print("Table, row, or link not found.")
        return None
    except Exception as e:  # Catch any other exceptions
        print(f"An unexpected error occurred: {e}")
        return None
    
def click_reupload_button(driver):
    """Clicks the '다시 올리기' (Re-upload) button, re-locating it immediately before clicking."""
    try:
        # Re-locate the button RIGHT BEFORE clicking
        
        reupload_button_locator = (By.XPATH, "//a[contains(normalize-space(.), '다시올리기')]")

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(reupload_button_locator)
        ).click()  # Find and click in one line!

        print("Clicked the 'Re-upload' button.")
        print("Waiting for the alert...")
        time.sleep(1)
        try:
            alert = driver.switch_to.alert()  # Switch to the alert
            print(f"Alert text: {alert.text}")  # Good for debugging
            alert.accept()  # Click "OK"

            print("Accepted the alert.")
            return True
        except NoAlertPresentException:
            print("No alert was present.") # Handle no alert.
            return False

    except TimeoutException:
        print("Timed out waiting for the 'Re-upload' button.")
        return False
    except NoSuchElementException:
        print("'Re-upload' button not found.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def reupload_ad():
    """Logs in to 04uk.com and re-uploads the advertisement."""
    try:
        # Use webdriver_manager to automatically download and manage ChromeDriver
        service = ChromeService(executable_path=ChromeDriverManager().install())# does this mean we down loead evrey time? 
        driver = webdriver.Chrome(service=service) #what is service here? 

        driver.get("http://04uk.com/bbs/myarticles.php")  # go to my article page 

        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mb_id"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mb_password"))
        )

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)# press enter 
        partial_title = "GCSE"  # Example

        ad_url = get_most_recent_ad_link(driver, partial_title)  # Example
        if not ad_url:
            print("Ad not found or does not match the partial title.")
            return
        else:
            print(f"Most recent ad URL: {ad_url}")
            driver.get(ad_url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #waites untlle pages if fully loaded
            print("Successfully navigated to the ad page.")

            click_reupload_button(driver)
            print("Re-upload process completed.")
            return


    except NoSuchElementException:
        print("Element not found. Check your locators (XPath, etc.).")
    except TimeoutException:
        print("Timeout waiting for an element to appear. Check your locators and website loading time.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    finally:
        if 'driver' in locals():
            driver.quit()
