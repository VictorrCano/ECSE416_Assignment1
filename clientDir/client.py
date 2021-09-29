import socket
import sys
from datetime import datetime

# Default settings VVV
HEADER = 64
PORT = 5050
DISCONNECT_MESSAGE = "!DISCONNECT"
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())
#SERVER = "192.168.56.1"
TIMEOUT = 5


# Reading arguments + assignment them VVV
arguments = []

if len(sys.argv) > 4:
    raise Exception('Invalid format, use the following format: python client.py [-port] [-filename] [-timeout]')
elif len(sys.argv) == 2:
    arguments.append(sys.argv[1])
elif len(sys.argv) == 3:
    arguments.append(sys.argv[1])
    arguments.append(sys.argv[2])
elif len(sys.argv) == 4:
    arguments.append(sys.argv[1])
    arguments.append(sys.argv[2])
    arguments.append(sys.argv[3])


if len(arguments) == 1:
    PORT = int(arguments[0])

if len(arguments) == 2:
    PORT = int(arguments[0])
    FILENAME = arguments[1]

if len(arguments) == 3:
    PORT = int(arguments[0])
    FILENAME = arguments[1]
    TIMEOUT = int(arguments[2])

ADDR = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
print("Connection: OK")


def sendDecoded(msg):
    message = msg.encode(FORMAT)
    client.send(message)

if FILENAME != None:
    sendDecoded(FILENAME)

    print("Request message sent.")

    fileType = FILENAME.split(".")

    if fileType[1] == "jpg":
        filetypeString = "Content-Type: jpg/html"
    else:
        filetypeString = "Content-Type: text/html"


    filex_response = client.recv(4096).decode(FORMAT)
    print("Server HTTP Response: " + filex_response)
    

    if filex_response == "HTTP 404 Not Found":
        print("404 Not Found")
        print("Socket closed")
        client.close()
    
    else:
        #header = client.recv(334491)
        filex_data = client.recv(334491)

        if filetypeString == "Content-Type: jpg/html":
            print(filetypeString)
            with open(FILENAME, 'wb') as outF:
                outF.write(filex_data)
        else:
            print(filetypeString)
            print(filex_data.decode(FORMAT))
            print("Socket closed")

    client.close()

