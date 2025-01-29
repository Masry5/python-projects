"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX=0
    countO=0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]==X:
                countX+=1
            if board[row][col]==O:
                countO+=1

    if countX>countO:
        return O
    else:
        return X
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
  
    available=set()
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]== EMPTY:
                available.add((row,col))
                
    return available



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception ("not valid")
    row,col=action
    board2=copy.deepcopy(board)
    board2[row][col]=player(board2)
    return board2
 

def row_checker(board,player):
    
    for row in range(len(board)):
        counter=0
        for col in range(len(board[0])):
            if board[row][col]== player:
                counter+=1
        if counter==3:
            return player
    else:
        return False    
def col_checker(board,player):
    
    for row in range(len(board)):
        counter=0
        for col in range(len(board[0])):
            if board[col][row]== player:
                counter+=1
        if counter==3:
            return player
    else:
        return False 
def dig1_checker(board ,player):
    if board[0][2]==player and board[1][1]==player and board[2][0]==player:
        return True
    else:
        return False

def dig2_checker(board ,player):
    if board[0][0]==player and board[1][1]==player and board[2][2]==player:
        return True
    else:
        return False    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if dig1_checker(board,X) or dig2_checker(board,X) or row_checker(board,X) or col_checker(board,X):
        return X
    elif dig1_checker(board,O) or dig2_checker(board,O) or row_checker(board,O) or col_checker(board,O):
        return O
    else:
        return None 



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)== O :
        return True
    elif winner(board)== X:
        return True
    for i in range(len(board)):
        for j in range (len(board[i])):
            if board[i][j]==EMPTY:
                return False
    return True
   


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)== X:
        return 1
    elif winner(board)== O:
        return -1
    else:
        return 0

def min_value(board):
        if terminal(board):
            return utility(board)
        v=math.inf
        for action in actions(board):
            v=min(v,max_value(result(board,action)))
        return v
def max_value(board):
    if terminal(board):
       return utility(board)
    v=-math.inf
    for action in actions(board):
        v=max(v,min_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board)== X:
        plays=[]
        for action in actions(board):
            plays.append([min_value(result(board,action)),action])
        return sorted(plays,key=lambda x:x[0],reverse=True)[0][1]
    elif player(board)== O:
        plays=[]
        for action in actions(board):
            plays.append([max_value(result(board,action)),action])
        return sorted(plays,key=lambda x:x[0])[0][1]
        
    
    
  
