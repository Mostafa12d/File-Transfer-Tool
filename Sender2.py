# Mostafa Ibrahim S2456656
import sys
from socket import *
import math
import time
import os

#parse arguments (host IP, Port number, File name, timeout)
IP = sys.argv[1]
PORT = int(sys.argv[2])
fileName = sys.argv[3]
timeOut = int(sys.argv[4])

#configure socket
senderSocket = socket(AF_INET, SOCK_DGRAM)
#Load the data to be sent
with open(fileName, 'rb') as file:
	f = file.read()
	byteArr = bytearray(f)

#configure packet
sequenceN = 0
EOF = 0
retrans = 0
#start timer
start = time.perf_counter()
#retransmission counter
retransmissions = 0
#number of 1KB packets
numofPackets = int(len(byteArr)/1024)
#remaining bytes < 1KB 
remainingBytes = len(byteArr)%1024

for p in range(numofPackets):
	#initialize ACK flags and sequence number
	ACKseq = 0
	correctACK = 0
	receivedACK = 0

	if remainingBytes == 0 & p == numofPackets-1:
		EOF = 1
	sequenceN+=1
	#add the 2B sequence number to header
	packet = bytearray(sequenceN.to_bytes(2,byteorder = 'big'))
	#add EOF byte to header
	packet.append(EOF)
	#add data to the packet
	packet.extend(byteArr[p*1024: (p+1)*1024])
	#send the packet
	senderSocket.sendto(packet, (IP, PORT))
	while (not correctACK):
		try:
			senderSocket.settimeout(timeOut/1000)
			ACK, address = senderSocket.recvfrom(2)
			ACKseq = int.from_bytes(ACK[:2], 'big')
			ReceivedACK = 1
		except timeout:
			ReceivedACK = 0
		if ReceivedACK == 1 and sequenceN == ACKseq:
			correctACK = 1
		else:
			senderSocket.sendto(packet, (IP,PORT))
			retransmissions += 1
	


#handle last packet
if(remainingBytes != 0):
	ACKseq = 0
	correctACK = 0
	receivedACK = 0
	EOF = 1
	#add the 2B sequence number to header
	packet = bytearray(sequenceN.to_bytes(2,byteorder = 'big'))
	#add EOF byte to header
	packet.append(EOF)
	#add data to the packet
	packet.extend(byteArr[numofPackets*1024: (numofPackets*1024)+remainingBytes])
	#send the packet
	senderSocket.sendto(packet, (IP, PORT))
	sequenceN+=1

	while (not correctACK):
		try:
			senderSocket.settimeout(timeOut/1000)
			ACK, senderAddress = senderSocket.recvfrom(2)
			ACKseq = int.from_bytes(ACK[:2], 'big')
			ReceivedACK = 1
			if  ACKseq == 0:
				break
		except timeout:
			ReceivedACK = 0
		if sequenceN == ACKseq and ReceivedACK == 1:
			correctACK = 1
		else:
			senderSocket.sendto(packet, (IP, PORT))
			retransmissions += 1

end = time.perf_counter()
timeTaken = end - start
file_KB = len(byteArr)/1000
throughput = file_KB/timeTaken
print("{} {}".format(retransmissions, throughput))
senderSocket.close()

