import random
from queue import PriorityQueue
import copy
import time
vassigned=0 #vassigned
start_time=time.time()
nodes_generated=0

def printWordoku(a,N):  #it will print the wordoku, a-wordoku array, N-size
    f=open("solution.txt","w")
    for i in range(N):
        for j in range(N):
            f.write(str(a[i][j]))
            f.write(" ")
        f.write("\n")
    f.close()
            
def readWordoku(a,domain,N): #will read wordoku from file, a-wordoku array is sudoku array
    global vassigned
    f = open("input.txt", "r")
    for i in range(N):
        line=f.readline()
        words=line.split()
        for d in words:
            if d!='*':
                domain.add(d)
                vassigned+=1
        a.append(words)
    f.close()

def create_fill_list(a,N): #It will create a list of variables which need to be fill
    fill_list=[]
    for i in range(N):
        for j in range(N):
            if a[i][j]=='*':
                fill_list.append((i,j))
    return fill_list
                
def picRandompos(fill_list): #it will generate some random variable
    pos=random.randint(0,len(fill_list)-1)
    return fill_list[pos]

def isPossible(x,y,a,N):   #if any inserted element at pos x,y in wordoku array (a)  is posible (any conflict is occuring or not)
    #row search
    for i in range(N):
        if i!=y and a[x][i]==a[x][y]:
            return False
    #col search
    for i in range(N):
        if i!=x and a[i][y]==a[x][y]:
            return False
    #grid search
    for i in range((x//3)*3,(x//3)*3+3):
        for j in range((y//3)*3,(y//3)*3+3):
            if i!=x and j!=y and a[i][j]==a[x][y]:
                return False
    return True

def const_domain(x,y,a,N,domain): #After applying all constraints, remaining domain set values possible will be returned
    cdomain={}
    cdomain=set() #constraint domain
    #row search
    for i in range(N):
        if a[x][i]!='*':
            cdomain.add(a[x][i])
    #col search
    for i in range(N):
        if a[i][y]!='*':
            cdomain.add(a[i][y])
    #grid search
    for i in range((x//3)*3,(x//3)*3+3):
        for j in range((y//3)*3,(y//3)*3+3):
            if a[i][j]!='*':
                cdomain.add(a[i][j])
    return domain.difference(cdomain) 

def goalTest(a,N):  #GOAL TEST, IF GOAL IS REACHED OR NOT
    for i in range(N):
        for j in range(N):
            if isPossible(i,j,a,N)==False:
                return False
    return True
    
def minimize_conflict(a,b,x,y,N,domain):  #it will return that value, for which the number of conflict will be minimum for given variable
					# It will also allow to escape from local minima, by allow uphill move with 5% probability
    cdomain=const_domain(x,y,b,N,domain) #adding constraints to reduce possible values for particular variable
    pq=PriorityQueue()
    for d in cdomain:
        count=0
        for i in range(N):
            if i!=y and a[x][i]==d:
                count=count+1
        #col search
        for i in range(N):
            if i!=x and a[i][y]==d:
                count=count+1
        #grid search
        for i in range((x//3)*3,(x//3)*3+3):
            for j in range((y//3)*3,(y//3)*3+3):
                if i!=x and j!=y and a[i][j]==d:
                    count=count+1
        pq.put((count,d))
    xx=(0,0)
    if random.random()<0.05: #downhill move probability
    	pos=random.randint(0,len(cdomain)-1)
    	for i in range(pos-1):
    		xx=pq.get()
    else:
    	xx=pq.get()
    return xx
          
def min_conflict(a,b,max_steps,fill_list,N,domain):
    global nodes_generated
    for k in range(max_steps):
        if goalTest(a,N)==True:  #O(n2)
        	return
        
        i,j=picRandompos(fill_list) #O(1)
        nodes_generated+=1
        item=minimize_conflict(a,b,i,j,N,domain)
        best_pic=item[1]
        a[i][j]=best_pic
        
    return False

def fill_board(a,N,domain):  #it will fill the board variable with any random value in it's domain, it min-conflict require filled board
    temp_list=[d for d in domain]
    for i in range(N):
        for j in range(N):
            if a[i][j]=='*':
                a[i][j]=temp_list[random.randint(1,len(domain)-1)]
N=9
a=[]
domain={}
domain=set()
readWordoku(a,domain,N)

b=copy.deepcopy(a)

fill_board(a,N,domain)  #fill the sudoku-array a

fill_list=create_fill_list(b,N)
search_time=time.time()
min_conflict(a,b,1000000,fill_list,N,domain)
total_search_time=time.time()-search_time

printWordoku(a,N)
print("\nFinal GoalTest",goalTest(a,N)) 
print("\nTotal time:",time.time()-start_time)
print("\nTotal search time:",total_search_time)
print("\nTotal nodes generated:",nodes_generated)
