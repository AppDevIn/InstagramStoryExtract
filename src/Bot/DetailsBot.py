import pdb
import time

from selenium import webdriver

from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException
from src.model.UserModel import User


class DetailsBot(BaseBot):
    def __init__(self, path="http://localhost:4444/wd/hub"):
        super(DetailsBot, self).__init__(path)
        self.user = User()

    def getBio(self) -> str:
        return self.find_element_by_css_selector(".QGPIr").get_attribute("innerText")

    def instagramDetails(self) -> User:
        header = self.find_element_by_css_selector(".k9GMp")
        posts = header.find_element_by_css_selector("li:nth-child(1)").get_attribute("innerText")
        followers = header.find_element_by_css_selector("li:nth-child(2)").get_attribute("innerText")
        following = header.find_element_by_css_selector("li:nth-child(3)").get_attribute("innerText")
        self.user.addHeader(posts, following, followers)
        return self.user

    def getProfilePicture(self) -> User:
        img_url = self.find_element_by_css_selector(".RR-M- img") \
            .get_attribute("src")

        self.user.addProfilePicture(img_url)
        return self.user

    def getDetails(self) -> User:
        self.instagramDetails()
        return self.getProfilePicture()

    def getFollowers(self, followers):
        header = self.find_element_by_css_selector(".k9GMp")
        followers_element = header.find_element_by_css_selector("li:nth-child(2) > a")
        followers_element.click()
        time.sleep(2)
        # Performs mouse move action onto the element
        target = self.find_element_by_css_selector(".isgrP")

        elements = []
        previous_count = 0
        while True:
            self.execute_script("arguments[0].scrollBy(0,10000000);", target)

            elements = elements + self.find_elements_by_css_selector(".isgrP ul li")
            for e in elements:
                try:
                    self.user.addFollowers(e.find_element_by_css_selector("a.FPmhX").get_attribute("innerText"))
                except Exception as e:
                    continue

            elements = set(elements)
            elements = list(elements)

            print(f"Extract following records {len(elements)}")
            if len(elements) <= previous_count:
                break
            previous_count = len(elements)


    def closeFollow(self):
        self.find_element_by_css_selector("div.WaOAr:nth-child(3) > button:nth-child(1)").click()

    def getFollowing(self, following):
        header = self.find_element_by_css_selector(".k9GMp")
        following_element = header.find_element_by_css_selector("li:nth-child(3) > a")
        following_element.click()
        time.sleep(2)
        # Performs mouse move action onto the element
        target = self.find_element_by_css_selector(".isgrP")

        elements = []
        previous_count = 0
        while True:
            self.execute_script("arguments[0].scrollBy(0,10000000);", target)

            elements = elements + self.find_elements_by_css_selector(".isgrP ul li")
            for e in elements:
                try:
                    self.user.addFollowing(e.find_element_by_css_selector("a.FPmhX").get_attribute("innerText"))
                except Exception as e:
                    continue

            elements = set(elements)
            elements = list(elements)

            print(f"Extract following records {len(elements)}")
            if len(elements) <= previous_count:
                break
            previous_count = len(elements)

