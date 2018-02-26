#!/usr/bin/python
import comm_f
import sys
A=sys.argv[1]+sys.argv[2]
B=sys.argv[2]+sys.argv[1]
formula_list1=comm_f.comm_f(A)
formula_list2=comm_f.comm_f(B)
formula1=[]
formula2=[]
for fa in formula_list1:
  tmp=''.join(fa)
  tmp=tmp.replace('c','[b,a]')
  formula1.append(tmp)
for fa in formula_list2:
  tmp=''.join(fa)
  tmp=tmp.replace('c','[b,a]')
  formula2.append(tmp)
formula1_dict=dict()
formula2_dict=dict()
for fa in formula1:
  if fa in formula1_dict.keys():
    formula1_dict[fa]=formula1_dict[fa]+1
  else:
    formula1_dict[fa]=1
for fa in formula2:
  if fa in formula2_dict.keys():
    formula2_dict[fa]=formula2_dict[fa]+1
  else:
    formula2_dict[fa]=1
for fa in formula1_dict.keys():
  if fa in formula2_dict.keys():
    formula1_dict[fa]=formula1_dict[fa]-formula2_dict[fa]
    formula2_dict.pop(fa)
for k in formula2_dict.keys():
  formula1_dict[k]=-formula2_dict[k]
formula_dict=dict()
for k in formula1_dict.keys():
  if not(formula1_dict[k] == 0):
     formula_dict[k]=formula1_dict[k]
formula_str=''
for k in formula_dict.keys():
  if (formula_dict[k] > 0):
    formula_str=formula_str+' + '+str(formula_dict[k])+'*'
  else:
    formula_str=formula_str+' - '+str(-formula_dict[k])+'*'
  formula_str=formula_str+k
if formula_str=='':
  print 0
else:
  print formula_str
    


