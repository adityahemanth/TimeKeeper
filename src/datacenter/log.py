#!/usr/bin/python
# Log file to maintain log info.

class log:

	def __init__(self, dc_no):
		self.dc_log = dict();
		self.dc_no = dc_no

	def append(self, time, logItem):
		self.dc_log[time] = logItem;

	def getLogs(self):
		return self.dc_log

	def getLogsFrom(self, time):

		new_log = dict()
		for k in self.dc_log:
			if( k > time ):
				new_log[k] = self.dc_log[k]

		return new_log


