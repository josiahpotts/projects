#Author: Josiah Potts
#Date: 3/18/23
#Description: Client side operations for Python Socket client-server chat functionality.

from socket import *

#Create the socket and set host and port number
clientSocket = socket(AF_INET, SOCK_STREAM)
host = 'localhost'
port = 10100

#Connect to host
clientSocket.connect((host, port))
print(f"Connectied to: {host}, on port: {port} \nType /q to quit \nEnter a message...")

#Client starts conversation and then listens
while True:

    message = input(">")
    if message == "":
        message = "<empty>"

    clientSocket.send(message.encode('utf-8'))
    data = clientSocket.recv(1024).decode('utf-8')

    if not data:
        break
    elif data == "/q":
        break

    print(f"SERVER: {data}")

clientSocket.close()
