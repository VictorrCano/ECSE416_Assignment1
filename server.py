import socket
import threading
import sys
import os

PORT = 5050
# HEADER is 5050first message sent by client warning server of size of incoming message
# header message fixed at 64 bytes
# padding after number representing size of incoming message, padded up to 64
HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

if len(sys.argv) > 2:
    raise Exception('Invalid format, use the following format: python client.py [-port] [-filename] [-timeout]')
elif len(sys.argv) == 2:
    PORT = int(sys.argv[1])



# print(SERVER)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', int(PORT)))
server.listen(PORT)


while True:
    connection, address = server.accept()
    print("Connection: OK")


    msg = connection.recv(4096).decode(FORMAT)
    if msg:
        print("Request message recieved.")
        # block again until actual message is sent (body not header)
    
        if os.path.isfile(msg):
            connection.send("HTTP 200 OK".encode(FORMAT))
        else:
            connection.send("HTTP 404 Not Found".encode(FORMAT))

        #f = open(msg, "rb")
        #file_data = f.read()

        with open(msg, 'rb') as f:

            file_data = f.read()
            try:
                connection.send(file_data)
            except:
                connection.send("HTTP 500 Internal Server Error".encode(FORMAT))

    connection.close()

