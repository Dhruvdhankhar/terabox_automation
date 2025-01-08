import random
import string
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def scrape_temp_email(driver):
    driver.get("https://temp-mail.org/en/")
    email_element = driver.find_element(By.ID, "email")
    temp_email = email_element.get_attribute("value")
    return temp_email

# Initialize WebDriver
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-extensions')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    return driver

# Generate a temporary email address using Temp-Mail API
def generate_temp_email():
    api_url = "https://api.temp-mail.org/request/domains/format/json"
    email_domain = requests.get(api_url).json()[0]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    email = f"{username}@{email_domain}"
    return email, username

# Check inbox for verification email
def fetch_verification_code(username, domain):
    api_url = f"https://api.temp-mail.org/request/mail/id/{username}@{domain}/format/json"
    time.sleep(10)  # Allow time for the email to arrive
    response = requests.get(api_url).json()
    if response:
        # Extract the verification code from the latest email
        return response[-1]['mail_text']
    return None

# Process a single account registration
def process_account(driver, join_link):
    email, username = generate_temp_email()
    domain = email.split('@')[1]  # Extract domain from the email
    
    try:
        # Navigate to the referral website
        driver.get(join_link)
        time.sleep(2)

        # Fill out the signup form
        email_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))  # Adjust ID based on actual site structure
        )
        email_field.send_keys(email)

        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))  # Adjust ID based on actual site structure
        )
        password_field.send_keys("SecurePassword123")  # Use a secure password

        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submitButton"))  # Adjust ID based on actual site structure
        )
        submit_button.click()

        print(f"Account created successfully with email: {email}")

        # Fetch verification code
        verification_code = fetch_verification_code(username, domain)
        if verification_code:
            print(f"Verification code received: {verification_code}")

            # Enter verification code into the form
            verification_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "verificationCode"))  # Adjust ID based on actual site structure
            )
            verification_field.send_keys(verification_code)

            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "confirmButton"))  # Adjust ID based on actual site structure
            )
            confirm_button.click()
            print(f"Account verified for email: {email}")
        else:
            print(f"No verification code received for email: {email}")

        # Save credentials
        with open('registered_emails.txt', 'a') as f:
            f.write(f"{email}:SecurePassword123\n")

        return True

    except Exception as e:
        print(f"Error processing account {email}: {str(e)}")
        return False

# Main function to handle multiple registrations
def main():
    join_link = "https://www.1024terabox.com/referral/4401045737659"  # Referral link
    registrations = 200
    interval = 300  # 5 minutes in seconds

    for i in range(registrations):
        print(f"Starting registration {i + 1}/{registrations}")
        driver = init_driver()
        try:
            success = process_account(driver, join_link)
            if success:
                print(f"Registration {i + 1} completed successfully.")
            else:
                print(f"Registration {i + 1} failed.")
        finally:
            driver.quit()
        if i < registrations - 1:
            print("Waiting for 5 minutes before the next registration...")
            time.sleep(interval)

if __name__ == "__main__":
    main()

