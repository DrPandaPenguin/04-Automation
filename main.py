# main.py
import schedule
import time
from utils.ad_automation import reupload_ad  # Import the function


def main():
    """Main function to schedule and run the ad re-upload."""

    # Schedule the task (example: every day at 10:30 AM)
    reupload_ad() 
    # schedule.every().day.at("10:30").do(reupload_ad)
    # schedule.every().tuesday.at("13:15").do(reupload_ad) # Another example

    # Run the scheduler in a loop
    return
    # while True: #
    #     schedule.run_pending() 
    #     time.sleep(60)  # Check every minute 


if __name__ == "__main__":
    main()