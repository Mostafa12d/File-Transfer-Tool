#Mostafa Ibrahim S2456656
import sys
from socket import *
import struct
from enum import Enum
import math
import time
import os

IP = '127.0.0.1'
PORT = int(sys.argv[1])
fileName = sys.argv[2]
windowSize = int(sys.argv[3])
receiverSocket = socket(AF_INET, SOCK_DGRAM)
receiverSocket.bind((IP,PORT))
byteArr = bytearray()


base = 0
last = base + windowSize -1 # last packet in the window base + window size - 1
lastR=False #bool to check if last packet was received
#recBuffer =[None]*windowSize #buffer for received packets not yet acked
received=[0]*windowSize #list of received packets in the window
while True:
  #print("waiting to receive")
  message, received_address = receiverSocket.recvfrom(1027)
  if message == None:
      continue
  #print("received something")
  if message[2]:
      break
  currentSeq = int.from_bytes(message[:2],byteorder='big')
  if currentSeq < base:
      byteArr.extend(message[3:])
      ACK_pkt = bytearray(currentSeq.to_bytes(2, byteorder='big'))
      receiverSocket.sendto(ACK_pkt, received_address)
  else:
    if currentSeq >= base and currentSeq <= last:
        if currentSeq == base:
            received[base%windowSize] = 0
            #recBuffer[base%windowSize] = None
            base +=1
            last +=1
        elif received[currentSeq%windowSize] == 0:
            received[currentSeq%windowSize]=1
            recBuffer[currentSeq%windowSize]=message[3:]
        byteArr.extend(message[3:])

      ACK_pkt = bytearray(currentSeq.to_bytes(2, byteorder='big'))
      receiverSocket.sendto(ACK_pkt, received_address)
#byteArr = bytearray(recBuffer)
with open(fileName, 'wb') as f:
  f.write(byteArr)
receiverSocket.close()
