import random
import string
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tempmail import EMail

def generate_temp_email():
    email = EMail()  # Create a new temporary email address
    return email.address, email.username

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
    chrome_options.add_argument('--enable-unsafe-swiftshader')  # Enable unsafe swiftshader
    # Uncomment below if you want headless mode
    # chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    return driver


def check_inbox(email):
    inbox = email.get_inbox()  # Get all messages in the inbox
    return inbox[-1] if inbox else None  # Return the latest message or None

def process_account(driver, join_link):
    email, username = generate_temp_email()
    
    try:
        driver.get(join_link)
        time.sleep(2)

        email_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.send_keys(email)

        password_field = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.send_keys("SecurePassword123")  # Use a secure password here

        submit_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "submitButton"))
        )
        submit_button.click()

        print(f"Account created successfully: {email}")

        # Wait for a few seconds to allow the email to arrive
        time.sleep(10)

        # Check inbox for verification code
        message = check_inbox(email)
        if message:
            print(f"Verification code received: {message.body}")  # Adjust based on actual message structure
            
            # Here you would need to enter the verification code in the appropriate field.
            # Example:
            # verification_field.send_keys(verification_code)
            # confirm_button.click()
        
        with open('registered_emails.txt', 'a') as f:
            f.write(f"{email}:SecurePassword123\n")
        
        return True

    except Exception as e:
        print(f"Error processing account {email}: {str(e)}")
        return False

def main():
    join_link = "https://www.1024terabox.com/referral/4401045737659"  # Updated join link
    for _ in range(200):
        driver = init_driver()
        try:
            process_account(driver, join_link)
        finally:
            driver.quit()
            print("Waiting for 5 minutes before next registration...")
            time.sleep(300)

if __name__ == "__main__":
    main()
