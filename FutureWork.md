Potential Improvements / Future Work
Here are some ways this script could be enhanced:

Activate Scheduling:

How: Uncomment the schedule lines and the while True loop in the main() function within main.py.
Running: You will need to keep the python main.py process running constantly in a terminal for the schedule to work. On Linux/macOS, tools like screen, tmux, or nohup python main.py & can run it in the background. On Windows, you might just leave the command prompt open or investigate background process options.
Alternative: For more robust scheduling that doesn't require the Python script to always be running, use your operating system's built-in scheduler:
Windows: Task Scheduler
macOS/Linux: cron
Run Headless (No Visible Browser):

What: Run Chrome in "headless" mode so the browser window doesn't pop up visually. This is faster and essential for running on servers without a graphical interface.
How: Modify the setup_driver function in main.py:
Python

from selenium.webdriver.chrome.options import Options

def setup_driver():
    logger.info("Setting up Chrome WebDriver...")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    # --- Add Options ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu") # Often needed with headless
    options.add_argument("--window-size=1920,1080") # Specify window size
    # --- Pass options to driver ---
    driver = webdriver.Chrome(service=service, options=options)
    logger.info("WebDriver setup complete (headless).")
    return driver
Note: Debugging can be harder without seeing the browser. Ensure your logging is thorough if using headless mode extensively.
Create an Executable File:

What: Package the Python script and its dependencies into a single executable file (.exe on Windows, a standalone executable on macOS/Linux) so it can be run on machines without Python or the specific libraries installed.
How (using PyInstaller):
Install PyInstaller: pip install pyinstaller
Navigate to your project directory in the terminal.
Run the command (basic example): pyinstaller --onefile --windowed main.py
--onefile: Bundles everything into a single executable.
--windowed: (Optional, for Windows) Prevents a console window from appearing when the executable runs. You might omit this if you want to see console output/logs.
Look in the dist folder for your executable.
Challenges: Creating executables for Selenium scripts can sometimes be tricky due to the need to bundle or locate chromedriver. You might need to experiment with PyInstaller's options or hooks. Antivirus software can also sometimes flag these executables. See the PyInstaller Documentation for more details.
