import os
import pathlib
import pdb
from datetime import datetime

import yaml
from dotenv import load_dotenv

from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException, MissingArgumentException, LoginException, \
    NoUserStoryException, StoryExtractionException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging
import sys

from src.Bot.StoryBot import StoryBot
from src.model.DriverModeEnum import DriverMode
from src.model.StoriesModel import StoriesModel
from functools import partial

from telegrambot.bot import TeleBot

load_dotenv()
env = os.getenv('env')

list_of_arguments = ["--gui", "--headless", "-r", "--attempt", "-t"]


def isHeadless(args):
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


def send_photo(photo):
    if hasTele():
        telebot.send_photo(chatId, photo)


def getAttempt(args=sys.argv) -> str:
    index = args.index("--attempt") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--attempt value is not added")

    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--attempte value is not added")


def downloadFiles(bot: StoryBot, stories: StoriesModel, profile_name):
    for story in stories.getAll():
        file = FileUtil(f"{data_path}/{profile_name}/{story.dateTime.strftime(DateUtil.DATE_FORMAT)}/")
        filename = story.dateTime.strftime(DateUtil.TIME_FORMAT)
        if story.video:
            writeVideo(story.media, filename, file.createFolder().getDir())
        else:
            writeImage(story.media, filename, file.createFolder().getDir())
        logger.info(f"File is saved into {file.getDir()}")
    snapScreenshotOfProfile(bot, profile_name)


def snapScreenshotOfProfile(bot, profile_name):
    bot.landProfilePage(profile_name)
    screenshot_path = f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}/screenshot_{profile_name}.png"
    logger.info(f"Saving screenshot in {screenshot_path}")
    bot.takeScreenshot(".zw3Ow", screenshot_path)
    send_photo(screenshot_path)


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

    bot.login(username, password, logger)

    for profileName in profileList:
        try:

            stories = bot.extractStories(logger, profileName)

            logger.info(f"The number of image/video needed to be downloaded are {stories.getSize()}")
            logger.info(f"Attempting to download them")
            downloadFiles(bot, stories, profileName)
            send_telemessage(f"{profileName} has {stories.getSize()} image/video and is downloaded")
        except StoryExtractionException as e:
            logger.error(e.message)
            send_telemessage(f"Sir, we experience unknown error {e.message}")
        except NoUserStoryException as e:
            logger.info(e.message)
            snapScreenshotOfProfile(bot, profileName)
            send_telemessage(f"Sir, {profileName} has no story today")


def run(attempt=0):
    instagram = StoryBot(isHeadless(sys.argv), path=chrome_path, mode=mode)
    try:
        main(instagram)
        instagram.closeDriver()
    except InstagramException as e:
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
    send_telemessage(f"Greetings sir, it's currently {datetime.now().strftime(DateUtil.TIME_FORMAT_NO_UNDERSCORE)},"
                     f" starting scrap protocol")
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
        send_telemessage(f"Sir, following profiles {', '.join(profileList)} with access from {user} account")
        if profileList is not None:
            run()

    send_telemessage("Sir, we have scrapped all the requested data. Have great day ahead sir 😊")
