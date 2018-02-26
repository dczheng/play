#!/usr/bin/python
import anticomm_f
import sys
import time
time1=time.time()
A=sys.argv[1]+sys.argv[2]
B=sys.argv[2]+sys.argv[1]
formula_list1=anticomm_f.anticomm_f(A)
formula_list2=anticomm_f.anticomm_f(B)
for k in formula_list1.keys():
	if k in formula_list2.keys():
		formula_list1[k]=formula_list1[k]+formula_list2[k]
		formula_list2.pop(k)
for k in formula_list2.keys():
	formula_list1[k]=formula_list2[k]
formula_list={}
for k in formula_list1.keys():
	if not(formula_list1[k]==0):
		formula_list[k]=formula_list1[k]
if (formula_list=={}):
	print 0
else:
	formula_str=''
	for k in formula_list.keys():
		if(formula_list[k]>0):
			formula_str=formula_str+' + '+str(formula_list[k])+'*'
			formula_str=formula_str+k.replace('c','{b,a}')
		else:	
			formula_str=formula_str+' - '+str(-formula_list[k])+'*'
			formula_str=formula_str+k.replace('c','{b,a}')
	print formula_str
time2=time.time()
Time=time2-time1
print
print "%-10s%-10f"%("Time:",Time)
