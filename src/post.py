#!/usr/bin/python  

class post:

	def __init__(self, dc_Id, post,versionNumber):
		self.dc_Id = dc_Id
		self.versionNumber=versionNumber
		self.post = post
		
	def getVersionNum(self):
		return self.versionNumber
	
	def getDCID(self):
		return self.dc_Id

	def getPost(self):
		return self.post

