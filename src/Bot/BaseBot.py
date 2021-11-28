import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import src.model.constants as const

import logging
import pdb

from src.Exception.CustomException import InstagramException
from src.model.UserHighlightModel import UserHighlightModel


class BaseBot(webdriver.Chrome):
    def __init__(self, headless):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        super(BaseBot, self).__init__(ChromeDriverManager().install(), options=chrome_options)
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
            login_btn = self.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')

            username_ele.send_keys(username)
            password_ele.send_keys(password)

            login_btn.click()
        except Exception as e:
            raise InstagramException("Error occurred when trying to login ", e)

    def waitTillInstagramLogoDetected(self, timeout):
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div"))
            )
        except Exception as e:
            raise InstagramException("Unable to detect logo", str(e))

    def closeDriver(self):
        self.close()