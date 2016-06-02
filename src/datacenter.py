#!/usr/bin/python  
import pickle, socket
from timeTable import timeTable
from log import log 
from logItem import *
from sync import *
from syncObject import *
from message import *
from syncRequest import *

# each data center will have a number.
class datacenter:

	def __init__(self, dc_ID):
		self.dc_ID = int(dc_ID)
		self.tt = timeTable(3, self.dc_ID)
		self.posts = []
		self.dc_log = log(self.dc_ID)
		# self.listen()

	def listen(self):
		
		tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

		tcpsock.bind((self.host,self.port))
		tcpsock.listen(5)
		print("listening ...")

		while True:
			(c, addr) = tcpsock.accept()
			rcv = c.recv(4096)
			message = pickle.loads(rcv)
			mtype = message.getType() 

			# client requests
			if (mtype == "lookup"):
				
				sendList = pickle.dumps(self.posts, 0)
				c.send(sendList)


			elif(mtype == "post"):
				
				self.tt.incrementEntry()
				postObj = message.getPayload()
				logitem = logItem(self.dc_ID, self.tt.getEntry(), postObj)
				self.dc_log.append(logitem)
				self.posts.append(postObj)
				c.send("200")

			elif(mtype == "sync"):
				
				newDc_no = int(message.getPayload())

				if(newDc_no != self.dc_ID and newDc_no < 4):
					new_logs = self.dc_log.getLogsFor(self.tt, newDc_no)
					syn = sync(newDc_no, self.tt, new_logs)

					syn.send(self.dc_list[newDc_no])
					c.send("200")

				else:
					c.send("404")

			elif(mtype == "sync_request"):

				newDc_no = int(message.getPayload())
				if(newDc_no != self.dc_ID and newDc_no < 4):
					synReq = syncRequest(self.dc_list[newDc_no], self.dc_ID)
					c.send("200")


				else:
					c.send("404")
			# server request
			elif(mtype == "sync_response"):
				
				syncObj = message.getPayload()
				logs =  syncObj.getLogs()
				new_tt = syncObj.getTimeTable()
				self.tt.updateTable(new_tt)

				for item in logs:
					if(self.dc_log.isUnique(item)):
						self.dc_log.append(item)
						self.posts.append(item.getPost())

				c.send("200")

			elif(mtype == "info"):
				c.send(str(self.dc_ID))

			else:
				c.send("404")

			print (mtype, addr)
			c.close()

	def config(self):

		self.dc_list = input("Input config:")
		print(self.dc_list)
		print(self.dc_ID)
		(self.host,self.port) = self.dc_list[self.dc_ID]		
	def setDcList(self,dc_list):
		self.dc_list = dc_list
		(self.host,self.port) = self.dc_list[self.dc_ID]
		
	def setHost(self,host):
		self.host=host
	def setPort(self,port):
		self.port=port


def main():

	ID = input ("$ datacenter ID:")
	dc = datacenter(ID)
	dc.config()
	#dc.setDcList([(str("0.0.0.0"),int(10000))])
	#dc.setHost('0.0.0.0')
	#dc.setPort(10000)
	dc.listen()

if __name__ == "__main__":
    main()

