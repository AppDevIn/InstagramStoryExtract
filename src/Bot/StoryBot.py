import pdb
import time
from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException, NoUserStoryException
from src.model.DriverModeEnum import DriverMode


class StoryBot(BaseBot):

    def __init__(self, headless, path=None, mode=DriverMode.CHROMEDRIVERMANAGER):
        super(StoryBot, self).__init__(headless, path=path, mode=mode)

    def __int__(self, base: BaseBot):
        super(base)
        return None

    def landOnUserStory(self, profile_name):
        self.get(f"{const.BASE_URL}/stories/{profile_name}/")

    def clickOnConfirmationToView(self):
        try:
            self.find_element_by_css_selector(
                "section > div.qF0y9 > div > section > div > div.qF0y9.Igw0E.IwRSH.eGOV_._4EzTm.NUiEW > div div.qF0y9 > button").click()
        except Exception as e:
            raise NoUserStoryException("No existing user story", e)

    def stillInStory(self) -> bool:
        try:
            self.find_element_by_css_selector(
                "button.FhutL")
            if self.current_url == "https://www.instagram.com/":
                return False
            return True
        except NoSuchElementException:
            return False

    def next(self):
        try:
            self.find_element_by_css_selector(
                "button.FhutL").click()
        except Exception as e:
            raise InstagramException("Next button failed to be clicked", e)

    def getTimeOfStory(self) -> datetime:
        time = self.find_element_by_css_selector("time")
        time_str = time.get_attribute("datetime")[:-5]
        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

    def getImageLink(self) -> str:
        image = self.find_element_by_css_selector("img.y-yJ5")
        value = image.get_attribute("srcset")
        value = value.split(',')
        return value[0]

    def getVideoLink(self) -> str:
        try:
            video = self.find_element_by_css_selector("video source")
            video_value = video.get_attribute("src")
            return video_value
        except Exception as e:
            raise InstagramException("Unable to get video link", str(e))

    def isVideo(self) -> bool:
        try:
            self.find_element_by_css_selector("video source")
            return True
        except Exception as e:
            return False

    def takeScreenshot(self, css: str, path):
        time.sleep(3)
        element = self.find_element_by_css_selector(css)
        element.screenshot(path)




