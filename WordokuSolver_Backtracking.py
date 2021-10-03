import random
import sys
import time
vassigned=0 #variables assigned
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
        
    
def pickUnassigned(a,N): #it will pic pic any unassigned variable 
			#(Selecting row wise, column wise or grid wise gives best result because of constraints)
			#so I am selecting row wise here
    for i in range(N):
        for j in range(N):
            if a[i][j]=='*':
               return i,j     #will return row,col index

def isPossible(x,y,a,N):      #if any inserted element at pos x,y in wordoku is posible (any conflict is occuring or not)
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

def const_domain(x,y,a,N,domain): 	#After applying all constraints, remaining domain set values possible will be returned
					#a is wordoku array, N is size (9)
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

def goalTest(a,N):   #Goal Test, a-wordoku array
    for i in range(N):
        for j in range(N):
            if isPossible(i,j,a,N)==False:
                return False
    return True	

def CSP_BT(a,N): #CSP-WITH-BACKTRACKING, a-wordoku array
    global vassigned
    global nodes_generated
    if vassigned==(N*N):		#if all variables are assigned, then return
        printWordoku(a,N)
        print("\n")
        print("Final GoalTest",goalTest(a,N))
        print("\nTotal time:",time.time()-start_time)
        print("\nTotal search time:",time.time()-search_time)
        print("\nTotal nodes generated:",nodes_generated)
        exit()  #exit
    i,j=pickUnassigned(a,N) 		#selecting some unassigned node
    nodes_generated+=1
    cdomain=const_domain(i,j,a,N,domain) #only possible domain after using constraints
    for d in cdomain:
        a[i][j]=d
        if isPossible(i,j,a,N):
            vassigned=vassigned+1
            CSP_BT(a,N)
        a[i][j]='*'
        vassigned=vassigned-1
        
N=9
a=[]  #Array of wordoku
domain={} #DOMAIN
domain=set()
readWordoku(a,domain,N)
#create_random_list(a,random_list,N) #creating random list
search_time=time.time()
CSP_BT(a,N)  #calling CSP-backtracking algorithm

printWordoku(a,N)
print("\nFinal GoalTest",goalTest(a,N)) 
print("\nTotal time:",time.time()-start_time)
print("\nTotal search time:",time.time()-search_time)
print("\nTotal nodes generated:",nodes_generated)
