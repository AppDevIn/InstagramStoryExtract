from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException


class HighlightBot(BaseBot):
    def __init__(self, headless):
        super(HighlightBot, self).__init__(headless)

    def hasHighlight(self, timeout) -> bool:
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/main/div/div[1]/div/div/div/ul/li[3]"))
            )
            return True
        except Exception as e:
            return False

    def getName(self):
        return WebDriverWait(self, 10).until(
            lambda d: d.find_element_by_css_selector(
                ".FPmhX")).get_attribute("innerHTML")

    def stillInHighlight(self, profile_name) -> bool:
        try:
            if self.current_url == f"https://www.instagram.com/{profile_name}/":
                return False
            return True
        except NoSuchElementException:
            return False

    def getTimeOfHighlight(self) -> datetime:
        time = self.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/div[5]/section/div/header/div[2]/div[1]/div/div/div/time"
        )
        time_str = time.get_attribute("datetime")[:-5]
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

    def getImageLink(self) -> str:
        image = self.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/div[5]/section/div/div[1]/div/div/img")
        value = image.get_attribute("srcset")
        value = value.split(',')
        return value[0]

    def getVideoLink(self) -> str:
        try:
            video = self.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/div[5]/section/div/div[1]/div/div/video/source")
            video_value = video.get_attribute("src")
            return video_value
        except Exception as e:
            raise InstagramException("Unable to get video link", str(e))

    def isVideo(self) -> bool:
        try:
            self.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/div[5]/section/div/div[1]/div/div/video/source")
            return True
        except Exception as e:
            return False

    def next(self):
        self.find_element_by_css_selector(".FhutL").click()

    def clickOnHighlight(self):
        self.find_elements_by_css_selector(
            "._3D7yK")[0].click()

    def landOnHighlightById(self, identification):
        self.get(
            f"{const.BASE_URL}/stories/highlights/{identification}/")
