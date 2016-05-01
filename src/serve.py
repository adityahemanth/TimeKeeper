#!/usr/bin/python           # This is server.py file
import socket               # Import socket module
import time

#global vars
clock = 0;

#opening sockets with clients

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = input("port : ")                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

while True:
	c, addr = s.accept()     # Establish connection with client.
	print 'Got connection from', addr
	c.send('Requesting mode')
	rep = c.recv(1024)

	if(rep == "Keep alive"):
		c.send("200")
		rep = c.recv(1024)
		
		while True:
			if(rep == "kill"):
				print "Killing connection"
				c.close
				break

			else:
				c.send("waiting")
				rep  = c.recv(1024)
				print rep


	else:
		print("terminating connection")
		c.close()                # Close the connection