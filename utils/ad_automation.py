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
PARTIAL_TITLE = os.environ.get("AD_PARTIAL_TITLE")  # Example
# --- End of Configuration ---

if not USERNAME or not PASSWORD or not PARTIAL_TITLE:# check if password and username are set
    raise ValueError("AD_USERNAME and AD_PASSWORD and PARTIAL_TITLE environment variables must be set.")

def get_most_recent_ad_link(driver, partial_title):
    """Finds and returns the URL of the most recent ad (first row in table) using XPath."""
    try:
        # 1. Wait for the table
        table_locator = (By.XPATH, "//table")  # find the first table in the webpage
        table_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(table_locator)
        )
        if table_element:
            print("Table found.")

        # 2. Find the *first* row in the table using XPath
        # first_row_locator = (By.XPATH, "//table/tbody/tr[1]")  # Or a more specific locator
        #  #fboardlist > div > table > tbody > tr:nth-child(1)
        first_row_locator = (By.CSS_SELECTOR, "tr:first-child")

        first_row = WebDriverWait(table_element, 10).until(  # Note: Use table_element, not driver
        EC.presence_of_element_located(first_row_locator))
        if first_row:
            print("First row found.")

        # 3. Find the link within that row using XPath
        
        title_link_locator = (By.XPATH, "//div[@class='tbl_head01 tbl_wrap']/table/tbody/tr[1]//td[@class='td_subject']/div[@class='bo_tit']/a")
        title_link = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(title_link_locator)
        )
        if title_link:
            print("title link found")
            print(title_link.text)

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

    """handel clikign the reupload button"""
    try:
        # Re-locate the button RIGHT BEFORE clicking
        
        reupload_button_locator = (By.XPATH, "//a[contains(normalize-space(.), '다시올리기')]")

        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(reupload_button_locator) # used clikable instead of presence_of_element_located since it can waint tuill the button is clickable
        )  
        print("Re-upload button found.")

        button.click()
        print("Clicked the 'Re-upload' button.")


        
    except TimeoutException:
        print("Timed out waiting for the re-upload button.")
        return "button_not_found"  # Specific return value for button not found
    except NoSuchElementException:
        print("Re-upload button element could not be found (unexpected).")
        return "button_not_found"
    except Exception as e:
        print(f"An unexpected error occurred while finding/clicking button: {e}")
        return "unexpected_error"
    

    """Handle the alert that appears after clicking the button."""
    try:    
        print("Waiting for the alert...")
        webdriver(driver, 10).until(EC.alert_is_present())  # Wait for the alert
        alert = driver.switch_to.alert  # Switch to the alert
        print(f"Alert text: {alert.text}")  
        alert.accept()  # Click "OK" 확인 버튼
        print("Accepted the alert.")
        return "button_clicked"  # Return a success value
    
    except TimeoutException:
        print("Timed out waiting for the alert.")
        return "alert_not_found"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return  "unexpected_error"


def reupload_ad():
    """Logs in to 04uk.com and re-uploads the advertisement."""
    try:
        # Use webdriver_manager to automatically download and manage ChromeDriver
        service = ChromeService(executable_path=ChromeDriverManager().install())# does this mean we down loead evrey time? 
        driver = webdriver.Chrome(service=service) #what is service here? 

        driver.get("http://04uk.com/bbs/myarticles.php")  # go to my article page 

        """Login to the website"""
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mb_id"))
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "mb_password"))
        )

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)# press enter 

        """Find the most recent ad and navigate to its page"""
        ad_url = get_most_recent_ad_link(driver, PARTIAL_TITLE)  # Example
        if not ad_url:
            print("Ad not found or does not match the partial title.")
            return
        
        print(f"Most recent ad URL: {ad_url}")
        driver.get(ad_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #waites untlle pages if fully loaded
        print("Successfully navigated to the ad page.")

        result = click_reupload_button(driver)
        if result == "button_clicked":  
            print("Re-upload process completed successfully!")
        elif result == "button_not_found":
            print("Re-upload button not found.")
        elif result == "alert_not_found":
            print("Re-upload button clicked, but no alert appeared.")
        elif result == "unexpected_error":
            print("An unexpected error occurred during re-upload.")
        
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
