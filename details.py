import os
import sys
import time
from datetime import datetime
import json
import yaml

from src.Bot.DetailsBot import DetailsBot
from src.Bot.PostBot import PostBot
from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging

from dotenv import load_dotenv
from src.model.ListOfPostModel import ListOfPost, ListOfPostEncoder
from src.model.UserModel import User

load_dotenv()
env = os.getenv('env')


def isHeadless(args):
    return "--headless" in args


def isId(args):
    return "--id" in args


def getId(args) -> str:
    index = args.index("--id") + 1
    if index > (len(args) - 1):
        return ""
    return args[index]


def main(bot: DetailsBot):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in config.yaml")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(10)
    logger.info("Login was successful")

    for profileName in profileList:
        try:
            logger.info(f"Attempting to open the user profile of {profileName}")
            bot.landProfilePage(profileName)
            bot.waitTillInstagramLogoDetected(10)
            logger.info(f"User profile opened successfully")

            user_profile = bot.getDetails()
            user_profile.username = profileName

            logger.info(f"Number of posts {user_profile.posts}")
            logger.info(f"Number of followers {user_profile.followers}")
            logger.info(f"Number of following {user_profile.following}")
            logger.info(f"Number of profile url {user_profile.profile_picture}")

            bot.getFollowing(user_profile.following)
        except InstagramException as e:
            logger.error(e.message)


def run(attempt=0):
    detailsBot = DetailsBot(isHeadless(sys.argv))
    try:
        main(detailsBot)
        detailsBot.closeDriver()
    except InstagramException as e:
        detailsBot.closeDriver()
        logger.error(e.message)
        if attempt < 3:
            attempt += 1
            run(attempt)
    except Exception as e:
        detailsBot.closeDriver()
        logger.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    config = {}
    with open('config.yaml') as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(exc)

    config = config[f"instagram-{env}"]
    data_path = config["post"]
    log_path = config["directory"] + data_path["logs"]
    json_filename = data_path["json_filename"]
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
