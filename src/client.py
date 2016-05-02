#!/usr/bin/python           # This is client.py file

from __future__ import print_function
import pickle
from message import *
from post import *
import socket               # Import socket module


def lookup( host, port):
	s = socket.socket() 
	conn = (host,port)

	msg = message("lookup", None)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)

	posts = pickle.loads(rcv)
	display(posts)


def postto(host, port):

	s = socket.socket() 
	conn = (host,port)

	u_id = raw_input("Enter User ID: ")
	pst = raw_input("Enter post: ")
	p = post(u_id, pst)

	msg = message("post", p)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)
	print(rcv)

def sync(host, port, current_Dc_no):
	dc_no = raw_input("Enter DataCenter ID: ")
	s = socket.socket() 
	conn = (host,port)

	if(dc_no != current_Dc_no):
		msg = message("sync_request", dc_no)
		send = pickle.dumps(msg,0)

		s.connect(conn)
		s.send(send)
		rcv = s.recv(4096)
		print(rcv)

	else:
		print("You cannot sync with your own DataCenter")

def getInfo(host, port):

	s = socket.socket() 
	conn = (host,port)

	msg = message("info", None)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)
	return int(rcv)

def display(posts):

	print("\n\n")
	for post in posts:
		print("User ID: ", end = "")
		print(post.getUID())

		print("Post: ", end = "")
		print(post.getPost())
		print("\n")


def main():

	ID = raw_input ("$ hostIP: ")
	port = raw_input("$ port: ")
	port = int(port)
	current_Dc_no = getInfo(ID, port)
	print("Connected to DataCenter: ", end = "")
	print(current_Dc_no)

	while True:

		ipt = raw_input("$ ")
		if(ipt == "lookup"):
			lookup(ID, port)

		elif(ipt == "post"):
			postto(ID, port)

		elif(ipt == "sync"):
			sync(ID, port, str(current_Dc_no))

		else:
			print("invalid input")



if __name__ == "__main__":
    main()




