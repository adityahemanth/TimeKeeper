#!/usr/bin/python 
import socket
import pickle
from syncObject import *
from message import *

class sync:

	def __init__(self, dc_ID ,tt, log_list):
		self.dc_ID = dc_ID
		self.tt = tt
		self.log_list = log_list

	def send(self, host, port):
		self.host = host
		self.port = port


		#creating a sync object
		syncObj = syncObject(self.tt, self.log_list) 

		s = socket.socket()
		m = message("sync", syncObj)
		s.connect((self.host, self.port))
		s.send(pickle.dumps(m,0))
		s.close()

