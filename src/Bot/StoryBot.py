from src.Bot.BaseBot import BaseBot
import src.model.constants as const
from src.Exception.CustomException import InstagramException


class StoryBot(BaseBot):

    def __init__(self, headless):
        super(StoryBot, self).__init__(headless)

    def landOnUserStory(self, profile_name):
        self.get(f"{const.BASE_URL}/stories/{profile_name}/")

    def clickOnConfirmationToView(self):
        try:
            self.find_element_by_xpath(
                "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/button").click()
        except Exception as e:
            raise InstagramException("Failed to confirm the user", e)
