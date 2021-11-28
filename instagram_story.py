import requests
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException
from src.FileUtil import FileUtil
import sys

from src.Bot.StoryBot import StoryBot

load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
profileName = os.getenv('default_account')
log_path = os.getenv('log_folder')
data_path = os.getenv('data_folder')
zone = os.getenv('timezone')


def downloadImage(link, name, path):
    url = link.split()[0]
    r = requests.get(url)

    open(f'{path}{name}.jpg', 'wb').write(r.content)


def downloadVideo(url, name, path):
    r = requests.get(url)

    open(f'{path}{name}.mp4', 'wb').write(r.content)


def setUpLogging(filename: str) -> logging.Logger:
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)
    return logger


def isHeadless(args):
    return "--headless" in sys.argv


def main(instagram: StoryBot):

    instagram.landOnPage()
    instagram.waitTillLoginPageLoaded(10)
    instagram.loginIntoInstagram(username, password)
    instagram.waitTillInstagramLogoDetected(10)
    instagram.landOnUserStory(profileName)
    instagram.clickOnConfirmationToView()
    #
    # if not instagram.visitUserStoryPage(profileName):
    #     instagram.closeDriver()
    #     exit()
    #
    # image_count = 0
    #
    # while instagram.stillInStory():
    #     dateTime = DateUtil.utc_time_to_zone(instagram.getTimeFromStory(), zone)
    #
    #     path = FileUtil(f"{data_path}/{dateTime.strftime(DateUtil.DATE_FORMAT)}/") \
    #         .createFolder().getDir()
    #
    #     logger.info(f"Story was posted on {dateTime}")
    #     logger.info(f"File is saved into {path}")
    #
    #     filename = dateTime.strftime(DateUtil.TIME_FORMAT)
    #
    #     videoLink = instagram.getStoryVideoLink()
    #
    #     if videoLink != "":
    #         downloadVideo(videoLink, filename, path)
    #     else:
    #         downloadImage(instagram.getStoryImageLink(), filename, path)
    #     image_count += 1
    #
    #     instagram.nextStory()
    #
    # logger.info(f"The number of image/video downloaded are {image_count}")
    #
    # instagram.closeDriver()


if __name__ == "__main__":
    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    instagram = StoryBot(isHeadless(sys.argv))
    try:
        main(instagram)
    except InstagramException as e:
        instagram.closeDriver()
        logger.error(e.message)
