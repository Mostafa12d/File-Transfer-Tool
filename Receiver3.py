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
nextseqN = 0
previousseqN = 0

while True: 
	message, received_address = receiverSocket.recvfrom(1027)
	EOF = message[2]
	# byteArr.extend(message[3:])
	if message is not None:
		currentSeq = int.from_bytes(message[:2],byteorder='big')
		if currentSeq == nextseqN:
			#previousSeq = currentSeq
			byteArr.extend(message[3:])
			nextseqN+=1
		if nextseqN == 0:
			previousSeqN = 0
		else:
			previousSeqN = nextseqN-1
		ACK_pkt = bytearray(previousSeqN.to_bytes(2, byteorder='big'))
		receiverSocket.sendto(ACK_pkt, received_address)
		while nextseqN != currentSeq +1:
			message, received_address = receiverSocket.recvfrom(1027)
			currentSeq = int.from_bytes(message[:2],'big')
			if currentSeq == nextseqN:
				byteArr.extend(message[3:])
				nextseqN +=1
			if nextseqN == 0:
				previousSeqN = 0
			else:
				previousSeqN = nextseqN-1
			ACK_pkt = bytearray(previousSeqN.to_bytes(2, byteorder='big'))
			receiverSocket.sendto(ACK_pkt, received_address)

		if EOF:
			ACK_pkt = bytearray(currentSeq.to_bytes(2, byteorder='big'))
			receiverSocket.sendto(ACK_pkt,received_address)
			break
with open(fileName, 'wb') as f:
	f.write(byteArr)
receiverSocket.close()