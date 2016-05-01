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


