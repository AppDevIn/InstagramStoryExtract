import pdb

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from webdriver_manager.utils import ChromeType

import src.model.constants as const


from src.Exception.CustomException import InstagramException, LoginException
from src.model.DriverModeEnum import DriverMode


class BaseBot(webdriver.Remote):
    def __init__(self, headless, path=None, mode=DriverMode.CHROMEDRIVERMANAGER):
        self.dead = False
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        if DriverMode.CHROME.value == mode:
            super(BaseBot, self).__init__(command_executor="http://localhost:4444/wd/hub", options=chrome_options)
        else:
            super(BaseBot, self).__init__(command_executor="http://localhost:4444/wd/hub"
                                          , options=chrome_options)
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
        self.dead = True
        self.quit()

    def login(self, username, password, logger, wait_time=5):
        try:
            logger.info("Opening the landing page")
            self.landOnPage()
            self.waitTillLoginPageLoaded(wait_time)
            logger.info("The page has loaded")
            self.loginIntoInstagram(username, password)
            logger.info("Attempting with the credentials given in config.yaml")
            logger.info(f"Login with username {username}")
            self.waitTillInstagramLogoDetected(wait_time)
            logger.info("Login was successful")
        except InstagramException as e:
            raise LoginException(e.message, e.default_message)
        except Exception as e:
            raise LoginException(f"Unknown exception: {str(e)}", e)
