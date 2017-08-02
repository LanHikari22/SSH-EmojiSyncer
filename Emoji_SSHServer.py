import paramiko
from paramiko import AUTH_FAILED
from paramiko.py3compat import u, decodebytes
from binascii import hexlify
import socket
import sys
import traceback
import threading

# from protocol import ServerProtocol

class Emoji_SSHServer:

    class Server(paramiko.ServerInterface):
        """
        Inner class that provides the paramiko server interface for authenticating the client
        """

        # 'data' is the output of base64.b64encode(key)
        # (using the "user_rsa_key" files)
        data = (b'AAAAB3NzaC1yc2EAAAABIwAAAIEAyO4it3fHlmGZWJaGrfeHOVY7RWO3P9M7hp'
                b'fAu7jJ2d7eothvfeuoRFtJwhUmZDluRdFyhFY/hFAh76PJKGAusIqIQKlkJxMC'
                b'KDqIexkgHAfID/6mqvmnSJf0b5W8v5h2pI/stOSwTQ+pxVhwJ9ctYDhRSlF0iT'
                b'UWT10hcuO4Ks8=')
        good_pub_key = paramiko.RSAKey(data=decodebytes(data))

        def __init__(self):
            self.event = threading.Event()

        def check_channel_request(self, kind, chanid):
            if kind == 'session':
                return paramiko.OPEN_SUCCEEDED
            return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        def check_auth_password(self, username, password):
            if (username == 'lan') and (password == 'admin'):
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED

        def check_auth_publickey(self, username, key):
            print('Auth attempt with key: ' + u(hexlify(key.get_fingerprint())))
            if (username == 'lan') and (key == self.good_pub_key):
                return paramiko.AUTH_SUCCESSFUL
            return paramiko.AUTH_FAILED


        def get_allowed_auths(self, username):
            return 'password, publickey'

        def check_channel_shell_request(self, channel):
            self.event.set()
            return True

        def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                      pixelheight, modes):
            return True

    # port number to bind to
    _port = 0
    # hostkey of server
    _hostkey = None

    def __init__(self, port=2222):
        self._port = port
        self._hostkey = self._setup_hostkey() # sets up private key for the server so that it can decode public key comm?

    def start_server(self):
        """
        Configures paramiko server and listens to clients and serves it gladly!
        :return: None!
        """
        # TODO [Lan]
        # TODO consider haing this run after client disconnects? ran into an exception doing that.
        # TODO Socket exception: Bad file descriptor (9). Even though I did reinit the socket each time?
        # TODO possible mistake, or it was accessed in some way I did not notice.

        server = self.Server()
        client, addr = self._connect() # listens for a connection and accepts a client
        # set up transport
        transport = paramiko.Transport(client)
        transport.add_server_key(self._hostkey)
        transport.start_server(server=server)
        # authenticate
        chan = self._authClient(transport=transport)
        # Setting up protocol for communication with channel.
        # protocol = ServerProtocol(chan)
        # Authenticated! Use the channel however you like :)

        # event is its own thread, and it's vital to continued communication with the client... :0
        # TODO [investigation] event and its importance and role
        # server.event.wait(10)
        # if not server.event.is_set():
        #     print('*** Client never asked for a shell.')
        #     client.close()
        #     sys.exit(1)


        chan.send('\r\n\r\nWelcome to my dorky little BBS!\r\n\r\n')
        chan.send('We are on fire all the time!  Hooray!  Candy corn for everyone!\r\n')
        chan.send('Happy birthday to Robot Dave!\r\n\r\n')
        chan.send('Username: ')


        f = chan.makefile('rU')
        username = f.readline().strip('\r\n')
        print(username)

        chan.send('\r\nI don\'t like you, ' + username + '.\r\n')

        # bye bye client!
        chan.close()
        client.close()
        print("Connection closed.")





    @staticmethod
    def _setup_hostkey():
        hostkey = paramiko.RSAKey(filename="test_rsa.key")
        print('Read key: ' + u(hexlify(hostkey.get_fingerprint())))
        return hostkey

    def _connect(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self._port))
        except Exception as e:
            print('*** Bind failed: ' + str(e))
            sys.exit(1)
        try:
            sock.listen(100)
            print('Listening for connection ...')
            client, addr = sock.accept()
        except Exception as e:
            print('*** Listen/accept failed: ' + str(e))
            sys.exit(1)
        print('Got a connection!')
        return client, addr

    @staticmethod
    def _authClient(transport:paramiko.Transport):
        chan = transport.accept(20) # 20
        if chan is None:
            print('*** No channel.')
            sys.exit(1)
        print("Authenticated!")
        return chan