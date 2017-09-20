import binascii
import socket
import struct
import sys
import hashlib
from socket import timeout

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
Rec_PORT = 5004

ACK = 0 #ACK always 0 for sender
SEQ = 0 #SEQ starts at 0 for sender

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

#defines unpacker for ACK pack
unpacker = struct.Struct('I I')

#creates separate sockets for sending receiving
send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#listens on the receiving socket and sets a timeout
rec_sock.bind((UDP_IP, Rec_PORT))
rec_sock.settimeout(0.009)

#builds and returns a UDP packet for the given data
def buildPack(Ack, Seq, data):
	
	s = data.encode()
	#Create the Checksum
	values = (Ack,Seq,s)
	UDP_Data = struct.Struct('I I 8s')
	packed_data = UDP_Data.pack(*values)
	chksum =  bytes(hashlib.md5(packed_data).hexdigest(), 	encoding="UTF-8")

	#Build the UDP Packet
	values = (Ack,Seq,s,chksum)
	UDP_Packet_Data = struct.Struct('I I 8s 32s')
	UDP_Packet = UDP_Packet_Data.pack(*values)
	print ("Sending Packet:", Ack, Seq, s, chksum)
	return UDP_Packet;

#used to send the given UDP_Packet and check the returned #ACK_packet
def sendUDP(UDP_Packet, ACK, SEQ):
	ack_received = False

	#sends UDP packet and awaits acknowledgement packet
	#if nothing received before timeout or wrong SEQ number
	#received, repeats the send
	while not ack_received:
		#Send the UDP Packet
		send_sock.sendto(UDP_Packet, (UDP_IP, UDP_PORT))

		try: #wait for message from receiver
			data, addr = rec_sock.recvfrom(1024)
		except timeout: #if timeout reached, stop waiting
			print ("Timer Expired, Packet lost, resending previous")
		else: #otherwise, check what was received
			ACK_Packet = unpacker.unpack(data)
			print ("received Ack Pack:", ACK_Packet)
			#if SEQ numbers match, exit loop
			if ACK_Packet[1] == SEQ:
				print ("Correct Ack Received")
				ack_received = True 
			else: #otherwise, resend
				print("Incorrect Ack, resending previous package")

#main method
#creates packets with given data and sends them to the receiver
data = "NCC-1701"
UDP_Packet = buildPack(ACK, SEQ, data)
sendUDP(UDP_Packet, ACK, SEQ)

SEQ = SEQ ^ 1 #changes SEQ 

data = "NCC-1664"
UDP_Packet = buildPack(ACK, SEQ, data)
sendUDP(UDP_Packet, ACK, SEQ)

SEQ = SEQ ^ 1 #changes SEQ 

data = "NCC-1017"
UDP_Packet = buildPack(ACK, SEQ, data)
sendUDP(UDP_Packet, ACK, SEQ)

rec_sock.shutdown(1)
send_sock.shutdown(1)
send_sock.close()
rec_sock.close()
