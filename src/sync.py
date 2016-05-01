#!/usr/bin/python 
import socket
import pickle

class sync:

	def __init__(self, dc_ID ,tt, log_list):
		self.dc_ID = dc_ID
		self.tt = tt
		self.log = log_list
		process()

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



	def process(self):

		s = self.tt.getSize()
		table = self.tt.getTable()

		for i in range(0,s):
			self.log_list[i] = self.log_list[i].getLogsFrom(table[self.dc_no][i])

