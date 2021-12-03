import os
import logging
import pdb
from datetime import datetime
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
username = os.getenv('username')
password = os.getenv('password')
profileName = os.getenv('default_account')
log_path = os.getenv('log_folder')
data_path = os.getenv('data_folder')
zone = os.getenv('timezone')



def isHeadless(args):
    return "--headless" in sys.argv


def isGUI():
    return "--gui" in sys.argv


def main(bot: StoryBot):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in .env")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(10)
    logger.info("Login was successful")
    logger.info(f"Attempting to open the user story of {profileName}")
    bot.landOnUserStory(profileName)
    bot.clickOnConfirmationToView()
    logger.info(f"Able to view the user story")

    stories = StoriesModel()

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

    logger.info(f"The number of image/video needed to be downloaded are {stories.getSize()}")
    logger.info(f"Attempting to download them")

    for story in stories.getAll():
        file = FileUtil(f"{data_path}/{story.dateTime.strftime(DateUtil.DATE_FORMAT)}/")
        filename = story.dateTime.strftime(DateUtil.TIME_FORMAT)
        if story.video:
            writeVideo(story.media, filename, file.createFolder().getDir())
        else:
            writeImage(story.media, filename, file.createFolder().getDir())
        logger.info(f"File is saved into {file.getDir()}")

    bot.closeDriver()


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
    except InstagramException as e:
        instagram.closeDriver()
        logger.error(e.message)
        if isGUI():
            tryAgain(e.message)
    except Exception as e:
        logger.error(str(e))


if __name__ == "__main__":
    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    run()
