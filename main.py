import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import schedule

# --- Configuration (Replace with your actual values) ---
USERNAME = "your_username"
PASSWORD = "your_password"
AD_URL = "https://www.04uk.com/your_ad_page"  # URL of the page with the re-upload button
REUPLOAD_BUTTON_XPATH = "//button[contains(text(), 'Reupload')]"  # Example XPath (VERY IMPORTANT - see below)
# Or, if there's an ID:  REUPLOAD_BUTTON_XPATH = "//*[@id='reuploadButtonId']"
# Or, a CSS selector: REUPLOAD_BUTTON_XPATH = "button.reupload-button"
BROWSER_EXECUTABLE_PATH = "/path/to/your/chromedriver"  # Or geckodriver, etc.

# --- Functions ---
def reupload_ad():
    """Logs in to 04uk.com and re-uploads the advertisement."""
    try:
        # 1. Initialize WebDriver
        driver = webdriver.Chrome(executable_path=BROWSER_EXECUTABLE_PATH)
        driver.get("https://www.04uk.com/login") # Go to login page.  Change if the URL is different.

        # 2. Login
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username")) # Or ID, or other locator.
        )
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        username_field.send_keys(USERNAME)
        password_field.send_keys(PASSWORD)
        password_field.send_keys(Keys.RETURN)  # Submit the form (often works)
        # OR, find and click the login button:
        # login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        # login_button.click()

        # 3. Wait for Login to Complete (and potentially handle 2FA)
        #    Very important:  The website might redirect you, or have a loading spinner.
        #    Wait for an element that *only* appears after successful login.
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'My Account')]")) #Example
            ) # Wait for "My Account" link (or similar)
        except TimeoutException:
            print("Login failed or took too long.")
            driver.quit()
            return  # Exit the function if login fails

        # 4. Navigate to the Ad Page
        driver.get(AD_URL)

        # 5. Find and Click the Re-upload Button
        try:
            reupload_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, REUPLOAD_BUTTON_XPATH))
            )
            reupload_button.click()

             # 6. (Optional) Confirmation
            #    Look for a success message or other indicator that the re-upload worked.
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Ad re-uploaded successfully')]")) # Example
                )
                print("Ad re-uploaded successfully!")
            except TimeoutException:
                print("Confirmation message not found, but re-upload might have worked.")

        except NoSuchElementException:
            print("Re-upload button not found.  Check the XPath or other locator.")
        except TimeoutException:
            print("Re-upload button didn't appear within the timeout.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 7. Close the Browser
        if 'driver' in locals():  # Only quit if the driver was initialized
            driver.quit()

# --- Scheduling (Using the `schedule` library) ---
# schedule.every().day.at("10:30").do(reupload_ad)  # Run every day at 10:30 AM
schedule.every().tuesday.at("13:15").do(reupload_ad) # Example: Every Tuesday at 1:15 PM
# schedule.every(1).minutes.do(reupload_ad) # for testing!  Don't do this on the live site.

while True:
    schedule.run_pending()
    time.sleep(60)  # Check for scheduled tasks every minute