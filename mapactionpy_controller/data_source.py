# TODO: asmith 2020/03/04
#
# Compare this class to the implementation here:
#       cmf_watcher.cmf_handler._hash_files(...)
# I think the implenmentation here (ie in the DataSource class) handles shapefiles better - notably
# handling lock files. However the use case in the cmf_watcher module is different and creating a
# new DataSource object each time might not be appropriate. Is it possible to refactor this so that it
# achieves boths use-cases?
import os
import hashlib
import glob


class DataSource:
    def __init__(self, pathToDataSource):
        self.parts = list()
        self.pathToDataSource = pathToDataSource

    def calculate_checksum(self):
        if (os.path.isfile(self.pathToDataSource)):
            self.parts = self.constituentParts(self.pathToDataSource)
        elif (os.path.isdir(self.pathToDataSource)):
            self.parts = self.directoryContents(self.pathToDataSource)

        hash = hashlib.md5()
        for fn in self.parts:
            if os.path.isfile(fn):
                hash.update(open(fn, "rb").read())
        return hash.hexdigest()

    def constituentParts(self, fileName):
        paths_to_hash = list()
        directoryName = os.path.dirname(fileName)
        baseName = os.path.basename(fileName)
        root, ext = os.path.splitext(baseName)
        filter = os.path.join(directoryName, root) + "*"
        files = glob.glob(filter)

        for file in files:
            root, ext = os.path.splitext(file)
            if (not(ext.endswith(".lock"))):
                paths_to_hash.append(file)
        return paths_to_hash

    def directoryContents(self, file_directory):
        file_directory = os.path.abspath(file_directory)
        paths_to_hash = list()

        for currentpath, folders, files in os.walk(file_directory):
            for file in files:
                paths_to_hash.append(os.path.join(currentpath, file))
        return(paths_to_hash)
