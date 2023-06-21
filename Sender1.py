# Mostafa Ibrahim S2456656
import sys
from socket import *
import math
import time

#parse arguments (host IP, Port number, File name)
IP = sys.argv[1]
PORT = int(sys.argv[2])
fileName = sys.argv[3]

#create socket
senderSocket = socket(AF_INET, SOCK_DGRAM)
#Load the data to be sent
with open(fileName, 'rb') as file:
	f = file.read()
	byteArr = bytearray(f)

#configure packet
sequenceN = 0
EOF = 0
#number of 1KB packets
numofPackets = math.floor(len(byteArr)/1024)
#remaining bytes < 1KB 
remainingBytes = len(byteArr)%1024
#loop to send packets
for p in range(numofPackets):
	if remainingBytes == 0 & p == numofPackets-1:
		EOF = 1

	#add the 2B sequence number to header
	packet = bytearray(sequenceN.to_bytes(2,byteorder = 'big'))
	#add EOF byte to header
	packet.append(EOF)
	#add data to the packet
	packet.extend(byteArr[p*1024: (p+1)*1024])
	#send the packet
	senderSocket.sendto(packet, (IP, PORT))
	sequenceN+=1
if(remainingBytes):
	sequenceN+=1
	#add the 2B sequence number to header
	packet = bytearray(sequenceN.to_bytes(2,byteorder = 'big'))
	#add EOF byte to header
	EOF = 1
	packet.append(EOF)
	#add data to the packet
	packet.extend(byteArr[numofPackets*1024: (numofPackets*1024)+remainingBytes])
	#send the packet
	senderSocket.sendto(packet, (IP, PORT))
#close socket
senderSocket.close()
