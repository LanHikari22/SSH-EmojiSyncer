##
# main module
# Creator: Lan
# Date Created: 7/29/17
# Call pthis and supply commands in order to activate the program's functionality.
##
import os
import glob
import hashlib
import paramiko

class FileEntry:
    _path = None
    _hash = None
    isNew = None # First time seen by client
    isModified = None # Seen by client, but has a different hash

    def __init__(self, path, hash=None, isNew=None, isModified=None):
        self._path = path
        self._hash = hash
        self.isNew = isNew
        self.isModified = isModified
        pass


def printState(filename):
    file = open(filename, 'w')
    for path in glob.iglob('./**/*', recursive=True):
        if os.path.isfile(path):
            file.write("%s " % path)
            temp = open(path, "br")
            file.write("%s\n" % hashlib.sha1(temp.read()).hexdigest())

    file.close()

def printChange(stateFilename, filename):
    file = open(filename, "w")
    stateFile = open(stateFilename, "r")
    prevFiles = [line.strip() for line in stateFile.readlines()]
    currFiles = [f for f in glob.iglob('./**/*', recursive=True)] # those actually include directories too, hmm

    for path in currFiles:
        if path not in prevFiles:
            file.write("[+] %s\n" % (path))

    file.close()
    stateFile.close()

##
# Parses entries from filename to a list of FileEntry objects.
# returns list of parsed FileEntry objects
##
def parseState(filename):
    pass

##
# returns list of FileEntry objects parsed from current directory
##
def getState():
    pass

class Main:
    USER = "lan"
    PATH =  "/home/%s/Desktop" % (USER)

    if __name__ == "__main__":
        pass
    
    def oldmain(self):
            os.chdir(PATH)
            dir = os.listdir(".")
            dirPath = "./Characters"
            if "Characters" in dir:
                os.chdir("./Characters")
                printState("%s/Character-State" % (PATH))
                printChange("%s/Character-State" % (PATH),"%s/Character-Changelog" % (PATH))
            else:
                print("Hey man, create a 'Characters' directory :T")

