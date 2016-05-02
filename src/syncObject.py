#!/usr/bin/python 

class syncObject:

	def __init__(self,tt, log_list):
		self.tt = tt
		self.log_list = log_list

	def getLogs(self):
		return self.log_list

	def getTimeTable(self):
		return self.tt