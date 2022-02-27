# ############ Michael David 212679567 and Yahel Orgad 325010809 #############

import socket
import json
import time
FORMAT = 'utf-8'

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

while True:
    msg = ClientSocket.recv(1024)
    print(msg.decode(FORMAT))
    if "game over" in msg.decode(FORMAT):
        ClientSocket.close()
        break
    if msg.decode(FORMAT) == "Client chose to quit":
        ClientSocket.close()
        break
    if msg.decode(FORMAT) == "can't have more than 5 players":
        ClientSocket.close()
        break
    else:
        msg2 = input()
        ClientSocket.send(msg2.encode())