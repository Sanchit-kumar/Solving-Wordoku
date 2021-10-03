import random
import copy
import math
import numpy as np
import sys
import enchant

vassigned=0 #variables assigned
word=enchant.Dict("en_US") #dictionary type
total_words={}
total_words=set() #for listing only unique words

def printWordoku(board,N): #it will print the wordoku, board-array, N-size
    for i in range(N):
        if i%3==0:
            print("")
        print("")
        for j in range(N):
            if j%3==0:
                print("\t",end="")
            print(board[i][j],end="\t")
            
def readWordoku(board,domain,N): #will read wordoku from file
    global vassigned
    f = open("input.txt", "r")
    for i in range(N):
        line=f.readline()
        words=line.split()
        for d in words:
            if d!='*':
                domain.add(d)
                vassigned+=1
        board.append(words)
        
    
def pickUnassigned(board,N): #it will pic pic any unassigned variable 
			#(Selecting row wise, column wise or grid wise gives best result because of constraints)
			#so I am selecting row wise here
    for i in range(N):
        for j in range(N):
            if board[i][j]=='*':
               return i,j     #will return row,col index

def isPossible(x,y,board,N):      #if any inserted element at pos x,y in wordoku is posible (any conflict is occuring or not)
    #row search
    for i in range(N):
        if i!=y and board[x][i]==board[x][y]:
            return False
    #col search
    for i in range(N):
        if i!=x and board[i][y]==board[x][y]:
            return False
    #grid search
    for i in range((x//3)*3,(x//3)*3+3):
        for j in range((y//3)*3,(y//3)*3+3):
            if i!=x and j!=y and board[i][j]==board[x][y]:
                return False
    return True

def const_domain(x,y,board,N,domain): 	#After applying all constraints, remaining domain set values possible will be returned
    cdomain={}
    cdomain=set() #constraint domain
    #row search
    for i in range(N):
        if board[x][i]!='*':
            cdomain.add(board[x][i])
    #col search
    for i in range(N):
        if board[i][y]!='*':
            cdomain.add(board[i][y])
    #grid search
    for i in range((x//3)*3,(x//3)*3+3):
        for j in range((y//3)*3,(y//3)*3+3):
            if board[i][j]!='*':
                cdomain.add(board[i][j])
    return domain.difference(cdomain)

def goalTest(board,N):   #Goal Test
    for i in range(N):
        for j in range(N):
            if isPossible(i,j,board,N)==False:
                return False
    return True	
def row_col_word(board,N): #It will add all complete row and column word
    global word
    global total_words
    count=0
    for i in range(N):
        row_str=""
        col_str=""
        for j in range(N):
            row_str+=board[i][j]
            col_str+=board[j][i]
        if word.check(row_str):
            total_words.add(row_str)
        if word.check(col_str):
            total_words.add(col_str)
            
def diagonal_word(board,N): #It will add main diagonal and off_diagonal word
    global word
    global total_words
    main_diag=""
    off_diag=""
    for i in range(N):
        main_diag+=board[i][i]
        off_diag+=board[N-1-i][i]
    if word.check(main_diag):
        total_words.add(main_diag)
    if word.check(off_diag):
        total_words.add(off_diag)
    
def listwords(board,N):  #It will list all meaning full word of row, column and diagonal and add to total_word set
    row_col_word(board,N)
    diagonal_word(board,N)
    #print(total_words)
    
    if len(total_words)>0:
        print("List of all meaning words present in wordoku (w.r.t pyenchant):")
        for w in total_words:
            print(w)
    else:
        print("No meaning full word present  (w.r.t pyenchant)")
    
def CSP_BT(board,N): #CSP-WITH-BACKTRACKING
    global vassigned
    if vassigned==(N*N):		#if all variables are assigned, then return
        printWordoku(board,N)
        print("\n")
        print("Final GoalTest",goalTest(board,N))
        listwords(board,N)
        exit()  #exit
    i,j=pickUnassigned(board,N) 		#selecting some unassigned node
    cdomain=const_domain(i,j,board,N,domain) #only possible domain after using constraints
    for d in cdomain:
        board[i][j]=d
        if isPossible(i,j,board,N):
            vassigned=vassigned+1
            CSP_BT(board,N)
        board[i][j]='*'
        vassigned=vassigned-1
        
  
N=9
board=[]  #Array of wordoku
domain={} #DOMAIN
domain=set()
readWordoku(board,domain,N)
CSP_BT(board,N)  #calling CSP-backtracking algorithm
print("\nFinal GoalTest",goalTest(board,N))
print("Final Wordoku") 
printWordoku(board,N)

listwords(board,N)
print(total_words)
if len(total_words)>0:
    print("List of all meaning words present in wordoku (w.r.t pyenchant):")
    for w in total_words:
        print(w)
else:
    print("None (w.r.t pyenchant)")
