# Mostafa Ibrahim S2456656
import sys
from socket import *
import select
import math
import time
import os

#parse arguments (host IP, Port number, File name, timeout, window size)
IP = sys.argv[1]
PORT = int(sys.argv[2])
fileName = sys.argv[3]
timeOut = int(sys.argv[4])
windowSize = int(sys.argv[5])

#configure socket
senderSocket = socket(AF_INET, SOCK_DGRAM)
#configure the socket to be non-blocking
senderSocket.setblocking(0)
#open file and create a byte array of the data
with open(fileName, 'rb') as file:
	f = file.read()
	byteArr = bytearray(f)

sequenceN = 0
EOF = 0


#retransmission counter
retransmissions = 0
#number of 1KB packets
numofPackets = int(len(byteArr)/1024)
#remaining bytes < 1KB 
remainingBytes = len(byteArr)%1024
lastseqN = numofPackets if not remainingBytes else numofPackets + 1
base = -1
nextseqN = 1
#start timer
start_time = time.perf_counter()
while base != lastseqN:
	while sequenceN <= windowSize + base and sequenceN <= lastseqN:
		#set indices of packet
		end = (sequenceN+1)*1024
		start = sequenceN*1024
		if sequenceN == lastseqN:
			if remainingBytes != 0:
				end = (numofPackets*1024)+remainingBytes
			EOF = 1
		else:
			EOF = 0
		#bytearray is used to enure correct packet format
		packet = bytearray(sequenceN.to_bytes(2,byteorder = 'big'))
		#add EOF byte to header
		packet.append(EOF)
		#add data to the packet
		packet.extend(byteArr[start:end])
		#send the packet
		try:
			senderSocket.sendto(packet, (IP, PORT))
		except error:
			select.select([],[senderSocket],[])
		sequenceN +=1
	ACKseq = -1
	try:
		while (base >= ACKseq):
			senderSocket.settimeout(timeOut/1000)
			ACK, address = senderSocket.recvfrom(2)
			ACKseq = int.from_bytes(ACK[:2], 'big')
		#set the base to the latest ack sequence number
		base = ACKseq
	except error as exc:
		sequenceN = base+1
		retransmissions+=1

end_time = time.perf_counter()
timeTaken = end_time - start_time
file_KB = len(byteArr)/1000
throughput = file_KB/timeTaken
print("{}".format(throughput))
senderSocket.close()
