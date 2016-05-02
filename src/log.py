#!/usr/bin/python
# Log file to maintain log info.

class log:

	def __init__(self, dc_no):
		self.dc_log = []
		self.dc_no = dc_no

	def append(self, logItem):
		self.dc_log.append(logItem)

	def getLogs(self):
		return self.dc_log

	def isUnique(self,logItem):
		for item in self.dc_log
			if(item.equals(logItem))
				return False

		return True

	def getLogsFor(self, tt, dc_no):

		new_log = []
		table = tt.getTable()
		for item in self.dc_log:
			if(table[dc_no][item.getDc_no()] < item.getPostID()):
				new_log.append(item)

		return new_log


