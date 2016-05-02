#!/usr/bin/python

class logItem:

	def __init__(self, dc_no, post_id, post):

		self.dc_no = dc_no
		self.post_id = post_id
		self.post = post


	def getPostID(self):
		return post_id

	def getPost(self):
		return self.post

	def getDc_no(self):
		return self.dc_no

	def equals(self, logItem):
		if(self.dc_no == logItem.getDc_no()):
			if(self.post_id == logItem.getPostID()):
				return True

		return False

