#!/usr/bin/python  
import pickle, socket
import message, syncObject
import timeTable, log, logItem

# each data center will have a number.
class datacenter:

	def __init__(self, dc_ID, port):
		self.dc_ID = dc_ID
		self.port = port
		self.host = "0.0.0.0"
		self.tt = timeTable(3, dc_ID)
		self.posts = []
		self.dc_log = log(dc_ID)
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

			elif(mtype == "sync_request"):
				
				newDc_no = message.getPayload()
				new_logs = self.dc_log.getLogsFor(newDc_no)
				syn = sync(newDc_no, self.tt, new_logs)
				syn.send()
				c.send("200")

			# server request
			elif(mtype == "sync"):
				
				syncObj = message.getPayload()
				logs =  syncObj.getLogs()
				new_tt = syncObj.getTimeTable()
				self.tt.update(new_tt)

				for item in logs
					if(self.dc_log.isUnique(item)):
						self.dc_log.append(item)
						self.posts.append(item.getPost())

				c.send("200")


			else:
				c.send("404")

			print mtype
			c.close()

def main():

	ID = input ("$ datacenter ID: ")
	port = input("$ port: ")
	dc = datacenter(ID,port)
	dc.listen()



if __name__ == "__main__":
    main()

