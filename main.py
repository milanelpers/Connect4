import numpy as np
from enum import Enum

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)

BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')
"""
a = '|=======|'
b = '|000000X|'
'\n'.join((a,b))
"""
#for i in range(len(c)):
"""c=c.replace('=', '')
c=c.replace('|', '')
c=c.replace('\n', '')
"""
#np.zeroes((6,7),dtype=.....)

"""board.diagonal für diagonale
for i range(string)
    if (0,X,O) put into array sonst ignore
    string to board
"""
"""
array = np.full((6, 7), NO_PLAYER, dtype=BoardPiece)
print(array[0] == BoardPiece(0))
print(array)
"""
# abc--123-789-ABC-XYZ

board = np.full((6,7), NO_PLAYER, dtype=BoardPiece)
board[0][0]= PLAYER1
board[1][0]= PLAYER1
board[2][0]= PLAYER1
board[3][0]= PLAYER1
board[4][0]= PLAYER1
board[5][0]= PLAYER1
#print(board)
#print('/////////////////////////////////////')
a = '\n|===============|'

for i in range(5,-1,-1):
    a+='\n|'
    for j in range(7):
        if(board[i][j]==PLAYER1):
            a+=' '
            a += PLAYER1_PRINT
        elif(board[i][j]==PLAYER2):
            a += ' '
            a+= PLAYER2_PRINT
        else:
            a += ' '
            #a+=NO_PLAYER_PRINT
            a+='-'
    a+=' |'
a+='\n|===============|'
a+='\n| 0 1 2 3 4 5 6 |'


a=a.replace('=', '')
a=a.replace('|', '')
#a=a.replace('\n', '')
a=a.replace(' ', '')
a= a[:len(a)-7]

split = a.split('\n')
string =split[2:8]
#print(string)
board = np.full((6, 7),NO_PLAYER,dtype=BoardPiece)
for i in range(5,-1,-1):
    count = 0
    for j in string[i]:
        #print(j)
        if(j==PLAYER1_PRINT):
            board[5-i][count]=PLAYER1
        elif (j==PLAYER2_PRINT):
            board[5-i][count]=PLAYER2
        count+=1
for i in range(6):
    print(i)