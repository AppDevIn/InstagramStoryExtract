import os
import sys
import pdb

import requests

from src.DateUtil import DateUtil
from src.FileUtil import FileUtil
from src.Selenium import InstagramSelenium
from dotenv import load_dotenv
import logging

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

def isHeadless(args):
    return "--headless" in sys.argv


def setUpLogging(filename: str) -> logging.Logger:
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return logger


def default(instagram: InstagramSelenium, highlights):
    highlights = instagram.getHighlights()
    instagram.restartHighLightPosition()
    index = 0
    for name in highlights.arrOfNames:
        index += 1
        print(f"{index}. {name}")
    chosenName = input("Pick a index: ")
    instagram.clickOnHighLightSelected(highlights.arrOfNames[int(chosenName)])


def main(instagram: InstagramSelenium):
    if not instagram.loginToInstagram(username, password):
        instagram.closeDriver()
        exit()

    if not instagram.visitProfilePage(profileName):
        instagram.closeDriver()
        exit()

    if not instagram.hasHighlight():
        instagram.closeDriver()
        exit()

    id = input("What is the highlight id: ")
    instagram.visitHighlight(id)

    image_count = 0

    while instagram.stillInStory():
        dateTime = DateUtil.utc_time_to_zone(instagram.getTimeFromStory(), zone)

        path = FileUtil(f"{data_path}/{dateTime.strftime(DateUtil.DATE_FORMAT)}/") \
            .createFolder().getDir()

        logger.info(f"Story was posted on {dateTime}")
        logger.info(f"File is saved into {path}")

        filename = dateTime.strftime(DateUtil.TIME_FORMAT)

        videoLink = instagram.getStoryVideoLink()

        if videoLink != "":
            downloadVideo(videoLink, filename, path)
        else:
            downloadImage(instagram.getStoryImageLink(), filename, path)
        image_count += 1

        instagram.nextStory()

    logger.info(f"The number of image/video downloaded are {image_count}")
    instagram.closeDriver()


if __name__ == "__main__":
    logFile = FileUtil(log_path, f"{DateUtil.getCurrentDateTime().strftime(DateUtil.DATETIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    instagramSelenium = InstagramSelenium(logger, isHeadless(sys.argv))

    try:
        main(instagramSelenium)
    except Exception as e:
        instagramSelenium.closeDriver()
        logger.error(f"Unexpected error: {e}")