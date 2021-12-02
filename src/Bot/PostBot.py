from datetime import datetime

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException
from src.model.ListOfPostModel import ListOfPost


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

    def getPosts(self) -> None:
        list_of_posts = self.find_elements_by_css_selector(".eLAPa")
        posts = ListOfPost()
        for e in list_of_posts:
            e.click()
            media = list(map(lambda x: x.get_attribute("src"), self.find_elements_by_css_selector(".qF0y9 .FFVAD")))
            caption = self.find_element_by_css_selector(".ZyFrc .C4VMK > span").get_attribute("innerHTML")
            time = self.find_element_by_css_selector("._1o9PC").get_attribute("datetime")[:-5]
            time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
            posts.add(media, time, caption)
            self.find_element_by_css_selector(".BI4qX > button:nth-child(1)").click()
        return posts







