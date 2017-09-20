import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
Send_PORT = 5004
unpacker = struct.Struct('I I 8s 32s')

ACK = 1 #ACK always equals 1 for receiver
SEQ = 1 #SEQ starts at 1 for receiver
#creates separate socket for sending
send_sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#builds and returns an Ackowledgement packet
#with the given data
def buildACK(Ack, Seq):
	#Build the ACK Packet
	values = (Ack,Seq)
	ACK_Packet_Data = struct.Struct('I I')
	ACK_Packet = ACK_Packet_Data.pack(*values)
	return ACK_Packet;

#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
    #Receive Data
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    UDP_Packet = unpacker.unpack(data)
    print("received from:", addr)
    print("received message:", UDP_Packet)
    #Create the Checksum for comparison
    values = (UDP_Packet[0],UDP_Packet[1],UDP_Packet[2])
    packer = struct.Struct('I I 8s')
    packed_data = packer.pack(*values)
    chksum =  bytes(hashlib.md5(packed_data).hexdigest(), encoding="UTF-8")
    #Compare Checksums to test for corrupt data
    if UDP_Packet[3] == chksum:
        print('CheckSums Match, Packet OK')
        SEQ = SEQ ^ 1 #changes SEQ to match Client
    else:
        print('Checksums Do Not Match, Packet Corrupt')
    
    #Build and send an Acknowledgment Packet
    ACK_Packet = buildACK(ACK, SEQ)
    send_sock.sendto(ACK_Packet, (UDP_IP, Send_PORT))