import os
import signal
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ustawienia aplikacji
USERNAME = 'reizer'
PASSWORD = 'hyT@LUkzTR3Qa7#8Ea'
LOGIN_URL = "https://emodul.pl/login"

def terminate_chrome_processes():
    """
    Próbuje zakończyć wszystkie procesy Chrome uruchomione przez skrypt.
    To dodatkowe zabezpieczenie, gdyby jakieś procesy pozostały po zamknięciu przeglądarki.
    """
    process_name = "chrome"
    for line in os.popen(f"ps ax | grep {process_name} | grep -v grep"):
        fields = line.split()
        if fields:
            pid = fields[0]
            try:
                os.kill(int(pid), signal.SIGKILL)
                logging.info(f"Terminated process {pid}")
            except Exception as kill_error:
                logging.error(f"Failed to terminate process {pid}: {kill_error}")

def main():
    # Konfiguracja opcji Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Praca w trybie bezgłowym (bez interfejsu)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Inicjalizacja ChromeDriver z wykorzystaniem webdriver_manager
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)

    try:
        logging.info("Navigating to login page...")
        browser.get(LOGIN_URL)

        # Wyszukanie pola dla nazwy użytkownika i wpisanie danych
        username_field = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "/html/body/div/div[1]/div[2]/div/login/div/div[2]/form/input[1]"))
        )
        username_field.send_keys(USERNAME)
        logging.info("Username entered.")

        # Wyszukanie pola dla hasła i wpisanie danych
        password_field = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "/html/body/div/div[1]/div[2]/div/login/div/div[2]/form/input[2]"))
        )
        password_field.send_keys(PASSWORD)
        logging.info("Password entered.")

        # Kliknięcie przycisku logowania
        sign_in_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, 
                "/html/body/div/div[1]/div[2]/div/login/div/div[2]/form/input[3]"))
        )
        sign_in_button.click()
        logging.info("Sign-in button clicked.")

        # Czekanie na pierwszy przycisk fazy i kliknięcie go
        stage_one_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                "/html/body/div/div[1]/div[2]/div/dashboard-tiles/div[2]/div/div[3]/div/div[1]/tile/div/div/div[3]"))
        )
        stage_one_button.click()
        logging.info("First stage button clicked.")

        # Czekanie na drugi przycisk fazy i kliknięcie go
        stage_two_button = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, 
                "/html/body/div/div[1]/div[2]/div/control-menu/div/controls/div/div[1]/div/div[2]/div/button[3]"))
        )
        stage_two_button.click()
        logging.info("Second stage button clicked.")

        logging.info("Done! Toggled firing up/down!")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        browser.quit()
        logging.info("Browser closed.")
        # Zabijanie pozostałych procesów Chrome, jeśli wystąpią
        terminate_chrome_processes()

if __name__ == "__main__":
    main()
