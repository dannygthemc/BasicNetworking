#server application which connects to client and responds to 
#queries for Date and Time data
#allows for multiple clients in sequence, but one at a time
#must be killed manually

import socket #provides Socket libraries
import time #provides Date and Time libraries
from threading import *

TCP_IP = '192.168.118.129'
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

#defines a threading class
class client(Thread):
	#constructor
	def __init__(self, socket, address):
		Thread.__init__(self)
		self.sock = socket
		self.addr = address
		self.start()
	#main func
	def run(self):
		#until Client sends 'exit' signal, maintains connection
		#and receives queries
		while 2:
			recText = self.sock.recv(1024).decode() #get qeuerey
			print(recText) #print it
			#get current date and time incase queried for it
			timeText = ("Current Date and Time - " + 
					time.strftime("%m/%d/%Y") + 
					" " + time.strftime("%H:%M:%S") )
			#if 'exit' command received
			if recText == "exit":
				#notify end of connection
				print("Client has ended connection")
				print("awaiting new client")
				#send Client 'end' to signify end of transmision
				self.sock.send("end".encode())
				break
			#if queried for date and time, send it
			elif recText == "What is the current date and time?":
				self.sock.send(timeText.encode())
				self.sock.send("end".encode())
			#for anything else, send Invalid Request error
			else:
				self.sock.send("Error: Invalid Request".encode())
				self.sock.send("end".encode())

#listens for Clients
s.listen(5)
print("awaiting Client")
#connects to Clients, runs thread to handle them, runs loop to await other clients
while 1:
	conn, addr = s.accept()
	print('Server Address:', TCP_IP)
	print('Client Address:', addr)
	print("Connection to Client Established")
	#runs a thread on the given connection
	client(conn, addr)

s.shutdown(1)
s.close
