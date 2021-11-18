import os
class FileUtil:

    def __init__(self, path):
        self.path = path

    def hasExistingFolder(self):
        return os.path.isdir(self.path)

    def createFolder(self, methodToCallIfPathExist = None) -> str:
        if not self.hasExistingFolder():
            os.makedirs(self.path)
        elif self.hasExistingFolder() and methodToCallIfPathExist is not None:
            self.path = methodToCallIfPathExist()

        return self.path


