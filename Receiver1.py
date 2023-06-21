# Mostafa Ibrahim S2456656
import sys
from socket import *

IP = "127.0.0.1"
PORT = int(sys.argv[1])
fileName = sys.argv[2]
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind((IP,PORT))
byteArr = bytearray()

while True:
	message, address = receiverSocket.recvfrom(1027)
	byteArr.extend(message[3:])
	if message[2]:
		break
with open(fileName, 'wb') as f:
    f.write(byteArr)
receiverSocket.close()