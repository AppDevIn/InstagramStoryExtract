# Simple assignment
import time
from urllib.parse import uses_relative
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests
import os
from datetime import date
import uuid0


username = os.environ['instagram_username']
password = os.environ['instagram_password']
default = os.environ['instagram_default']


def document_initialised(driver):
    return driver.execute_script("return initialised")


def login(driver):
    driver.get("https://www.instagram.com/")
    usernameEle = WebDriverWait(driver, 30).until(
        lambda d: d.find_element_by_name("username"))

    passwordEle = driver.find_element_by_name("password")
    loginBtn = driver.find_element_by_xpath(
        '/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button')

    usernameEle.send_keys(username)
    passwordEle.send_keys(password)

    loginBtn.click()


def reachFeed(driver):
    notNowBtn = WebDriverWait(driver, 30).until(
        lambda d: d.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div/div/button"))

    notNowBtn.click()
    WebDriverWait(driver, 30).until(
        lambda d: d.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[2]")).click()


def getImageLink() -> str:
    image = driver.find_element_by_xpath(
        "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/img")
    value = image.get_attribute("srcset")
    value = value.split(',')
    return value[0]


def getVideoLink() -> str:
    try:
        video = driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/video/source")

        videoValue = video.get_attribute("src")
        return videoValue

    except Exception:
        return ""


def nextStory() -> bool:
    try:
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/button[2]")
        if driver.current_url == "https://www.instagram.com/":
            return False
        return True
    except NoSuchElementException:
        return False


def downloadImage(link, name, path):
    url = link.split()[0]
    r = requests.get(url)

    open(f'./{path}{name}.jpg', 'wb').write(r.content)


def downloadVideo(url, name, path):
    r = requests.get(url)

    open(f'./{path}{name}.mp4', 'wb').write(r.content)


def createFolder(date) -> str:
    path = f"record/{date}/"
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        path = f"{path}{uuid0.generate()}/"
        os.makedirs(path)
    return path


def getDate() -> str:
    today = date.today()
    return today.strftime("%Y%m%d")


def validatename(name) -> str:
    if name == '':
        return default
    else:
        return name


if __name__ == "__main__":
    profileName = validatename(input("Which instagram: "))

    driver = webdriver.Chrome(
        ChromeDriverManager().install())

    print(f"Logging in to account {username}")
    login(driver)

    print(f"Trying to reach feed")
    reachFeed(driver)

    print(f"Entering the {profileName} profile")
    driver.get(
        f"https://www.instagram.com/stories/{profileName}/2602290251374219276/")

    print("Clicking on the profile")
    WebDriverWait(driver, 30).until(
        lambda d: d.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/div[1]/div/div/div/div[3]/button")).click()

    print("Looping through the story")
    imagesArr = []
    CURRENT_DATE = getDate()
    path = createFolder(CURRENT_DATE)
    while nextStory():
        imagesArr.append(getImageLink())
        videoLink = getVideoLink()
        if videoLink != "":
            downloadVideo(videoLink, len(imagesArr), path)
        else:
            downloadImage(getImageLink(), len(imagesArr), path)

        driver.find_element_by_xpath(
            "/html/body/div[1]/section/div[1]/div/section/div/button[2]").click()
    driver.close()
    print(imagesArr)
