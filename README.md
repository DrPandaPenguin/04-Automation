
# 04uk.com Ad Re-upload Bot

This project automates the process of re-uploading advertisements on the 04uk.com website using Python and Selenium.

## Description

This script logs into 04uk.com, navigates to the user's articles page, finds the most recent advertisement based on a partial title match, navigates to that ad's page, clicks the "Re-upload" (다시 올리기) button, and handles the confirmation alert. It uses the `schedule` library to run the task automatically at configured times (currently set to run once immediately for testing). WebDriver management is handled automatically using `webdriver-manager`, and sensitive credentials are managed securely using environment variables via a `.env` file. Logging is implemented to track the bot's progress and errors.

**Tech Stack:**

* Python 3.x
* Selenium
* webdriver-manager (for automatic ChromeDriver handling)
* python-dotenv (for loading environment variables)
* schedule (for task scheduling)
* logging (for application logging)

## Features

* Automated login to 04uk.com.
* Finds the most recent advertisement based on a partial title match in the user's articles list.
* Navigates to the specific advertisement page.
* Locates and clicks the "Re-upload" button.
* Handles the JavaScript confirmation alert after clicking the button.
* Uses `webdriver-manager` for easy and automatic ChromeDriver setup.
* Securely manages credentials using a `.env` file.
* Logs progress and errors using Python's `logging` module.
* Includes a basic structure for scheduled execution using the `schedule` library.

## Prerequisites

* Python 3.8+ installed.
* Google Chrome web browser installed.
* Git installed (for cloning the repository).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/DrPandaPenguin/04-Automation.git](https://github.com/DrPandaPenguin/04-Automation.git)
    cd 04-Automation
    ```
2.  **Create and activate a virtual environment (Recommended):**
    ```bash
    # On macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # On Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to generate `requirements.txt` first using `pip freeze > requirements.txt` in your activated virtual environment after ensuring all needed libraries like `selenium`, `webdriver-manager`, `python-dotenv`, `schedule` are installed.)*

## Configuration

Sensitive information like your username and password should not be hardcoded. This script uses a `.env` file to manage them.

1.  **Copy the example file:**
    ```bash
    cp .env.example .env
    ```
2.  **Edit the `.env` file:** Open the newly created `.env` file in a text editor and replace the placeholder values with your actual 04uk.com credentials and the partial title identifier for your ad.

    ```dotenv
    # .env
    # Credentials for 04uk.com
    AD_USERNAME="YOUR_ACTUAL_USERNAME"
    AD_PASSWORD="YOUR_ACTUAL_PASSWORD"
    AD_PARTIAL_TITLE="PART_OF_YOUR_AD_TITLE_TO_MATCH"
    ```
    **Important:** Ensure the `.env` file is listed in your `.gitignore` file to avoid accidentally committing your credentials to version control.
    ## Configuration

2.  **Edit the `.env` file:** Open the `.env` file with a text editor and replace the placeholder values with your actual information:
    * `AD_USERNAME`: Your username for 04uk.com.
    * `AD_PASSWORD`: Your password for 04uk.com.
    * `AD_PARTIAL_TITLE`: A unique part of the title of the ad you want the script to find and re-upload.

**Example `.env` file:**
```dotenv
AD_USERNAME="my_actual_user"
AD_PASSWORD="my_real_password123"
AD_PARTIAL_TITLE="GCSE, A-level"

## Usage

Make sure your virtual environment is activated. Run the main script from the project's root directory:

```bash
python main.py