# Mostafa Ibrahim S2456656
import sys
from socket import *
import math
import time
import os

IP = '127.0.0.1'
PORT = int(sys.argv[1])
fileName = sys.argv[2]
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind((IP,PORT))
byteArr = bytearray()

#previous sequence number to check for duplicates
previousSeq = 0


while True: 
	message, received_address = receiverSocket.recvfrom(1027)
	if message is None:
		continue
	currentSeq = int.from_bytes(message[:2],byteorder='big')
	if currentSeq == previousSeq+1:
		previousSeq = currentSeq
		byteArr.extend(message[3:])
		ACK_pkt = bytearray(previousSeq.to_bytes(2, byteorder ='big'))
		receiverSocket.sendto(ACK_pkt, received_address)
	else:
		ACK_pkt = bytearray(previousSeq.to_bytes(2, byteorder='big'))
		receiverSocket.sendto(ACK_pkt, received_address)
	if message[2]:
		last = 0
		ACK_pkt = bytearray(last.to_bytes(2, byteorder='big'))
		receiverSocket.sendto(ACK_pkt,received_address)
		break
with open(fileName, 'wb') as f:
	f.write(byteArr)
receiverSocket.close()

