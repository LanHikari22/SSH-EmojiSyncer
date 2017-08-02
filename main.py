##
# main module
# Creator: Lan
# Date Created: 7/29/17
# Call this and supply commands in order to activate the program's functionality.
##
import os, sys, getpass
from Emoji_SSHClient import Emoji_SSHClient
from Emoji_SSHServer import Emoji_SSHServer
import paramiko


# TODO data to put inside a .ini or .confg file
USER = 'lan' # obtain automatically, no need to be input
PATH =  '/home/%s/Desktop' % (USER)
FOLDER_NAME = 'Characters'
PORT = 2200
KEY_FILENAME='user_rsa.key'

# start_client functions
CLIENT_PUSH = 0
CLIENT_PULL = 1

def execute(argv):
    """"Executes command parsed from args passed to program. """
    cmd = argv[1]
    if cmd == 'help':
        print("Available commands: 'push <hostname>', 'pull <hostname>', and 'start_server'")
    elif cmd == 'push' and len(argv) == 3:
        start_client(function=CLIENT_PUSH, hostname=assertValidHost(argv[2]))
    elif cmd == 'pull' and len(argv) == 3:
        start_client(function=CLIENT_PULL, hostname=assertValidHost(argv[2]))
    elif cmd == 'start_server' and len(argv) == 2:
        start_server()
    else:
        print("Incorrect usage. Please supply help as an argument as such for usage information: '<progName> help'")

def assertValidHost(hostname):
    """
    Ensures that the passed hostname is valid If not, it tells the user and exits the program.
    :returns: hostname if valid, else it wont return. this program will cease execution :(
    """
    return hostname # todo verify? or just wait for the program to crash somewhere down the line???


def start_client(function:int, hostname):
    """
    Initiates the client to perform what it was born to perform. To a better emoji world, comrades!
    :param function: specifies what functionality the client is initiated to perform. Check out the CLIENT_x consts.
    :param hostname: hostname to connect to and perform emoji magic with.
    :return: Nothing. Nada. Null. None. Have a nice day!
    """
    # password = getpass.getpass('Please input password: ') # only invisible echo in actual terminal, not IDLE-like env..
    # TODO ^ if false, then authenticationis automatically closed. Prefer to be asked for password later on
    client = Emoji_SSHClient(host=hostname,port=PORT,username=USER,password=None, keyfilename=KEY_FILENAME)
    client.connect()

    try:
        pass # TODO debug
        # client.connect() # [Lan]: TODO when accounting for private key, no exception is raised upon failed auth :o
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("\nUnfortunately, we could not connect... You sure the server is up? Double-checked your password?")
        print("Exiting...")
        sys.exit(1)
    except paramiko.ssh_exception.AuthenticationException:
        print('\nI could not authenticate you... Yikes, a hacker?! Please don\'t hack me!! ><""')
        print("Exiting (Running away)...")

    # perform specified function
    if function == CLIENT_PUSH:
        client.push()
    elif function == CLIENT_PULL:
        client.pull()
    else:
        print("Why are you here? You shouldn't ever see this! :T")



def start_server():
    import demo_server
    print('start_server()' )
    server = Emoji_SSHServer(port=PORT) # todo should have access to config file?
    server.start_server()

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Incorrect usage. Please supply help as argument as such '<progName> help'")
        sys.exit(1)
    execute(argv)
    sys.exit(0)