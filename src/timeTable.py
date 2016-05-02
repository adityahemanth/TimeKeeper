#!/usr/bin/python  
# timetable class.

class timeTable:

	# initializes timeTable.
	def __init__(self, dc_size, dc_no):
		self.dc_no = dc_no 
		self.dc_size = dc_size
		self.tt = [ [0 for _ in range(0,dc_size)] for _ in range(0, dc_size)]


	def getSize(self):
		return self.dc_size

	def getDc_no(self):
		return self.dc_no

	def getSize(self):
		return self.dc_size

	# returns time table
	def getTable(self):
		return self.tt

	# updates the timetable with the max of self and
	# passed in values.
	def updateTable(self, tt2):

		dc_no2 = tt2.getDc_no()
		tt2 = tt2.getTable()
 
		for i in range(0, self.dc_size):
			self.tt[self.dc_no][i] = max(tt2[dc_no2][i], self.tt[self.dc_no][i])

		for i in range(0, self.dc_size):
			for j in range(0, self.dc_size):
				self.tt[i][j] = max(self.tt[i][j], tt2[i][j])


	# gets the latest info about a datacenter
	# with of id : ID. 
	def getLatest(self, ID):
		ID = ID 
		return self.tt[self.dc_no][ID]


	# updates a single entry in the timetable
	# used to update the datacenters own entry
	def incrementEntry(self):
		self.tt[self.dc_no][self.dc_no] += 1

	def getEntry(self):
		return self.tt[self.dc_no][self.dc_no]






