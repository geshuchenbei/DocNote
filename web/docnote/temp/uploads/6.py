# coding=utf-8
info=[]
keywordList={"语文":0,"数学":1,"英语":2,"物理":3,"化学":4}
class student:
	sid=0
	name=''
	socore=[0]*5
	sum=0
	avg=0
	rank=0
	def __init__(self,input):
		temp=input().split(',')
		self.sid=int(temp[0])
		self.name=temp[1]
		self.socore=[int(x) for x in temp[2:]]
		for i in range(0,5):self.sum+=self.socore[i]
		self.avg=self.sum/5.0
	def setRank(self,rank):
		self.rank=rank
	def printInfo(self,rank='First',printList=[0,1,2,3,4],sum_and_avg=True):
		if rank=='First': print(self.rank),
		print(self.sid),
		print(self.name),
		for i in printList: print(self.socore[i]),
		if sum_and_avg:
			print(self.sum),
			print(self.avg),
		if rank=='Last': print(self.rank),
		print
		
def bigger(a,b,key):#compare by key
	if key=='sid':
		return a.sid>b.sid
	elif key=='sum':
		if a.sum!=b.sum: return a.sum>b.sum
	else:
		if a.socore[key]!=b.socore[key]: return a.socore[key]>b.socore[key]
	
	
	if a.sum==b.sum:
		for i in range(0,5):
			if a.socore[i]==b.socore[i]: continue
			else: return a.socore[i]>b.socore[i]
	else: return a.sum>b.sum


def selectionSort(key):
	for i in range(0,len(info)):
		pMax=i
		for j in range(i,len(info)):
			if bigger(info[j],info[pMax],key):
				pMax=j
		info[i],info[pMax] = info[pMax],info[i] #swap

def bubbleSort(key):
	for i in range(len(info)-1):
		for j in range(len(info)-i-1):
			if bigger(info[j+1],info[j],key):
				info[j+1],info[j]=info[j],info[j+1]

def binSearch(sid):
	cnt=0
	f=0
	r=len(info)
	mid=(f+r)/2
	while f<=r and cnt<=30:
		mid=(f+r)/2
		if info[mid].sid==sid: break
		if info[mid].sid>sid: f=mid
		else: r=mid
		cnt+=1
	if info[mid].sid==sid: info[mid].printInfo(rank='Last')
	else: print ("not found!")


##########################################################


def read():
	try:
		while True:
			info.append(student(raw_input))
	except: return

def sortAll():
	try:
		selectionSort('sum')
		for i in range(0,len(info)):
			info[i].setRank(i+1)
			info[i].printInfo()
		print("******")
	except: return

def querySubject():
	try:
		while True:
			query=raw_input()
			if query=='======': break
			bubbleSort(keywordList[query])
			for i in range(len(info)):
				print(i+1),
				info[i].printInfo(rank='None',printList=[keywordList[query]],sum_and_avg=False)
		print("******")
	except: return

def queryStudent():
	try:
		selectionSort('sid')
		while True:
			query=raw_input()
			if query=='======': break
			binSearch(int(query))
		print("******")
	except: return

if __name__=="__main__":
	read()
	sortAll()
	querySubject()
	queryStudent()
