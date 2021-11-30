import os

import requests
import uuid0
import pdb
import logging

def writeImage(link, name, path):
    url = link.split()[0]
    r = requests.get(url)

    open(f'{path}{name}.jpg', 'wb').write(r.content)


def writeVideo(url, name, path):
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


class FileUtil:
    def __init__(self, dir_path, filename = None):
        self.dir_path = dir_path
        self.filename = filename

    def hasExistingFolder(self):
        return os.path.isdir(self.dir_path)

    def createFolder(self, createUniqueSubFolderIfExits=False):
        if not self.hasExistingFolder():
            os.makedirs(self.dir_path)
        elif createUniqueSubFolderIfExits and self.hasExistingFolder():
            self.dir_path = f"{self.dir_path}{uuid0.generate()}/"
            os.makedirs(self.dir_path)

        return self

    def getPath(self) -> str:
        return f"{self.dir_path}/{self.filename}"

    def getDir(self) -> str:
        return self.dir_path
