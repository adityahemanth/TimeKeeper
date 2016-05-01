#!/usr/bin/python           # This is client.py file

import time
import random
import json
import threading
import socket               # Import socket module

port = 9999;


def insert(s,host,port):

	conn =  (host,port)
	key = raw_input("key: ")
	val = raw_input("val: ")

	if(key != "" and val != ""):
		pair = key + "<>" + val
		s.connect(conn)
		s.send(pair)
		print s.recv(1024)
		s.close()

	else:
		print("Invalid input")
		insert()

def delete(s,host,port):

	conn =  (host,port)
	key = raw_input("key: ")

	if(key != ""):
		s.connect(conn)
		s.send(key)
		print s.recv(1024)
		s.close()

	else:
		print("Invalid input")
		insert()


while True:
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	command = raw_input("$: ")

	if(command == 'insert'):
		insert(s,host,port)

	elif(command == 'delete'):
		delete(s,host,port)

	else:
		print("invalid input")
s.connect((host, port))
rep = s.recv(1024)
print rep
s.send ("Keep alive")

ans = s.recv(1024)
kill = 0

if(ans == "200"):
	print "successful"
	while True:
		r = random.randint(0,1)
		time.sleep(r)
		
		if(kill == 6):
			s.send("kill")
			print "Killing connection"
			s.close()
			break

		else:
			s.send("safe")

		print s.recv(1024)
		kill = random.randint(0,20)

else:
	print "400, unsuccessful"
	s.close()                     # Close the socket when done

