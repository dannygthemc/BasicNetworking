#Client application to querey server for Time and Date info
#Uses Python3
#type 'What is current date and time?' to querey server
#type 'exit' to close client
#any other input will receive an 'Ivalid Request Error' from server
#waits for 'end' signal from Server to stop waiting for input

import socket

TCP_IP = '192.168.118.129' #Server IP
TCP_PORT = 5005	#Server Port

print ("Attempting to contact server at ",TCP_IP,":",TCP_PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates socket
s.connect((TCP_IP, TCP_PORT))	#connects
print ("Connection to Server Established")

#a function that defines interactions with server
def send(str):
	#send message
	s.send(str.encode()) 
	data = ''
	#receive message back
	#continues receiving until 'end' is received
	while 2:
		data = s.recv(1024).decode()
		#print back received message
		print (data)
		if data == "end":
			break #break out of the loop

#allows user to continue querying server until they type 'exit'
while 1:
	print("Type 'What is the current date and time?' to receive date and time from server")
	print("type 'exit' to close client")
	text = input('Enter your command: ')
	send(text)
	if text == "exit":
		break
#shutsdown and closes Client	
s.shutdown(1)
s.close()
