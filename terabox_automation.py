import requests
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import time

def generate_temp_email():
    # Alternative Temp-Mail API
    api_url = "https://api.mail.tm/domains"
    try:
        # Get available domains from Mail.tm
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()

        # Extract the first domain from the response
        domain = response.json()["hydra:member"][0]["domain"]

        # Generate a random username
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        # Combine to create an email
        email = f"{username}@{domain}"
        return email, username
    except requests.exceptions.RequestException as e:
        print(f"Error fetching temp email: {e}")
        raise

def process_account(driver, join_link):
    try:
        # Generate temporary email
        email, username = generate_temp_email()

        # Navigate to the join link
        driver.get(join_link)
        
        # Wait for the registration form to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))

        # Fill the registration form
        email_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirmPassword")

        email_field.send_keys(email)
        password_field.send_keys("password123")
        confirm_password_field.send_keys("password123")

        # Submit the form
        submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        submit_button.click()

        # Wait for the account creation confirmation
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Account created')]")))

        print(f"Account created successfully: {email}")
        return True
    except Exception as e:
        print(f"Error processing account: {e}")
        return False

def main():
    # Initialize Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Link to join/register
        join_link = "https://example.com/join"

        # Process the account
        success = process_account(driver, join_link)

        if success:
            print("Account creation completed.")
        else:
            print("Account creation failed.")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
