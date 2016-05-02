import socket, pickle
from message import message

class syncRequest:

	def __init__(self, conn, newDc_no):
		msg = message("sync", newDc_no)
		send = pickle.dumps(msg,0)
		s = socket.socket()
		s.connect(conn)
		s.send(send)
		s.close()