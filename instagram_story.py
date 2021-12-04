import os
from datetime import datetime

import yaml
from dotenv import load_dotenv

from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging
import sys

from src.Bot.StoryBot import StoryBot
from src.GUI import GUI
from src.model.StoriesModel import StoriesModel
from functools import partial

load_dotenv()
env = os.getenv('env')


def isHeadless(args):
    return "--headless" in sys.argv


def isGUI():
    return "--gui" in sys.argv


def downloadFiles(bot: StoryBot, stories: StoriesModel, profile_name):
    for story in stories.getAll():
        file = FileUtil(f"{data_path}/{profile_name}/{story.dateTime.strftime(DateUtil.DATE_FORMAT)}/")
        filename = story.dateTime.strftime(DateUtil.TIME_FORMAT)
        if story.video:
            writeVideo(story.media, filename, file.createFolder().getDir())
        else:
            writeImage(story.media, filename, file.createFolder().getDir())
        logger.info(f"File is saved into {file.getDir()}")

    bot.landProfilePage(profile_name)
    screenshot_path = f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}/screenshot_{datetime.now().strftime(DateUtil.TIME_FORMAT)}.png"
    logger.info(f"Saving screenshot in {screenshot_path}")
    bot.takeScreenshot(".zw3Ow", screenshot_path)


def extractStories(bot: StoryBot, stories: StoriesModel) -> StoriesModel:
    logger.info("Starting to extract stories")
    while bot.stillInStory():
        bot.implicitly_wait(0)
        dateTime = DateUtil.utc_time_to_zone(bot.getTimeOfStory(), zone)
        logger.info(f"Story was posted on {dateTime}")

        if bot.isVideo():
            stories.add(bot.getVideoLink(), dateTime, True)
        else:
            stories.add(bot.getImageLink(), dateTime, False)

        bot.next()
    logger.info("End stories extract")
    bot.implicitly_wait(5)
    return stories


def main(bot: StoryBot):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in .env")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(5)
    logger.info("Login was successful")

    for profileName in profileList:
        try:
            logger.info(f"Attempting to open the user story of {profileName}")
            bot.landOnUserStory(profileName)
            bot.clickOnConfirmationToView()
            logger.info(f"Able to view the user story")

            stories = StoriesModel()
            stories = extractStories(bot, stories)

            logger.info(f"The number of image/video needed to be downloaded are {stories.getSize()}")
            logger.info(f"Attempting to download them")
            downloadFiles(bot, stories, profileName)
        except InstagramException as e:
            logger.error(e.message)



def subTryAgain(window):
    window.quit()
    run()


def tryAgain(error):
    gui = GUI(error)
    gui.setPositiveButton("Try again", partial(subTryAgain, gui))
    gui.setNegativeButton("Close")
    gui.start()


def run():
    instagram = StoryBot(isHeadless(sys.argv))
    try:
        main(instagram)
        instagram.closeDriver()
    except InstagramException as e:
        instagram.closeDriver()
        logger.error(e.message)
        if isGUI():
            tryAgain(e.message)
    except Exception as e:
        logger.error(str(e))
        instagram.closeDriver()


if __name__ == "__main__":
    config = {}
    with open('config.yaml') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    config = config[f"instagram-{env}"]
    data_path = config["story"]
    log_path = config["directory"] + data_path["logs"]
    data_path = config["directory"] + data_path["data"]
    zone = config["timezone"]
    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())

    for user in config["accounts"]:
        username = config[f"account-{user}"]["username"]
        password = config[f"account-{user}"]["password"]
        profileList = config[f"account-{user}"]["profile"]
        run()
