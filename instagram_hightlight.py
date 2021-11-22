import os
import sys
import pdb
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

    highlights = instagram.getHighlights()
    instagram.restartHighLightPosition()

    index = 0
    for name in highlights.arrOfNames:
        index += 1
        print(f"{index}. {name}")
    chosenName = input("Pick a index: ")
    instagram.clickOnHighLightSelected(highlights.arrOfNames[int(chosenName)])


if __name__ == "__main__":
    logFile = FileUtil(log_path, f"{DateUtil.getCurrentDateTime().strftime(DateUtil.DATETIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())
    instagramSelenium = InstagramSelenium(logger, isHeadless(sys.argv))

    try:
        main(instagramSelenium)
    except Exception as e:
        # instagramSelenium.closeDriver()
        logger.error(f"Unexpected error: {e}")