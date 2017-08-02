import glob, hashlib
from paramiko import Channel

# protocol control character constants
ACK  = '\vACK'
NCK  = '\vNCK'
END0 = '\vEND0'
END1 = '\vEND1'


class Protocol:
    # common communication features between both client and server

    # The channel endpoint being connected to
    chan = None
    # Channel file (BufferedFile) to recieve data from guest
    chanfile = None

    def __init__(self, chan:Channel):
        self.chan = chan
        # need that U. no universal new line = pressing enter might not stop sending data..
        self.chanfile = chan.makefile('rU')

    def wait_for_comm(self):
        """
        Host blocks until guest communicates with it. It returns the message obtained from guest.
        :return:
        """
    pass

    def recvFile(self):
        # First, recieve the size...
        size = self.chanfile.readline() # stripping '\n\r' is unnecessary
        fileData = self.chanfile.read(int(size))
        # Recieved file just fine? ACK. TODO might want to check actual size, and perhaps also request hash to check.
        self.host.send(ACK)
        return fileData

    def sendFile(self, filename):
        file = open(filename, 'r')
        file.read()
        size = file.tell()
        file.seek(0)
        # First, send the size...
        self.chan.send(str(size) + '\r\n') # '\n\r' so guest can recognize endline. (obtained through readLine)
        # Now send the file's data!
        self.chan.send(file.read())
        # Wait for response... could be an ACK. could be a NCK.
        response = self.chanfile.readlines()
        return response


class ClientProtocol(Protocol):

    def __init(self, chan:Channel):
        super().__init__(chan)

    def listen(self):
        """client listens for instructions from server and executes them subsequently"""
        line = self.chanfile.readlines().strip('\r\n')
        argv = line.split(' ')
        # todo debug
        print(argv)


    pass


class ServerProtocol(Protocol):

    def __init(self, chan:Channel):
        super().__init__(chan)

    def requestFile(self, filename):
        cmd = "requestFile %s\r\n" % (filename)
        self.chan.send(cmd)
        # get back file...
        fileData = self.recvFile()
        return fileData


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