from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import logging


class InstagramSelenium:

    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install())

    def loginToInstagram(self, username, password) -> bool:
        url = "https://www.instagram.com/"
        try:
            self.driver.get(url)
            self.logger.info(f"Opening {url}")
            username_ele = WebDriverWait(self.driver, 30).until(
                lambda d: d.find_element_by_name("username"))

            password_ele = self.driver.find_element_by_name("password")
            login_btn = self.driver.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')
            self.logger.info(f"Logging in to account {username}")

            username_ele.send_keys(username)
            password_ele.send_keys(password)

            login_btn.click()
            wait = WebDriverWait(self.driver, 10)
            self.driver.get(url)
            return True
        except Exception as e:
            self.logger.error(f"Logging failed due to {e}")
            return False

    def visitProfilePage(self, username):
        self.driver.get(
            f"https://www.instagram.com/stories/{username}/")

    def clickInstagramStoryFromUserPage(self):
        WebDriverWait(self.driver, 30).until(
            lambda d: d.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/button")).click()

