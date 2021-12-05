from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from src.Bot.BaseBot import BaseBot
from src.Exception.CustomException import InstagramException
from src.model.ListOfPostModel import ListOfPost
from src.model.post import Media, Post, Comment
import src.model.constants as const

import pdb


class PostBot(BaseBot):
    def __init__(self, headless):
        super(PostBot, self).__init__(headless)

    def landOnPostById(self, id):
        self.get(f"{const.BASE_URL}/p/{id}")

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

    def hasCaption(self):
        self.implicitly_wait(1)
        try:
            self.find_element_by_css_selector(".ZyFrc .C4VMK > span")
            return True
        except Exception:
            return False
        finally:
            self.implicitly_wait(5)

    def hasNextMediaButton(self):
        self.implicitly_wait(1)
        try:
            self.find_element_by_css_selector("div.qF0y9.Igw0E > div > button._6CZji")
            return True
        except Exception:
            return False
        finally:
            self.implicitly_wait(5)

    def closePost(self):
        self.find_element_by_css_selector("div._2dDPU > div.qF0y9 > button").click()

    def nextPost(self):
        self.find_element_by_css_selector(".l8mY4 .wpO6b").click()

    def getLikes(self) -> str:
        try:
            return self.find_element_by_css_selector("section.EDfFK.ygqzn > div").get_attribute(
                "innerText")
        except Exception:
            return None

    def hasMoreCommentsButton(self) -> bool:
        self.implicitly_wait(1)
        try:
            self.find_element_by_css_selector("div.qF0y9.NUiEW button.wpO6b")
            return True
        except Exception:
            return False
        finally:
            self.implicitly_wait(5)

    def clickOnMoreCommentsButton(self):
        self.find_element_by_css_selector("div.qF0y9.NUiEW button.wpO6b").click()

    def getComments(self) -> [Comment]:
        while self.hasMoreCommentsButton():
            self.clickOnMoreCommentsButton()

        comments = []
        comments_element = self.find_elements_by_css_selector(".C4VMK")
        for comment_element in comments_element:
            user = comment_element.find_element_by_css_selector("span a").get_attribute("innerHTML")
            comment = comment_element.find_element_by_css_selector("span:nth-child(2)").get_attribute("innerHTML")
            time = comment_element.find_element_by_css_selector("time").get_attribute("datetime")[:-5]
            time = str(datetime.strptime(time, "%Y-%m-%dT%H:%M:%S"))
            comments.append(Comment(user, comment, time))
        return comments

    def getPost(self, id) -> Post:
        caption = None
        if self.hasCaption():
            caption = self.find_element_by_css_selector(".ZyFrc .C4VMK > span").get_attribute("innerHTML")
        time = self.find_element_by_css_selector("._1o9PC").get_attribute("datetime")[:-5]
        comments = self.getComments()
        time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
        likes = self.getLikes()
        post = Post(id, [], str(time), caption, likes, comments)

        while True:
            if self.hasImg():
                post.addMedia(list(
                    map(lambda x: Media(x.get_attribute("src")), self.find_elements_by_css_selector(".qF0y9 .FFVAD"))))
            else:
                post.addMedia(
                    list(map(lambda x: Media(x.get_attribute("src"), True),
                        self.find_elements_by_css_selector(".qF0y9 .tWeCl"))))
            if self.hasNextMediaButton():
                self.find_element_by_css_selector("div.qF0y9.Igw0E > div > button._6CZji").click()
            else: break
        return post

    def getPosts(self, callback, failedCallback) -> ListOfPost:
        self.find_elements_by_css_selector(".eLAPa")[0].click()
        posts = ListOfPost()
        while True:
            id = self.current_url.split("/p/")[-1][:-1]
            try:
                try:
                    post = self.getPost(id)
                    posts.add(post)
                    callback(posts)
                except Exception as e:
                    failedCallback(id, e)
                if self.hasNextButton(2) is False:
                    break
                self.nextPost()
            except InstagramException as e:
                failedCallback(id, e)
                self.nextPost()

        return posts
