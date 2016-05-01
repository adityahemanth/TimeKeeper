#!/usr/bin/python

class logItem:

	def __init__(self, dc_no, post, post_id = None):

		self.dc_no = dc_no
		self.post_id = post_id
		self.post = post


	def getInfluencerID(self):
		return self.post_id

	def getPost(self):
		return self.post

	def getDc_no(self):
		return self.dc_no

