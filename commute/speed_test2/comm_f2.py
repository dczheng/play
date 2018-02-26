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
  fa1=[i for i in fa]
  fa1=changec(fa1)
  fa2=''.join(fa1)
  fa_dict={}
  fa_dict[fa2]=1
  fa_list=[fa1]
  fa_list.append(fa1)
  for fa1 in fa_list:
    fa2=''.join(fa1)
    i=0
    while(i<len(fa1)):
      while(i<len(fa1) and fa1[i]=='c'):
        i=i+1
      while(i<len(fa1) and fa1[i]=='a'):
        i=i+1
      while(i<len(fa1) and fa1[i]=='b'):
        i=i+1
      if(i<len(fa1)):
        i=i-1
        fa1[i]='a'
        fa1[i+1]='b'
        tmp1=fa1[0:i]+['c']+fa1[i+2:]
        tmp1=changec(tmp1)
        tmp2=''.join(tmp1)
        if tmp2 in fa_dict.keys():
           fa_dict[tmp2]=fa_dict[tmp2]+fa_dict[fa2]
        else:
           fa_dict[tmp2]=fa_dict[fa2]
           fa_list.append(tmp1)
        fa2n=''.join(fa1)
        if fa2n in fa_dict.keys():
           fa_dict[fa2n]=fa_dict[fa2]+fa_dict[fa2n]
           fa_list.reverse()
           fa_list.remove(fa1)
           fa_list.reverse() 
        else:
           fa_dict[fa2n]=fa_dict[fa2]
        fa_dict[fa2]=0
        if(isover(fa1)==0): 
           i=0
           fa2=''.join(fa1)
  fa_dict_out={}
  for k in fa_dict.keys():
    if not(fa_dict[k]==0):
       fa_dict_out[k]=fa_dict[k]
  return fa_dict_out
