import paramiko


class Emoji_SSHClient:
    # str for host to connect to
    _host = None
    # port number to connect to, Default=22
    _port = 22
    # username str for authentication
    _username = None
    # username password for authentication
    _password = None
    # private key for client. used for public key authentication
    _keyfilename = None
    # paramiko SSHClient
    _client = None

    ##
    # Initializes client address and authentication data as  well as paramiko client.
    # It loads system host keys. An exception will be thrown if trying to connect to an unregistered host.
    ##
    def __init__(self, host=None, port=22, username=None, password=None, keyfilename=None):
        self._host = host
        self._port = port
        self._username = username
        # self._password = password
        self._keyfilename = keyfilename
        self._client = paramiko.SSHClient()
        # self._client.load_system_host_keys()
        self._client.load_host_keys('known_hosts')
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ##
    # Connects to given address using given authentication data.
    ##
    def connect(self):

        # if self._keyfilename is not None:
        #     self._client.connect(self._host, self._port, self._username, self._password, key_filename=self._keyfilename)
        # else:
        #     self._client.connect(self._host, self._port, self._username, self._password)

        self._client.connect(self._host, self._port, self._username, key_filename=self._keyfilename)
        # t = self._client.get_transport()
        # chan = t.open_channel(kind='session',dest_addr=((self._host, self._port)))
        # print(bytes.decode(chan.recv(4096)))
        # chan.send("lan")
        # print(chan)

    def pull(self):
        pass

    def push(self):
        pass

    def clone(self):
        pass

    def set_address(self, host, port=22):
        self._host = host
        self._port = port

    def set_authentication(self, username, password=None, keyfilename=None):
        self._username = username
        self._password = password
        self._keyfilename = keyfilename