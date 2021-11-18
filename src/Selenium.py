from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging


class InstagramSelenium:

    def __init__(self, logger: logging.Logger, headless):
        self.logger = logger
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=chrome_options)

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
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/nav/div[2]/div/div/div[1]/a/div/div"))
            )
            self.driver.get(url)
            return True
        except TimeoutException as e:
            self.logger.error(f"Login failed")
            return False
        except Exception as e:
            self.logger.error(f"Unable to login due to {e}")
            return False

    def visitProfilePage(self, username):
        return NotImplemented

    def visitUserStoryPage(self, username) -> bool:
        self.logger.info(f"Visiting {username} story")

        try:
            self.driver.get(
                f"https://www.instagram.com/stories/{username}/")

            WebDriverWait(self.driver, 5).until(
                lambda d: d.find_element_by_xpath(
                    "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/button")).click()
            return True
        except TimeoutException as e:
            self.logger.error("No existing story to download")
            return False
        except Exception as e:
            self.logger.error(f"Unable to view story due to {e}")
            return False

    def stillInStory(self) -> bool:
        try:
            self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/section/div/button[2]")
            if self.driver.current_url == "https://www.instagram.com/":
                return False
            return True
        except NoSuchElementException:
            return False

    def nextStory(self):
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/button[2]").click()

    def getStoryImageLink(self) -> str:
        image = self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/img")
        value = image.get_attribute("srcset")
        value = value.split(',')
        return value[0]

    def getStoryVideoLink(self) -> str:
        try:
            video = self.driver.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/video/source")
            video_value = video.get_attribute("src")
            return video_value
        except Exception as e:
            return ""

    def closeDriver(self):
        self.driver.close()
