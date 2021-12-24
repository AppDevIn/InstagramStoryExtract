import os
import pdb
import sys
from datetime import datetime
import requests
import yaml
from main import Yaml

from src.Bot.HighlightBot import HighlightBot
from src.Bot.StoryBot import StoryBot
from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging
from src.Selenium import InstagramSelenium
from dotenv import load_dotenv

from src.model.HighlightsModel import HighlightsModel
from src.model.UserHighlightModel import UserHighlightModel

load_dotenv()
env = os.getenv('env')

y = Yaml(f"{os.path.dirname(os.path.realpath(__file__))}/config.yaml")


@y.value(f"instagram-{env}.accounts")
def users(): pass
@y.value(f"instagram-{env}.timezone")
def zone(): pass
@y.value(f"instagram-{env}.directory")
def directory(): pass
@y.value(f"instagram-{env}.highlight.logs")
def log(): pass
@y.value(f"instagram-{env}.highlight.data")
def data(): pass
@y.value(f"instagram-{env}.account-{users[0]}.username")
def username(): pass
@y.value(f"instagram-{env}.account-{users[0]}.password")
def password(): pass
@y.value(f"instagram-{env}.account-{users[0]}.profile")
def profiles(): pass


profileName = profiles[0]
data_path = directory + data
log_path = directory + log


def isHeadless(args):
    return "--headless" in args


def isId(args):
    return "--id" in args


def isAll(args):
    return "--all" in args


def getId(args) -> str:
    index = args.index("--id") + 1
    if index > (len(args) - 1):
        return ""
    return args[index]


def downloadFiles(stories, highlight_name):
    logger.info(f"Attempting to download {highlight_name} with {stories.getSize()} highlights")

    count = 0
    for story in stories.getAll():
        file = FileUtil(f"{data_path}/{profileName}/{highlight_name}/")
        filename = story.dateTime.strftime(DateUtil.DATETIME_FORMAT_WITH_UNDERSCORE)
        try:
            if story.video:
                writeVideo(story.media, filename, file.createFolder().getDir())
            else:
                writeImage(story.media, filename, file.createFolder().getDir())
            if count % 10 == 0:
                logger.info(f"{count}/{stories.getSize()} has been downloaded")
            count += 1
        except Exception as e:
            logger.error(f"Failed to download image from highlight: {highlight_name} ")

    logger.info(f"{count}/{stories.getSize()} have been downloaded")


def default(instagram: InstagramSelenium, highlights):
    highlights = instagram.getHighlights()
    instagram.restartHighLightPosition()
    index = 0
    for name in highlights.arrOfNames:
        index += 1
        print(f"{index}. {name}")
    chosenName = input("Pick a index: ")
    instagram.clickOnHighLightSelected(highlights.arrOfNames[int(chosenName)])


def idRun(bot: StoryBot, name):
    bot.clickOnConfirmationToView()
    logger.info(f"Able to view the user story")

    highlight = UserHighlightModel(name)

    logger.info("Starting to extract highlight")
    while bot.stillInStory():
        bot.implicitly_wait(0)
        dateTime = DateUtil.utc_time_to_zone(bot.getTimeOfStory(), zone)

        if bot.isVideo():
            highlight.add(bot.getVideoLink(), dateTime, True)
        else:
            highlight.add(bot.getImageLink(), dateTime, False)

        bot.next()
    logger.info("End highlight extract")
    bot.implicitly_wait(5)

    logger.info(f"The number of image/video needed to be downloaded are {highlight.getSize()}")
    downloadFiles(highlight, highlight.name)


def allHighlightRun(bot: HighlightBot):
    # Click the first highlight
    bot.clickOnHighlight()

    highlight = UserHighlightModel(bot.getName())
    highlights = HighlightsModel()

    logger.info("Start of highlight extract")
    logger.info(f"Extract highlight {highlight.name}")
    while bot.stillInHighlight(profileName):
        if highlight.name != bot.getName():
            highlights.add(highlight)
            logger.info(f"{highlight.name} has {highlight.getSize()} highlight")
            highlight = UserHighlightModel(bot.getName())
            logger.info(f"Extract highlight {highlight.name}")

        bot.implicitly_wait(0)
        dateTime = DateUtil.utc_time_to_zone(bot.getTimeOfHighlight(), zone)

        if bot.isVideo():
            highlight.add(bot.getVideoLink(), dateTime, True)
        else:
            highlight.add(bot.getImageLink(), dateTime, False)

        bot.next()
    highlights.add(highlight)
    logger.info(f"{highlight.name} has {highlight.getSize()}")
    logger.info("End highlight extract")
    bot.implicitly_wait(5)
    logger.info(f"The number of image/video needed to be downloaded are {highlights.getTotalMediaSize()}")

    for highlight in highlights.getAll():
        downloadFiles(highlight, highlight.name)


def main(bot: HighlightBot):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in config.yaml")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(10)
    logger.info("Login was successful")
    logger.info(f"Attempting to open the user profile of {profileName}")
    bot.landProfilePage(profileName)
    bot.waitTillInstagramLogoDetected(10)
    logger.info(f"User profile opened successfully")

    if not bot.hasHighlight(5):
        raise InstagramException("No existing highlight on profile", str(e))

    if isId(sys.argv) is True and getId(sys.argv) is not None:
        bot.landOnHighlightById(getId(sys.argv))
        highlight_name = bot.getName()
        bot.__class__ = StoryBot
        idRun(bot, highlight_name)
    elif isAll(sys.argv) is True:
        allHighlightRun(bot)
    else:
        highlight_id = input("What is the highlight id: ")
        bot.landOnHighlightById(highlight_id)
        highlight_name = bot.getName()
        bot.__class__ = StoryBot
        idRun(bot, highlight_name)

    bot.closeDriver()


if __name__ == "__main__":
    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    highlightBot = HighlightBot(isHeadless(sys.argv))

    try:
        main(highlightBot)
    except InstagramException as e:
        highlightBot.closeDriver()
        logger.error(e.message)
    except Exception as e:
        highlightBot.closeDriver()
        logger.error(f"Unexpected error: {e}")
