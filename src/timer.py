import time
import threading

class Timer(threading.Thread):

	# init function
	def __init__(self, endTime, callback):
		self.t1 = time.time()
		self.stop = 0;
		self.endTime = endTime
		self.callback = callback
		print 'calling function'
		threading.Thread.__init__(self)

	def run(self):
		print 'running'
		while(True and self.stop != 1):
			self.t2 = time.time()
			print (self.t2 - self.t1)
			if(self.t2 - self.t1 >= self.endTime):
				# print 'done'
				self.callback()
				return

		if(self.stop == 1):
			print 'stopping'

	def reset(self):
		self.t1 = time.time();


	def stop(self):
		self.stop = 1



	
def hello():
	print 'hello'


t = Timer(6, hello)
t.start()
time.sleep(4)
t.reset()