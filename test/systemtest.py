import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
import time
from multiprocessing import Process

import os


def start_flask_app():
    os.system("flask run")

class SystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Process(target=start_flask_app)
        cls.server.start()
        time.sleep(2)

        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.base_url = "http://127.0.0.1:5000"

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.terminate()

    def test_register_and_login(self):
        self.driver.get(f"{self.base_url}/login")

        self.driver.find_element(By.LINK_TEXT, "Register here").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "username").send_keys("testuser123")
        self.driver.find_element(By.ID, "email").send_keys("testuser123@example.com")
        self.driver.find_element(By.ID, "password").send_keys("Password123!")
        self.driver.find_element(By.ID, "confirm_password").send_keys("Password123!")
        self.driver.find_element(By.CLASS_NAME, "btn-primary").click()
        time.sleep(2)

        self.assertIn("login", self.driver.current_url)

        self.driver.find_element(By.ID, "username").send_keys("testuser123")
        self.driver.find_element(By.ID, "password").send_keys("Password123!")
        self.driver.find_element(By.CLASS_NAME, "btn-primary").click()
        time.sleep(3)

        if "accounts.spotify.com" in self.driver.current_url:
            try:
                
                username_input = self.driver.find_element(By.ID, "login-username")
                username_input.clear()
                username_input.send_keys("thipad123@outlook.com")

                password_input = self.driver.find_element(By.ID, "login-password")
                password_input.clear()
                password_input.send_keys("SpotAccount$1")

                self.driver.find_element(By.ID, "login-button").click()
                time.sleep(4)

                try:
                    agree_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='auth-accept']")
                    agree_button.click()
                    time.sleep(4)
                except NoSuchElementException:
                    pass  # Already authorized

            except NoSuchElementException:
                pass  # Already logged in on Spotify, can account for test being run multiple times.

        
        time.sleep(2)
        if "/home" in self.driver.current_url:
           
            self.driver.get(f"{self.base_url}/scores")
    

    def test_score_page_with_the_weeknd(self):
        self.driver.get(f"{self.base_url}/scores")

        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, "search-bar-input"))
        )

        
        search_input = self.driver.find_element(By.ID, "search-bar-input")
        search_input.clear()
        search_input.send_keys("the weeknd")
        search_input.send_keys(Keys.ENTER)
        time.sleep(5)

        
        score_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "item-score-input"))
        )

        score_input.click()

        
        score_input.clear()
        score_input.send_keys("9")
        score_input.send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            print(f"Alert text: {alert.text}")
            alert.accept()
        except:
            print("No alert appeared — maybe score already existed")

        if "/scores" in self.driver.current_url:
            self.driver.get(f"{self.base_url}/profile")


    def test_home_page_access(self):
        self.driver.get(f"{self.base_url}/")
        self.assertIn("Rankd", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
