import os
import time
import logging
import re
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from cryptography.fernet import Fernet
from selenium import webdriver

# Key files must be deleted to make changes to usernames/passwords
# This code is not very clean but it works so im not interested in making any changes.
# There is an argument that can be commented on line 104 to make the browsers visible for troubleshooting

# logging config
logging.basicConfig(filename='script_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# get domain from user
domainfull = (input("Enter the domain to be blocked: "))


def extract_email(data):
    # Use regex to find email within <>
    email_match = re.search(r'<(.*?)>', data)
    if email_match:
        return email_match.group(1)  # Return the email found inside <>
    else:
        return None  # If no email is found


# filtering email out
domain = extract_email(domainfull)
if domain:
    print(f"Extracted email: {domain}")
else:
    print("No email found")
    sys.exit(1)

# Get usernames and password


def generate_key():
    """
    Generates a key and saves it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    return key


def load_key():
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()


def encrypt_message(message, key):
    """
    Encrypts a message
    """
    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message, key):
    """
    Decrypts an encrypted message
    """
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return decrypted_message.decode()


def save_credentials(credentials, key):
    """
    Encrypts and saves the credentials to a file
    """
    with open("credentials.enc", "wb") as file:
        for username, password in credentials.items():
            encrypted_username = encrypt_message(username, key)
            encrypted_password = encrypt_message(password, key)
            file.write(encrypted_username + b"\n" + encrypted_password + b"\n")


def load_credentials(key):
    """
    Load, decrypt and return credentials
    """
    credentials = {}
    with open("credentials.enc", "rb") as file:
        lines = file.read().split(b"\n")
        for i in range(0, len(lines)-1, 2):
            encrypted_username = lines[i]
            encrypted_password = lines[i+1]
            username = decrypt_message(encrypted_username, key)
            password = decrypt_message(encrypted_password, key)
            credentials[username] = password
    return credentials


def main():
    if not os.path.exists("secret.key"):
        key = generate_key()
    else:
        key = load_key()

    if not os.path.exists("credentials.enc"):
        credentials = {}
        while True:
            username = input(
                "Enter your username (or type 'done' to finish): ")
            if username.lower() == 'done':
                break
            password = input("Enter your password: ")
            credentials[username] = password
        save_credentials(credentials, key)
    else:
        credentials = load_credentials(key)
        for username, password in credentials.items():
            launch_browser({username: password})


url = "https://us2.proofpointessentials.com/app/login.php"


def launch_browser(credentials):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get("https://us2.proofpointessentials.com/app/login.php")

    try:
        wait = WebDriverWait(driver, 2)
        # Send Username
        username_field = wait.until(
            EC.visibility_of_element_located((By.ID, "login-email-field")))
        for username, password in credentials.items():
            username_field.send_keys(username)

            # Click the Login button after entering the username
            login_button = wait.until(EC.element_to_be_clickable(
                (By.ID, "login-username-submit-btn")))
            login_button.click()

            # Wait for the password field to be visible
            password_field = wait.until(
                EC.visibility_of_element_located((By.ID, "login-password-field")))
            password_field.send_keys(password)

            # Click the Login button after entering the password
            login_button = wait.until(EC.element_to_be_clickable(
                (By.ID, "login-password-submit-btn")))
            login_button.click()

            # Click on the email button
            first_element = wait.until(
                EC.element_to_be_clickable((By.ID, "menu-email")))
            first_element.click()

            # Click on the sender lists button
            second_element = wait.until(
                EC.element_to_be_clickable((By.ID, "nav_sender-lists")))
            second_element.click()

            # Interact with the textarea
            textarea = wait.until(
                EC.visibility_of_element_located((By.ID, "blocklist")))
            textarea.click()  # Click to set focus on the window
            textarea.send_keys(Keys.RETURN)  # Send a return keystroke

            # Input the data
            textarea.send_keys(domain)

            # Click on the save button
            second_element = wait.until(
                EC.element_to_be_clickable((By.ID, "form-save-btn")))
            second_element.click()

            logging.info(f"Domain '{domain}' at blocked successfully")

    except TimeoutException as e:
        logging.error(f"Timeout error occurred: {e}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Add a delay
        time.sleep(5)
        driver.quit()

    return driver


credentials = {}  # Define the "credentials" variable

browsers = []

try:
    if __name__ == "__main__":
        main()

    # required for loop i believe
    browsers = [launch_browser(credentials)]
finally:
    # Close the browsers
    for browser in browsers:
        browser.quit()
