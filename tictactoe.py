import math
import copy
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
    num=0
    for i in range(3):
        for j in range(3):
            if(board[i][j]!=EMPTY):
                num+=1
    if board==initial_state():
        return X

    if num%2!=0:
        return O
    else:
        return X
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    a=set()
    num=0
    for i in range(3):
        for j in range(3):
            if(board[i][j]==EMPTY):
                num=1
                a.add((i,j))
    if(num==0):
        return -1
    else:
        return a
     #Raise Not Implemenyed Error
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newboard=copy.deepcopy(board)
    i,j=action
    if(newboard[i][j]!=EMPTY):
        raise Exception("Not Possible")
    else:
        newboard[i][j]=player(newboard)
        return newboard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #For rows
    for i in range(3):
        if (board[i].count(X)==3):
            return X
        elif(board[i].count(O)==3):
            return O

     #For Columns
    for i in range(3):
        if(board[0][i]==board[1][i]==board[2][i]== X):
            return X
        elif(board[0][i]==board[1][i]==board[2][i]==O):
            return O
     #For one Diagonal
    FlagO=0
    FlagX=0

    for i in range(3):
        if(board[i][i]==X):
            FlagX+=1
        elif(board[i][i]==O):
            FlagO+=1
    if(FlagX==3):
        return X
    elif(FlagO==3):
        return O
    #For the other diagonal
    FlagO = 0
    FlagX = 0

    for i in range(3):
        if (board[i][2-i] == X):
            FlagX += 1
        elif (board[i][2-i] == O):
            FlagO += 1
    if (FlagX == 3):
        return X
    elif (FlagO == 3):
        return O
    return None

       def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if (winner(board)!=None):
        return True
    Flag=0
    for i in range(3):
        for j in range(3):
            if(board[i][j]!=EMPTY):
                Flag+=1
    if(Flag==9):
        return True
    else:
        return False

       def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w=winner(board)
    if(w==X):
        return 1
    elif(w==O):
        return -1
    else:
        return 0

          def MIN(board):
    if (terminal(board)==True):
        return utility(board)

    b=2
    moves=actions(board)
    for move in moves:
        b=min(b,MAX(result(board,move)))
        if(b==-1):
            return b
    return b
def MAX(board):
    if (terminal(board)==True):
            return utility(board)

    b=-2
    moves=actions(board)
    for move in moves:
        b = max(b, MIN(result(board, move)))

        if(b==1):

            return b
        return b
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)==True):
        return None
    elif(player(board)==X):
        val=-2
        bestmove=tuple()
        moves=actions(board)
        for move in moves:
            move_val=MIN(result(board,move))
            if (val==1):
                return move
            elif(move_val>val):
                val=move_val
                bestmove=move
        return bestmove
    elif (player(board) == O):
        val = 2
        bestmove = tuple()
        moves = actions(board)
        for move in moves:
            move_val = MAX(result(board, move))
            if (move_val == -1):
                return move
            elif (move_val < val):
                val = move_val
                bestmove = move
        return bestmove
