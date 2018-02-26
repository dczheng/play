#!/usr/bin/python
def isover(fa):
	i=0
	while(i<len(fa) and fa[i] =='c'):
		i=i+1
	while(i<len(fa) and fa[i] =='a'):
		i=i+1
	while(i<len(fa) and fa[i] =='b'):
		i=i+1
	if(i<len(fa)):
		return 0
	else:
		return 1
def changec(fa):
	for i in range(len(fa)):
		if(fa[i]=='c'):
			j=i
			while(j>0):
				fa[j]=fa[j-1]
				j=j-1;
			fa[j]='c'
	return fa

def comm_f(fa):
  fa_list=[]
  tmp=[]
  fa_list.append([i for i in fa])
  for fa1 in fa_list:
    fa1=changec(fa1)
    i=0
    while (i<len(fa1)):
      while(i<len(fa1) and fa1[i]=='c'):
        i=i+1
      while(i<len(fa1) and fa1[i]=='a'):
        i=i+1
      while(i<len(fa1) and fa1[i]=='b'):
        i=i+1
      if (i<len(fa1)):
        i=i-1
        fa1[i]='a'
        fa1[i+1]='b'
        tmp=fa1[0:i]+['c']+fa1[i+2:]
        fa_list.append(tmp)
        if(isover(fa1)==0):
         i=0
  return fa_list
