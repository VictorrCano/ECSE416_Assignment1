import socket
import threading
import sys

PORT = 5050
# HEADER is first message sent by client warning server of size of incoming message
# header message fixed at 64 bytes
# padding after number representing size of incoming message, padded up to 64
HEADER = 64
# SERVER = "192.168.56.1"
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

if len(sys.argv) > 2:
    raise Exception('Invalid format, use the following format: python client.py [-port] [-filename] [-timeout]')
elif len(sys.argv) == 2:
    PORT = int(sys.argv[1])

ADDR = (SERVER, PORT)

# print(SERVER)
print(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected.")
    connected = True
    while connected:
        # blocking line of code VVV so run handle_client in individual threads
        # first we receive header
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            # block again until actual message is sent (body not header)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f"[{address}] {msg}")

    connection.close()


def begin():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        # blocking line of code VVV
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting...")
begin()
