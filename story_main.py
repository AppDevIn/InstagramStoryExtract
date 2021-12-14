import os
import pathlib
import pdb
import time
from datetime import datetime

import yaml
from TeleBot import TeleBot
from dotenv import load_dotenv

from src.DateUtil import DateUtil
from src.Exception.CustomException import MissingArgumentException, LoginException, \
    NoUserStoryException, StoryExtractionException, InvalidProfileException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging
import sys

from src.Bot.StoryBot import StoryBot
from src.TextBuilder import TextBuilder
from src.model.StoriesModel import StoriesModel

load_dotenv()
env = os.getenv('env')

list_of_arguments = ["--gui", "--headless", "-r", "--attempt", "-t"]

textBuilder = TextBuilder()


def isHeadless():
    return "--headless" in sys.argv


def isGUI():
    return "--gui" in sys.argv


def hasAttempt():
    return "--attempt" in sys.argv


def hasRetry():
    return "-r" in sys.argv


def hasTele():
    return "-t" in sys.argv


def send_telemessage(message):
    if hasTele():
        telebot.send_message(chatId, message)


def getAttempt(args=sys.argv) -> str:
    index = args.index("--attempt") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--attempt value is not added")

    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--attempte value is not added")


def downloadFiles(stories: StoriesModel, profile_name, data_path, logger):
    for story in stories.getAll():
        file = FileUtil(f"{data_path}/{profile_name}/{story.dateTime.strftime(DateUtil.DATE_FORMAT)}/")
        filename = story.dateTime.strftime(DateUtil.TIME_FORMAT)
        if story.video:
            writeVideo(story.media, filename, file.createFolder().getDir())
        else:
            writeImage(story.media, filename, file.createFolder().getDir())
        logger.info(f"File is saved into {file.getDir()}")


def snapScreenshotOfProfile(bot, profile_name, path) -> str:
    time.sleep(2)
    screenshot_path = f"{path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}/screenshot_{profile_name}.png"
    bot.takeScreenshot(".zw3Ow", screenshot_path)
    return screenshot_path


def main(bot: StoryBot):

    bot.login(username, password, logger)

    for profileName in profileList:
        try:
            stories = bot.extractStories(logger, profileName, zone)
            logger.info(f"The number of image/video needed to be downloaded are {stories.getSize()}")
            logger.info(f"Attempting to download them")
            downloadFiles(stories, profileName, data_path=data_path, logger=logger)
            bot.landProfilePage(profileName)
            screenshot_path = snapScreenshotOfProfile(bot, profileName, log_path)
            logger.info(f"Saving screenshot in {screenshot_path}")
            textBuilder.addText(f"{profileName}: {stories.getSize()} stories ✅")
        except StoryExtractionException as e:
            logger.error(e.message)
            textBuilder.addText(f"{profileName}: Error has occurred ⛔️")
        except NoUserStoryException as e:
            logger.info(e.message)
            screenshot_path = snapScreenshotOfProfile(bot, profileName, log_path)
            textBuilder.addText(f"{profileName}: No story 😳")
        except InvalidProfileException as e:
            logger.error(e.message)
            textBuilder.addText(f"{profileName}: {e.message} ⚠️")


def run(attempt=0):
    instagram = StoryBot(isHeadless(), path=chrome_path, mode=mode)
    try:
        main(instagram)
        instagram.closeDriver()
    except LoginException as e:
        instagram.closeDriver()
        logger.error(e.message)
        if (hasRetry() or hasAttempt()) and attempt < retry_attempt:
            logger.info("Failed to login, retrying...")
            attempt += 1
            run(attempt)
    except Exception as e:
        logger.error(str(e))
        instagram.closeDriver()


if __name__ == "__main__":
    c = {}
    with open(f'{pathlib.Path(__file__).parent.resolve()}/config.yaml') as file:
        try:
            c = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    chrome_path = c["driver"]["path"]
    mode = c["driver"]["mode"]
    config = c[f"instagram-{env}"]
    data_path = config["story"]
    log_path = config["directory"] + data_path["logs"]
    data_path = config["directory"] + data_path["data"]
    zone = config["timezone"]
    TOKEN = c["telegram-api-key"]
    chatId = c["chat-id"]
    telebot = TeleBot(TOKEN)

    if hasAttempt():
        retry_attempt = int(getAttempt())
    else:
        retry_attempt = config["retry_attempt"]
    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())

    for user in config["accounts"]:
        username = config[f"account-{user}"]["username"]
        password = config[f"account-{user}"]["password"]
        profileList = config[f"account-{user}"]["profile"]
        textBuilder.addText(f"*From {user} account* ⛄️")
        if profileList is not None:
            run()
    send_telemessage(textBuilder.build())
