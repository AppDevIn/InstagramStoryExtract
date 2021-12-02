from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException
from src.model.ListOfPostModel import ListOfPost
from src.model.post import Media


class PostBot(BaseBot):
    def __init__(self, headless):
        super(PostBot, self).__init__(headless)

    def hasPost(self, timeout) -> bool:
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".eLAPa"))
            )
            return True
        except Exception as e:
            return False

    def hasNextButton(self, timeout) -> bool:
        try:
            WebDriverWait(self, timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".l8mY4 .wpO6b"))
            )
            return True
        except Exception as e:
            return False

    def hasVideo(self):
        self.implicitly_wait(1)
        try:
            self.find_element_by_css_selector(".qF0y9 .tWeCl")
            return True
        except Exception:
            return False
        finally:
            self.implicitly_wait(5)

    def hasImg(self):
        self.implicitly_wait(1)
        try:
            self.find_element_by_css_selector(".qF0y9 .FFVAD")
            return True
        except Exception:
            return False
        finally:
            self.implicitly_wait(5)

    def closePost(self):
        self.find_element_by_css_selector("div._2dDPU > div.qF0y9 > button").click()

    def getPosts(self, callback) -> ListOfPost:
        self.find_elements_by_css_selector(".eLAPa")[0].click()
        posts = ListOfPost()
        while True:
            video = []
            img = []
            if self.hasImg():
                img = list(map(lambda x: Media(x.get_attribute("src")), self.find_elements_by_css_selector(".qF0y9 .FFVAD")))
            if self.hasVideo():
                video = list(map(lambda x: Media(x.get_attribute("src"), True), self.find_elements_by_css_selector(".qF0y9 .tWeCl")))
            img += video
            caption = self.find_element_by_css_selector(".ZyFrc .C4VMK > span").get_attribute("innerHTML")
            time = self.find_element_by_css_selector("._1o9PC").get_attribute("datetime")[:-5]
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            posts.add(img, time, caption)
            callback(posts)
            if self.hasNextButton(2) is False:
                break
            self.find_element_by_css_selector(".l8mY4 .wpO6b").click()
        self.closePost()
        return posts
