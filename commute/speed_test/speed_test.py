#!/usr/bin/python
import random
import comm_f1
import comm_f2
import time
M=4
N=30
print "%-10s%-10s%-10s%-10s%-10s"%("num1","num2","time1","time2","time1/time2")
for i in range(M,N):
	fa_str=''
	for j in range(i):
		k=random.randint(1,100)
		if(k%2==0):
			fa_str=fa_str+'a'
		else:
			fa_str=fa_str+'b'	
	time11=time.time()
	output1=comm_f1.comm_f(fa_str)
	time12=time.time()
	time1=time12-time11
	time21=time.time()
	output2=comm_f2.comm_f(fa_str)
	print output2
	time22=time.time()
	time2=time22-time21
	num1=len(output1)
	num2=sum(output2.values())
	print "%-10d%-10d%-10f%-10f%-10f"%(num1,num2,time1,time2,time1/time2)
	print 
