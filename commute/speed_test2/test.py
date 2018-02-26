#!/usr/bin/python
import random
import os
import time
M=4
N=15
for i in range(M,N):
	A=''
	B=''
	for j in range(i):
		k=random.randint(1,100)
		if(k%2==0):
			A=A+'a'
		else:
			A=A+'b'	
		k=random.randint(1,100)
		if(k%2==0):
			B=B+'a'
		else:
			B=B+'b'	
	print 
	run_str="%s %s %s"%("./commute1.py",A,B)
	print 50*"-"
	print run_str
	time11=time.time()
	os.system(run_str)	
	time12=time.time()
	time1=time12-time11

	print
	run_str="%s %s %s"%("./commute2.py",A,B)
	print run_str
	time21=time.time()
	os.system(run_str)	
	time22=time.time()
	time2=time22-time21

	print 
	print "%-10s%-10s%-10s"%("time1","time2","time1/time2")
	print "%-10f%-10f%-10f"%(time1,time2,time1/time2)
	print 50*"-"
	print 
