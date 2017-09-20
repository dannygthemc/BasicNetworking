import binascii
import socket
import struct
import sys
import hashlib

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

#holds data to be transfered
dataList = ['NCC-1701', 'NCC-1664', 'NCC-1017'];

#ACK is always 0 for client
ACK = 0
#SEQ starts at 0
SEQ = 0
#used for looping
x = 0

#send start signal
sock.sendto(b'0', (UDP_IP, UDP_PORT))
#wait for confirmation signal
##while 1:
##	print('waiting for confrimation signal')
##	temp = sock.recv(1024) # buffer size is 1024
##	print(temp.decode() )
##	if temp.decode() == "0":
##		break;

#once confrimation signal received
#for each piece of data
#tries to send
#if Acknowledgment pack from Server has wrong SEQ digit
#doesn't increment loop and resends same packet
#if Acknowledgment pack from Server has correct SEQ digit
#increments and sends nextpacket with next bit of data
while (x < 3):

	s = dataList[x].encode()
	#Create the Checksum
	values = (ACK,SEQ,s)
	UDP_Data = struct.Struct('I I 8s')
	packed_data = UDP_Data.pack(*values)
	chksum =  bytes(hashlib.md5(packed_data).hexdigest(), 	encoding="UTF-8")

	#Build the UDP Packet
	values = (ACK,SEQ, s ,chksum)
	UDP_Packet_Data = struct.Struct('I I 8s 32s')
	UDP_Packet = UDP_Packet_Data.pack(*values)

	#Send the UDP Packet
	sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))
	sock.sendto(b'end', (UDP_IP, UDP_PORT))
	#Get Acknowledgment pack from Server
	while 2:
		print('awaiting Acknowledgment pack')
		data = sock.recv(1024) # buffer size is 1024
		ACK_Pack = unpacker.unpack(data)
		print("received message:", ACK_Pack)

		#If SEQ bit is the same
		#increments loop to send next packet
		#Switches SEQ bit to indicate progression
		if UDP_Packet[1] == SEQ:
			x = x + 1
			SEQ = SEQ ^ 1
			break;
		#otherwise, does nothing
		#repeats loop with same variables
		else:
			break;	

#once all three pieces of data have been received
#send completed signal
#Build the final UDP Packet
values = (ACK,SEQ,b'fin', 0)
UDP_Packet_Data = struct.Struct('I I 8s 32s')
UDP_Packet = UDP_Packet_Data.pack(*values)
#if 'fin' received on Server, stops querying socket for more data
#shutsdown and closes Client	
s.shutdown(1)
s.close()












