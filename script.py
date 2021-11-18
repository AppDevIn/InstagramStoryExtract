# Simple assignment
import requests
import os
import logging
from datetime import date, datetime
from dotenv import load_dotenv
from src.FileUtil import FileUtil
from src.Selenium import InstagramSelenium
import sys

load_dotenv()
username = os.getenv('username')
password = os.getenv('password')
profileName = os.getenv('default_account')
log_path = os.getenv('log_folder')
data_path = os.getenv('data_folder')


def downloadImage(link, name, path):
    url = link.split()[0]
    r = requests.get(url)

    open(f'{path}{name}.jpg', 'wb').write(r.content)


def downloadVideo(url, name, path):
    r = requests.get(url)

    open(f'{path}{name}.mp4', 'wb').write(r.content)


def getDate() -> str:
    today = date.today()
    return today.strftime("%Y%m%d")


def setUpLogging(filename: str) -> logging.Logger:
    # Logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)
    return logger


def isHeadless(args):
    return "--headless" in sys.argv


def main(instagram: InstagramSelenium):
    if not instagram.loginToInstagram(username, password):
        instagram.closeDriver()
        exit()

    if not instagram.visitUserStoryPage(profileName):
        instagram.closeDriver()
        exit()

    image_count = 0
    dataFile = FileUtil(f"{data_path}/{getDate()}/")
    path = dataFile.createFolder(True).getDir()
    logger.info(f"Files will be stored in {path}")

    while instagram.stillInStory():
        videoLink = instagram.getStoryVideoLink()
        filename = instagram.getTimeFromStory().strftime("%H%M%S")
        if videoLink != "":
            downloadVideo(videoLink, filename, path)
        else:
            downloadImage(instagram.getStoryImageLink(), filename, path)
        image_count += 1

        instagram.nextStory()

    logger.info(f"The number of image/video downloaded are {image_count}")

    instagram.closeDriver()


if __name__ == "__main__":
    logFile = FileUtil(log_path, f"{datetime.now().strftime('%Y%m%d%H%M%S')}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    instagram = InstagramSelenium(logger, isHeadless(sys.argv))
    try:
        main(instagram)
    except Exception as e:
        instagram.closeDriver()
        logger.error(f"Unexpected error: {e}")
