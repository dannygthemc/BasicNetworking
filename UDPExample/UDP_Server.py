import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
unpacker = struct.Struct('I I 8s 32s')
#ACK is always 1 for Server
ACK = 1
#SEQ starts at 1 for Server
#changes to match starting bit of Client only if not corrupt
SEQ = 1
#Create the socket and listen
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

#Receive Data
def rec(SEQ):
    #Sends confirmation code 0 to start sending
    sock.sendto(b'0', (UDP_IP, UDP_PORT))
    print('made it to receiving loop')    
    data1 = b'101'
    data2 = b'101'
    while 2:
        data1 = sock.recv(1024) # buffer size is 1024
        data2 = sock.recv(1024) # buffer size is 1024
        if data2.decode() == "end":
            break; 
    UDP_Packet = unpacker.unpack(data1)
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
        #doesn't change Seq
    
    #creates Acknowledgment Packet to send back to Client
    print('made it here')
    values = (ACK,SEQ,b'test', chksum)
    ACK_Packet_Data = struct.Struct('I I 8s 32s')
    ACK_Packet = ACK_Packet_Data.pack(*values)

    #Send the ACK Packet
    sock.sendto(ACK_Packet, (UDP_IP, UDP_PORT))
    print('made it here too')

#Server runs until manually closed
while 1:
	#gets data from Client
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print("received from:", addr)
	print("received message:", data.decode() )
	data = data.decode() 
	#if received start code 0, start receiving code
	if data == "0":
		print('made it here')
		rec(SEQ)







