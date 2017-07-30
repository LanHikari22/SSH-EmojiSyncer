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
    # paramiko SSHClient
    _client = None

    ##
    # Initializes client address and authentication data as  well as paramiko client.
    # It loads system host keys. An exception will be thrown if trying to connect to an unregistered host.
    ##
    def __init__(self, host=None, port=22, username=None, password=None):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()


    ##
    # Connects to given address using given authentication data.
    ##
    def connect(self):
        self._client.connect(self._host, self._port, self._username, self._password)

    def pull(self):
        pass

    def push(self):
        pass

    def clone(self):
        pass

    def set_address(self, host, port=22):
        self._host = host
        self._port = port

    def set_authentication(self, username, password):
        self._username = username
        self._password = password