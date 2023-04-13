#Author: Josiah Potts
#Date: 3/18/23
#Description: Server side operations for Python Socket client-server chat functionality.

from socket import *

#Create socket and set host and port number for connection
serverSocket = socket(AF_INET, SOCK_STREAM)
host = 'localhost'
port = 10100

#Bind to the host and port and listen for a connection
serverSocket.bind((host, port))
serverSocket.listen(1)

print(f"Server listening on {host}:{port}")

#Accept connecting host
clientSocket, address = serverSocket.accept()
print(f"Connected by: ({address[0]}, {address[1]}) \nType /q to quit \nWaiting for message...")

#Wait for a message to be sent and then prompt to reply
while True:

    data = clientSocket.recv(1024).decode('utf-8')

    if not data:
        break
    elif data == "/q":
        break

    print(f"CLIENT: {data}")

    message = input(">")
    if message == "":
        message = "<empty>"

    clientSocket.send(message.encode('utf-8'))

clientSocket.close()
serverSocket.close()