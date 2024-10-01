import requests
import time
import schedule
import logging
from datetime import datetime

# List of websites to monitor
URLS = [
    'https://www.google.com',    # Example of an online website
    'https://www.github.com',    # Another online website
    'https://www.nonexistentwebsite123.com',  # Example of an offline website
]

# Setup logging configuration
logging.basicConfig(filename='website_status.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Function to check the status of each website
def check_website_status():
    print(f"\nChecking websites at {datetime.now()}")
    for url in URLS:
        try:
            # Sending an HTTP request to the website
            response = requests.get(url, timeout=10)
            
            # If the response status code is 200, the website is online
            if response.status_code == 200:
                print(f'{url} is ONLINE.')
                logging.info(f'{url} is ONLINE.')
            else:
                print(f'{url} is OFFLINE. Status code: {response.status_code}')
                logging.warning(f'{url} is OFFLINE. Status code: {response.status_code}')
        
        # Handling errors if the website is not reachable
        except requests.exceptions.RequestException:
            print(f'{url} is OFFLINE or not reachable.')
            logging.error(f'{url} is OFFLINE or not reachable.')

# Scheduling function to check websites every minute
def start_scheduler(max_checks=5):
    check_count = 0  # Counter to keep track of how many checks have been made
    schedule.every(1).minutes.do(check_website_status)

    print("Starting website checker...")
    logging.info("Started website checker")

    while check_count < max_checks:
        schedule.run_pending()
        time.sleep(1)  # Wait for 1 second before checking again
        # Increase the check count after each minute
        if schedule.idle_seconds() <= 60:
            check_count += 1

    print(f"Completed {max_checks} checks. Exiting the program.")
    logging.info(f"Completed {max_checks} checks. Exiting the program.")

if __name__ == '__main__':
    check_frequency_minutes = 1
    check_website_status()  # Initial check before the scheduler starts
    start_scheduler(max_checks=5)  # Run the checker 5 times (5 minutes)
