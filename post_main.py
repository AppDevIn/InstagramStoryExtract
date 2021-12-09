import os
import pdb
import sys
import time
from datetime import datetime
import json
import yaml

from src.Bot.PostBot import PostBot
from src.DateUtil import DateUtil
from src.Exception.CustomException import InstagramException, MissingArgumentException
from src.FileUtil import FileUtil, writeVideo, writeImage, setUpLogging

from dotenv import load_dotenv
from src.model.ListOfPostModel import ListOfPost, ListOfPostEncoder
from src.model.post import Post

load_dotenv()
env = os.getenv('env')

list_of_arguments = ["--id", "--account", "--profile", "--attempt", "-r"]


def isHeadless(args):
    return "--headless" in args


def isId(args):
    return "--id" in args and "--account" in args and "--profile" in args


def hasAttempt():
    return "--attempt" in sys.argv


def hasProfile():
    return "--profile" in sys.argv


def hasRetry():
    return "-r" in sys.argv


def getId(args) -> str:
    index = args.index("--id") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--id value is not added")

    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--id value is not added")


def getAccount(args) -> str:
    index = args.index("--account") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--account value is not added")
    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--id value is not added")


def getProfile(args) -> str:
    index = args.index("--profile") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--profile value is not added")

    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--profile value is not added")


def getAttempt(args=sys.argv) -> str:
    index = args.index("--attempt") + 1
    if index > (len(args) - 1):
        raise MissingArgumentException("--attempt value is not added")

    if args[index] not in list_of_arguments:
        return args[index]
    else:
        MissingArgumentException("--attempte value is not added")


def downloadFile(post: Post, profile_name) -> bool:
    file = FileUtil(f"{data_path}/{profile_name}/{post.id}/")
    index = 0
    hasDownloadedAll = True
    for m in post.media:
        try:
            if m.video:
                writeVideo(m.media, index, file.createFolder().getDir())
            else:
                writeImage(m.media, index, file.createFolder().getDir())
            index += 1
        except Exception as e:
            hasDownloadedAll = False
            logger.error(f"Failed to download image from post id: {post.id} index {index} due to {e}")

    logger.info(f"Downloaded id {post.id} {index} times out of {len(post.media)}")
    return hasDownloadedAll


def downloadFiles(posts, profile_name):
    logger.info(f"Attempting to download {posts.getSize()} posts from {profile_name}")
    failed = []
    count = 0
    for post in posts.getAll():
        if not downloadFile(post, profile_name):
            failed.append(post.id)
        if count % 10 == 0:
            logger.info(f"{count}/{posts.getSize()} has been downloaded")
        count += 1
    if len(failed) is not 0:
        logger.error(f"Failed to completely download this ids {failed}")

    logger.info(f"{count}/{posts.getSize()} have been downloaded")


def everySuccessfulPost(posts: ListOfPost):
    if posts.getSize() % 10 == 0:
        logger.info(f"Total number of post extracted so far are {posts.getSize()}")


def failedExtract(id, e):
    logger.error(f"Failed to extract the post id {id} due to {str(e)})")


def main(bot: PostBot, method):
    logger.info("Opening the landing page")
    bot.landOnPage()
    bot.waitTillLoginPageLoaded(10)
    logger.info("The page has loaded")
    bot.loginIntoInstagram(username, password)
    logger.info("Attempting with the credentials given in config.yaml")
    logger.info(f"Login with username {username}")
    bot.waitTillInstagramLogoDetected(10)
    logger.info("Login was successful")

    method(bot)


def defaultMethod(bot: PostBot):
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

            file = FileUtil(f"{data_path}/{profileList[0]}/records/{datetime.now().strftime(DateUtil.DATE_FORMAT)}",
                            f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.json")
            downloadFiles(posts, profileName)
            with open(file.createFolder().getPath(), "w") as outfile:
                data = json.dumps(posts, cls=ListOfPostEncoder, ensure_ascii=False)
                outfile.write(data)
        except InstagramException as e:
            logger.error(e.message)


def idMethod(bot: PostBot):
    list_of_id = getId(sys.argv).split(",")
    posts: ListOfPost = ListOfPost()
    file = FileUtil(f"{data_path}/{profileList[0]}/records/{datetime.now().strftime(DateUtil.DATE_FORMAT)}",
                    f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.json")
    for id in list_of_id:
        bot.landOnPostById(id)
        post: Post = bot.getPost(id)
        downloadFile(post, profileList[0])
        posts.add(post)

    with open(file.createFolder().getPath(), "w") as outfile:
        data = json.dumps(posts, cls=ListOfPostEncoder, ensure_ascii=False)
        outfile.write(data)


def run(method, attempt=0):
    postBot = PostBot(isHeadless(sys.argv), path=chrome_path, mode=mode)
    try:
        main(postBot, method)
        postBot.closeDriver()
    except InstagramException as e:
        postBot.closeDriver()
        logger.error(e.message)
        if (hasRetry() or hasAttempt()) and attempt < retry_attempt:
            attempt += 1
            run(method, attempt)
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

    chrome_path = config["driver"]["path"]
    mode = config["driver"]["mode"]
    config = config[f"instagram-{env}"]
    data_path = config["post"]
    log_path = config["directory"] + data_path["logs"]
    json_filename = data_path["json_filename"]
    data_path = config["directory"] + data_path["data"]
    zone = config["timezone"]

    if hasAttempt():
        retry_attempt = int(getAttempt())
    else:
        retry_attempt = config["retry_attempt"]

    logFile = FileUtil(f"{log_path}/{datetime.now().strftime(DateUtil.DATE_FORMAT)}"
                       , f"{datetime.now().strftime(DateUtil.TIME_FORMAT)}.log")

    logger = setUpLogging(logFile.createFolder().getPath())

    if isId(sys.argv) or hasProfile():
        username = config[f"account-{getAccount(sys.argv)}"]["username"]
        password = config[f"account-{getAccount(sys.argv)}"]["password"]

    if isId(sys.argv):
        profileList = [getProfile(sys.argv)]
        run(idMethod)
    elif hasProfile():
        profileList = [getProfile(sys.argv)]
        run(defaultMethod)
    else:
        for user in config["accounts"]:
            username = config[f"account-{user}"]["username"]
            password = config[f"account-{user}"]["password"]
            profileList = config[f"account-{user}"]["profile"]
            if profileList is not None:
                run(defaultMethod)
