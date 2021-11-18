import os
import uuid0


class FileUtil:
    def __init__(self, path):
        self.path = path

    def hasExistingFolder(self):
        return os.path.isdir(self.path)

    def createFolder(self, createUniqueSubFolderIfExits=False) -> str:
        if not self.hasExistingFolder():
            os.makedirs(self.path)
        elif createUniqueSubFolderIfExits:
            self.path = f"{self.path}{uuid0.generate()}/"
            os.makedirs(self.path)

        return self.path
