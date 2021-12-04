import os
import sys
import time
from datetime import datetime
import json
import yaml

from src.Bot.PostBot import PostBot
from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging

from dotenv import load_dotenv
from src.model.ListOfPostModel import ListOfPost, ListOfPostEncoder

load_dotenv()
env = os.getenv('env')


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


def downloadFiles(posts, profile_name):
    logger.info(f"Attempting to download {posts.getSize()} posts from {profile_name}")

    count = 0
    for post in posts.getAll():
        file = FileUtil(f"{data_path}/{profile_name}/{post.id}/")
        index = 0
        for m in post.media:
            try:
                if m.video:
                    writeVideo(m.media, index, file.createFolder().getDir())
                else:
                    writeImage(m.media, index, file.createFolder().getDir())
                index += 1
            except Exception as e:
                logger.error(f"Failed to download image from post id: {post.id} index {index} due to {e}")
        if count % 10 == 0:
            logger.info(f"{count}/{posts.getSize()} has been downloaded")
        logger.info(f"Downloaded id {post.id} {index} times out of {len(post.media)}")
        count += 1

    logger.info(f"{count}/{posts.getSize()} have been downloaded")


def everySuccessfulPost(posts: ListOfPost):
    if posts.getSize() % 10 == 0:
        logger.info(f"Total number of post extracted so far are {posts.getSize()}")


def failedExtract(id, e):
    logger.error(f"Failed to extract the post id {id} due to {str(e)})")


def main(bot: PostBot):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in .env")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(10)
    logger.info("Login was successful")

    for profileName in profileList:
        try:
            logger.info(f"Attempting to open the user profile of {profileName}")
            bot.landProfilePage(profileName)
            bot.waitTillInstagramLogoDetected(10)
            logger.info(f"User profile opened successfully")

            if bot.hasPost(5) is False:
                logger.info("No post found")
                bot.closeDriver()
                return

            logger.info("Extracting posts from user profile")
            posts: ListOfPost = bot.getPosts(everySuccessfulPost, failedCallback=failedExtract)
            logger.info(f"Total number of post extracted are {posts.getSize()}")

            downloadFiles(posts, profileName)
            with open(f"{json_filename}_{profileName}.json", "w") as outfile:
                data = json.dumps(posts, cls=ListOfPostEncoder, ensure_ascii=False, )
                outfile.write(data)
        except InstagramException as e:
            logger.error(e.message)


def run(attempt=0):
    postBot = PostBot(isHeadless(sys.argv))
    try:
        main(postBot)
        postBot.closeDriver()
    except InstagramException as e:
        postBot.closeDriver()
        logger.error(e.message)
        if attempt < 3:
            attempt += 1
            run(attempt)
    except Exception as e:
        postBot.closeDriver()
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
    json_filename = config["directory"] + data_path["json_filename"]
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
