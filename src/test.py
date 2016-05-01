from timetable import *
from log import log

tt0 = timeTable(3,0)
tt1 = timeTable(3,1)
tt2 = timeTable(3,2)

for x in range (0,7):
	tt0.incrementEntry()

for x in range (0,4):
	tt1.incrementEntry()

for _ in  range (0,5):
	tt2.incrementEntry()

tt1.updateTable(tt2)
tt0.updateTable(tt1)

print tt0.getTable()
print tt0.getLatest(2);


print ("\n\n\n TESTING LOG ITEMS \n\n\n ")

li = logItem(0,5,"This is a post",2)

print li.getUID()
print li.getPost()
print li.getDc_no()
print li.getInfluencerID()

