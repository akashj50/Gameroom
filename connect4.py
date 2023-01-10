import numpy as n
import os
import pygame
import sys
import math
import mysql.connector
from tkinter import *
db=mysql.connector.connect(host="localhost",user="root",passwd="root" )
cursor=db.cursor()
try:                                            #to create or access the database and table
   cursor.execute("create database score;")
except:
   cursor.execute("use score;")
try:
   cursor.execute("create table player_info(Pno int,score int);")
except:
   pass
update="Update player_info set score = %s where Pno = %s" #to remove preexisting values in the score column
cursor.execute(update, (0,1))
cursor.execute(update, (0,2))


pygame.init()


row_no = 6
col_no = 7
f1=0
f2=0


blue = (0, 0, 205)
red = (225, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)


slot_size = 100            # Size of graphical game
width = col_no * slot_size
height = (row_no+1) * slot_size
size = (width, height)
radius = int(slot_size/2 - 5)
font = pygame.font.SysFont("comicsansms", 60)


def create_board():
     board = n.zeros((row_no,col_no))
     return board

def print_board(board):
     print(n.flip(board, 0))


def win_check(board, piece):

 for c in range(col_no-3): # Horizontal check for win
         for r in range(row_no):
                 if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                         return True

 for c in range(col_no): # Vertical check for win
         for r in range(row_no-3):
                 if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                         return True

 for c in range(col_no-3): # Diagonal check from bottom for win
         for r in range(row_no-3):
                 if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                         return True

 for c in range(col_no-3): # Diagonal check from top for win
         for r in range(3, row_no):
                 if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                         return True
                        

def drop_piece(board, row, col, piece): # function to replace the slot with the piece
         board[row][col] =  piece 

def valid_location(board, col): # function to see if a row has an open slot
         return board[row_no-1][col] == 0

def open_row(board, col): # function to find an open slot in a row and return it
         for r in range(row_no):
                 if board[r][col] == 0:
                         return r

def color_board(board): # function to fill the window with shapes and for coin
     for c in range(col_no):
         for r in range(row_no):
             pygame.draw.rect(screen, blue, (c*slot_size, r*slot_size+slot_size, slot_size, slot_size))
             pygame.draw.circle(screen, white, (int(c*slot_size+slot_size/2), int(r*slot_size+slot_size+slot_size/2)), radius)

     for c in range(col_no):
         for r in range(row_no):
             if board[r][c] == 1:
                 pygame.draw.circle(screen, red, (int(c*slot_size+slot_size/2), height-int(r*slot_size+slot_size/2)), radius)
             elif board[r][c] == 2:
                 pygame.draw.circle(screen, yellow, (int(c*slot_size+slot_size/2), height-int(r*slot_size+slot_size/2)), radius)
     pygame.display.update()

def mysql():  #to update the scores in database as well as return them to show in popup
  global f1
  global f2 
  upd8="Update player_info set score = %s where Pno = %s"
  cursor.execute(upd8, (v,u))
  a="select Pno, score from player_info where Pno = %s "
  cursor.execute(a, (u,))
  b=cursor.fetchone()
  db.commit()
  pn=b[0]
  if pn==1:
   f1=b[1]
  elif pn==2:
   f2=b[1]
  return f1
  return f2


def scorebox(): #popup to show scores
   root = Tk()
   text = Text(root,width=50,height=18)
   text.insert(INSERT, "Player 1 Score: "+str(f1)+"\n")
   text.insert(END, "Player 2 Score: "+str(f2))
   root.title("SCORES")
   text.pack()

   text.tag_add("here", "1.0", "1.20")
   text.tag_add("start", "2.0", "2.20")
   text.tag_config("here", foreground="blue", font=("comicsansms",25), spacing1=60, spacing3=10)
   text.tag_config("start", foreground="green", font=("comicsansms",25), spacing1=60, spacing3=10)
   root.mainloop()



while True: 
 board = create_board()
 print_board(board)
 game = True
 turn = 0


 screen = pygame.display.set_mode(size)
 color_board(board)
 pygame.display.update()

 p1 = 0
 p2 = 0
 global u
 global v

 while game: #to not close game automatically
         for event in pygame.event.get():

                 pygame.draw.rect(screen, white, (0,0, width, slot_size)) #to draw the red and yellow coin when mouse is still
                 x,y = pygame.mouse.get_pos()
                 if turn == 0:
                   pygame.draw.circle(screen, red, (x, int(slot_size/2)), radius)
                 else:
                   pygame.draw.circle(screen, yellow, (x, int(slot_size/2)), radius)
                                 
                 if event.type == pygame.QUIT:
                         sys.exit()

                 if event.type == pygame.MOUSEMOTION: #to draw the red and yellow coin when mouse is moving
                         pygame.draw.rect(screen, white, (0,0, width, slot_size))
                         x = event.pos[0]
                         if turn == 0:
                                 pygame.draw.circle(screen, red, (x, int(slot_size/2)), radius)
                         else:
                                 pygame.draw.circle(screen, yellow, (x, int(slot_size/2)), radius)
                 pygame.display.update()

                 if event.type == pygame.MOUSEBUTTONDOWN:

                         if turn == 0:
                             x = event.pos[0]
                             col = int(math.floor(x/slot_size))

                             if valid_location(board, col):
                                 row = open_row(board, col)
                                 drop_piece(board, row, col, 1)
                                 

                                 if win_check(board, 1):
                                         pygame.draw.rect(screen, white, (0,0, width, slot_size))
                                         text = font.render("Player 1 wins!!", 1, red)
                                         screen.blit(text, (160,10))                          
                                         board = create_board()
                                         color_board(board)
                                         pygame.display.update()
                                         p1=p1+1
                                         u=1
                                         v=p1
                                         mysql()
                                         scorebox()
                                   
                                         
                                        
                         else:
                                 x = event.pos[0]
                                 col = int(math.floor(x/slot_size))

                                 if valid_location(board, col):
                                         row = open_row(board, col)
                                         drop_piece(board, row, col, 2)
                                         
                                         if win_check(board, 2):
                                                 pygame.draw.rect(screen, white, (0,0, width, slot_size))
                                                 text = font.render("Player 2 wins!!", 1, yellow)
                                                 screen.blit(text, (160,10))
                                                 board = create_board()
                                                 color_board(board)
                                                 pygame.display.update()
                                                 p2=p2+1
                                                 u=2
                                                 v=p2
                                                 mysql()
                                                 scorebox()
                                               
                                                 
                                                 
                         print_board(board)
                         color_board(board)

                         turn = (turn + 1) % 2

                         if game == False: #redundant(testing purpose)
                                pygame.time.wait(3500)
