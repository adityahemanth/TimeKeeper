#!/usr/bin/python           # This is client.py file

import pickle, message
import socket               # Import socket module


def lookup(self, host, port):
	s = socket.socket() 
	conn = (host,port)

	msg = message("lookup", None)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)

	posts = pickle.loads(rcv)
	display(posts)


def post(self, host, port):

	u_id = input("Enter User ID: ")
	pst = input("Enter post: ")
	p = post(u_id, pst)

	msg = message("post", p)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)
	print(rcv)

def sync(self, host, port, current_Dc_no):
	dc_no = input("Enter DataCenter ID: ")

	if(dc_no != current_Dc_no):
		msg = message("sync_request", dc_no)
		send = pickle.dumps(msg,0)

		s.connect(conn)
		s.send(send)
		rcv = s.recv(4096)
		print(rcv)

	else:
		print("You cannot sync with your own DataCenter")

def getInfo(self, host, port):

	msg = message("info", None)
	send = pickle.dumps(msg,0)

	s.connect(conn)
	s.send(send)
	rcv = s.recv(4096)
	return int(rcv)

def display(posts):

	for post in posts:
		print("User ID: ", end = "")
		print(post.getUID())

		print("Post: ", end = "")
		print(post.getPost())
		print("\n\n")


def main():

	ID = input ("$ hostIP: ")
	port = input("$ port: ")
	current_Dc_no = getInfo(ID, port)
	print("Connected to DataCenter: ", end = "")
	print(current_Dc_no)

	while True:

		ipt = input("$ ")
		if(ipt == "lookup"):
			lookup(ID, port)

		elif(ipt == "post"):
			post(ID, port)

		elif(ipt == "sync"):
			sync(ID, port)

		else:
			print("invalid input")



if __name__ == "__main__":
    main()




