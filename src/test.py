from timeTable import *
from log import log
from logItem import *
from message import *
from sync import *
from syncObject import *

tt0 = timeTable(3,0)

for x in range (0,7):
	tt0.incrementEntry()


log1 = log(1)
log2 = log(2)
log3 = log(3)


log_list = [log1, log2, log3]
host = "127.0.0.1"
port = 9999

syn = sync(2, tt0, log_list)
syn.send(host,port)

