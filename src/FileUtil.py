import os
import uuid0
import pdb


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

