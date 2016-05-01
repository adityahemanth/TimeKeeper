#!/usr/bin/python  

class post:

	def __init__(self, u_id, p_id, post):
		self.u_id = u_id
		self.p_id = p_id
		self.post = post


	def getUID(self):
		return self.u_id

	def getPostID(self):
		return self.p_id

	def getPost(self):
		return self.post

