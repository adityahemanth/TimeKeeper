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

	def send(self, conn):

		#creating a sync object
		syncObj = syncObject(self.tt, self.log_list) 

		s = socket.socket()
		m = message("sync_response", syncObj)
		s.connect(conn)
		s.send(pickle.dumps(m,0))
		s.close()

