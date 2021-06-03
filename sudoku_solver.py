from copy import deepcopy
import time
import sys
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def check(board,val,row,col):
    #check col
    checkpos=row+str(col)
    for i in ROW:
        
        pos=i+str(col)
        if board[pos]==val and pos!=checkpos:
            return False
        
    #check row
    for k in COL:
        pos=row+str(k)
        if board[pos]==val and pos!=checkpos:
            return False

    #check box
    if row in ROW[0:3]:
        if str(col) in COL[0:3]:
            for l in ROW[0:3]:
                for m in COL[0:3]: 
                    if board[l+m]==val and l+m!=checkpos:
                        return False                    
        if str(col) in COL[3:6]:
            for l in ROW[0:3]:
                    for m in COL[3:6]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[0:3]:
                    for m in COL[6:9]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False
    if row in ROW[3:6]:
        if str(col) in COL[0:3]:
            for l in ROW[3:6]:
                for m in COL[0:3]:
                    if board[l+m]==val and l+m!=checkpos:
                        return False
                    
        if str(col) in COL[3:6]:
            for l in ROW[3:6]:
                    for m in COL[3:6]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[3:6]:
                    for m in COL[6:9]: 
                        if board[l+m]==val and l+m!=checkpos:
                            return False
            
    if row in ROW[6:9]:
        if str(col) in COL[0:3]:
            for l in ROW[6:9]:
                for m in COL[0:3]:
                    if board[l+m]==val and l+m!=checkpos:
                        return False
                    
        if str(col) in COL[3:6]:
            for l in ROW[6:9]:
                    for m in COL[3:6]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False
        if str(col) in COL[6:9]:
            for l in ROW[6:9]:
                    for m in COL[6:9]:
                        if board[l+m]==val and l+m!=checkpos:
                            return False

    return True

def mrv(domain_dict, board):
    unassigned_tile = [tile for tile in domain_dict.keys() if board[tile] == 0]
    return min(unassigned_tile, key=lambda tile: len(domain_dict[tile]))

def backtracking(board):
    d=domains(board)
    finished_board = bt({},board,d)
    return finished_board

def bt(assignment, board,domains):
    """Takes a board and returns solved board."""
    cur_domain=deepcopy(domains)    
    


    x = [tile for tile in domains.keys() if board[tile] == 0]
    if not x:
        return board

    pos=mrv(domains, board)
    vals=cur_domain[pos]
    
    for k in vals:
        if forwardcheck(board,k,pos)==True:
            d_copy=deepcopy(domains)

            board[pos]=k

            assignment_copy = deepcopy(assignment)
            assignment_copy[pos] = k
            d=updatedomains(cur_domain,board)

            result=bt(assignment_copy,board, d)
            if result!=False:
                return result
            
            board[pos]=0
        d =deepcopy(domains)
    return False

def forwardcheck(board, pos, k):
    board[pos]=k
    allvars=[]
    for i in ROW:
        for j in COL:
            if board[i+j]==0:
                posvar=[]
                for k in range(1,10):
                    if check(board,k,i,j):
                        posvar.append(k)
                allvars.append(posvar)
    if any (x==[] for x in allvars):
        return False
    else:
        return True

def checkdone(board):
    for i in ROW:
        for j in COL:
            if check(board,board[i+j],i,j)==False:
               return False 
    return True

def domains(board):
    allvars=[]
    allboardpos=[]
    varsdict={}
    for i in ROW:
        for j in COL:
            if board[i+j]==0:
                posvar=[]
                boardpos=str(i+j)
                allboardpos.append(boardpos)
                for k in range(1,10):
                    if check(board,k,i,j):
                        posvar.append(k)
                allvars.append(posvar)
                varsdict[str(i+j)]=posvar
    if len(allvars)>0:
        minvars=min(allvars)
        ind=allvars.index(minvars)
        orddict={a: b for a, b in sorted(varsdict.items(), key=lambda item: len(item[1]))}
        return orddict
        
    return False

def updatedomains(domain,board):
    allvars=[]
    allboardpos=[]
    varsdict={}
    for i in domain:
        posvar=[]
        boardpos=i
        allboardpos.append(boardpos)
        for k in range(1,10):
            if check(board,k,i[0],i[1]):
                posvar.append(k)
        allvars.append(posvar)
        varsdict[i]=posvar
    if len(allvars)>0:
        minvars=min(allvars)
        ind=allvars.index(minvars)
        orddict={a: b for a, b in sorted(varsdict.items(), key=lambda item: len(item[1]))}
        return orddict
        
    return False
def solver(line):
    
    board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

    if initial_check(board):
        sol=backtracking(board)
        return(sol)
    else:
        return False
#    return backtracking(board)
def initial_check(board):
    #Check Rows
    for i in ROW:
        row_val=[]
        for j in COL:
            row_val.append(board[i+j])
        no_zero_row=list(filter(lambda a: a != 0, row_val))
        if len(no_zero_row)!=len(set(no_zero_row)):    
            return False
    #Check Columns
    for i in COL:
        col_val=[]
        for j in ROW:
            col_val.append(board[j+i])
        no_zero_col=list(filter(lambda a: a != 0, col_val))
        if len(no_zero_col)!=len(set(no_zero_col)):    
            return False
    #Check Boxes in cols 1-3
    box1=[]
    box2=[]
    box3=[]
    for i in ROW[0:3]:   
        for j in COL[0:3]:
            box1.append(board[i+j])
        no_zero_box_1=list(filter(lambda a: a != 0, box1))
        if len(no_zero_box_1)!=len(set(no_zero_box_1)):
            return False
        for j in COL[3:6]:   
            box2.append(board[i+j])
        no_zero_box_2=list(filter(lambda a: a != 0, box2))
        if len(no_zero_box_2)!=len(set(no_zero_box_2)):
            return False
        for j in COL[6:9]:
            box3.append(board[i+j])
        no_zero_box_3=list(filter(lambda a: a != 0, box3))
        if len(no_zero_box_3)!=len(set(no_zero_box_3)):
            return False
    #Check Boxes in cols 3-6
    box1=[]
    box2=[]
    box3=[]
    for i in ROW[3:6]:   
        for j in COL[0:3]:
            box1.append(board[i+j])
        no_zero_box_1=list(filter(lambda a: a != 0, box1))
        if len(no_zero_box_1)!=len(set(no_zero_box_1)):
            return False
        for j in COL[3:6]:   
            box2.append(board[i+j])
        no_zero_box_2=list(filter(lambda a: a != 0, box2))
        if len(no_zero_box_2)!=len(set(no_zero_box_2)):
            return False
        for j in COL[6:9]:
            box3.append(board[i+j])
        no_zero_box_3=list(filter(lambda a: a != 0, box3))
        if len(no_zero_box_3)!=len(set(no_zero_box_3)):
            return False
    #Check Boxes in cols 6-9 
    box1=[]
    box2=[]
    box3=[]
    for i in ROW[6:9]:   
        for j in COL[0:3]:
            box1.append(board[i+j])
        no_zero_box_1=list(filter(lambda a: a != 0, box1))
        if len(no_zero_box_1)!=len(set(no_zero_box_1)):
            return False
        for j in COL[3:6]:   
            box2.append(board[i+j])
        no_zero_box_2=list(filter(lambda a: a != 0, box2))
        if len(no_zero_box_2)!=len(set(no_zero_box_2)):
            return False
        for j in COL[6:9]:
            box3.append(board[i+j])
        no_zero_box_3=list(filter(lambda a: a != 0, box3))

        if len(no_zero_box_3)!=len(set(no_zero_box_3)):
            return False
    return True