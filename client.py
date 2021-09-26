import socket
import sys

# Default settings VVV
HEADER = 64
PORT = 8080
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.56.1"
TIMEOUT = 5


# Reading arguments + assignment them VVV
arguments = []

if len(sys.argv) > 4:
    raise Exception('Invalid format, use the following format: python client.py [-port] [-filename] [-timeout]')
elif len(sys.argv) == 3:
    arguments.append(sys.argv[1])
    arguments.append(sys.argv[2])
elif len(sys.argv) == 4:
    arguments.append(sys.argv[1])
    arguments.append(sys.argv[2])
    arguments.append(sys.argv[3])


if len(arguments) == 2:
    PORT = int(arguments[1])

if len(arguments) == 3:
    PORT = int(arguments[1])
    FILENAME = arguments[2]

if len(arguments) == 4:
    PORT = int(arguments[1])
    FILENAME = arguments[2]
    TIMEOUT = int(arguments[3])

ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


send("Hello!")
send(DISCONNECT_MESSAGE)
