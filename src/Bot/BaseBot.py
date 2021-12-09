import pathlib
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

from webdriver_manager.utils import ChromeType

import src.model.constants as const

import pdb

from src.Exception.CustomException import InstagramException
from src.model.DriverModeEnum import DriverMode


class BaseBot(webdriver.Chrome):
    def __init__(self, headless, path=None, mode=DriverMode.CHROMEDRIVERMANAGER):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        if DriverMode.CHROME.value == mode:
            super(BaseBot, self).__init__(path, options=chrome_options)
        else:
            super(BaseBot, self).__init__(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(),
                                          options=chrome_options)
        self.implicitly_wait(5)

    def landOnPage(self):
        try:
            self.get(const.BASE_URL)
        except Exception as e:
            raise InstagramException("Failed to land on the login page", e)

    def waitTillLoginPageLoaded(self, timeout: int):
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.NAME, "username"))
            )
        except Exception as e:
            raise InstagramException("Error occurred waiting for login page to load", e)

    def loginIntoInstagram(self, username, password):
        try:
            username_ele = self.find_element_by_name("username")
            password_ele = self.find_element_by_name("password")
            login_btn = self.find_element_by_css_selector("#loginForm button.L3NKy")

            username_ele.send_keys(username)
            password_ele.send_keys(password)

            login_btn.click()
        except Exception as e:
            raise InstagramException("Error occurred when trying to login ", e)

    def waitTillInstagramLogoDetected(self, timeout):
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div._8MQSO a > div > div"))
            )
        except Exception as e:
            raise InstagramException("Unable to detect logo", str(e))

    def landProfilePage(self, profile_name):
        try:
            self.get(
                f"https://www.instagram.com/{profile_name}/")
        except Exception as e:
            raise InstagramException(f"Unable to access {profile_name}'s profile", str(e))

    def closeDriver(self):
        self.close()