# utils/ad_automation.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, NoAlertPresentException
 # Import Service
 # Import ChromeDriverManager





def get_most_recent_ad_link(driver, partial_title):
    """Finds and returns the URL of the most recent ad (first row in table) using XPath."""
    try:
        # 1. Wait for the table
        table_locator = (By.XPATH, "//table")  # find the first table in the webpage
        table_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(table_locator)
        )
        print("Table found.")

        # 2. Find the *first* row in the table using XPath
        # first_row_locator = (By.XPATH, "//table/tbody/tr[1]")  # Or a more specific locator
        #  #fboardlist > div > table > tbody > tr:nth-child(1)
        first_row_locator = (By.CSS_SELECTOR, "tr:first-child") # find the first row in the table using convention 

        first_row = WebDriverWait(table_element, 10).until(  # Note: Use table_element, not driver
        EC.presence_of_element_located(first_row_locator))
        print("First row found.")

        # 3. Find the link within that row using XPath
        
        title_link_locator = (By.CSS_SELECTOR, "td.td_subject div.bo_tit a")
        title_link = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(title_link_locator)
        )
        print("Title link found")
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
    
def click_reupload_button(driver):#done!!


    """Finds and clicks the '다시 올리기' (Re-upload) button.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        "button_clicked_success": If the button was found and clicked.
        "button_not_found": If the button was not found/clickable within the timeout.
        "unexpected_error_clicking": If any other exception occurred during click.
    """
    try:
        button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(normalize-space(.), '다시올리기')]"))
        )
        print("Re-upload button found.")
        button.click()
        print("Clicked the 'Re-upload' button.")
        return "button_clicked_success"

    except TimeoutException:
        print("Timed out waiting for the re-upload button to be clickable.")
        return "button_not_found"
    except NoSuchElementException:
        # Less likely with WebDriverWait, but good to handle
        print("Re-upload button element could not be found in DOM.")
        return "button_not_found"
    except Exception as e:
        print(f"An unexpected error occurred while finding/clicking button: {e}")
        return "unexpected_error_clicking"
    
def handle_alert(driver):
    """Waits for and accepts the confirmation alert after clicking re-upload.

    Args:
        driver: The Selenium WebDriver instance.

    Returns:
        "alert_accepted": If the alert appeared and was accepted.
        "alert_not_found": If the alert did not appear within the timeout.
        "unexpected_error_alert": If any other exception occurred during alert handling.
    """
    try:
        print("Waiting for the alert...")
        # Use WebDriverWait to wait for the alert, remove time.sleep()
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        print(f"Alert appeared. Text: {alert.text}")
        alert.accept()  # Click "OK"
        print("Accepted the alert.")
        return "alert_accepted"

    except TimeoutException:
        print("Timed out waiting for the alert to appear.")
        return "alert_not_found"
    except Exception as e:
        print(f"An unexpected error occurred while handling alert: {e}")
        return "unexpected_error_alert"

def login_to_04uk(driver,username, password):
        print(username, password)
        try:
                # 1. Go to the login page
            
            driver.get("http://04uk.com/bbs/myarticles.php")  # go to my article page 

            """Login to the website"""
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mb_id"))
            )
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "mb_password"))
            )

            username_field.send_keys(username)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)# press enter 

            return "login_success" # return success value
        except TimeoutException:
            print("Timed out waiting for the login fields.")
            return "login_failed"   

        


