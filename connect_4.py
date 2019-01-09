import numpy as np
import pygame
import sys
import math
from pygame.locals import *

#RGB VALUE, which is blue in this case
COLOUR_BOARD = (0,0,255)
#RGB VALUE, which is black in this case
COLOUR_BACKGROUND = (0,0,0)
COLOUR_PLAYER1 = (255,0,0)
COLOUR_PLAYER2 = (255,255,0)



ROW_COUNT = 6
COLUMN_COUNT = 7
CONNECT_COUNT = 4


def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
board = create_board()

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    if col>COLUMN_COUNT:
        print("The column you selected is outside the board, you lost your turn")
    else: return board[ROW_COUNT-1][col]==0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
def print_board(board):
    print(np.flip(board, 0))
    
def winning_move(board, piece):
    #Checking all horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r][c+i]==piece:
                    check = True
                    break
            if check==False:
                return True
    #Checking all verical locations        
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r+i][c]==piece:
                    check = True
                    break
            if check==False:
                return True
    #Checking all positive sloping diagonal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r+i][c+i]==piece:
                    check = True
                    break
            if check==False:
                return True
    #Checking all negative sloping diagonal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r-i][c+i]==piece:
                    check = True
                    break
            if check==False:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, COLOUR_BOARD,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen, COLOUR_BACKGROUND,(int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                pygame.draw.circle(screen, COLOUR_PLAYER1,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c]==2:
                pygame.draw.circle(screen, COLOUR_PLAYER2,(int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
    
    
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)
RADIUS = int(SQUARESIZE/2 -5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace",75)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, COLOUR_BACKGROUND, (0,0,width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen,COLOUR_PLAYER1,(posx,int(SQUARESIZE/2)),RADIUS)
            else:
                pygame.draw.circle(screen,COLOUR_PLAYER2,(posx,int(SQUARESIZE/2)),RADIUS)
        pygame.display.update()
                
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, COLOUR_BACKGROUND, (0,0,width, SQUARESIZE))
            #Ask for Player 1 input
            if turn==0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 1)
                    print_board(board)
                    draw_board(board)
                    if winning_move(board,1):
                        label = myfont.render("Player 1 wins! Congrats",1,COLOUR_PLAYER1)
                        screen.blit(label,(40,10))
                        game_over = True
            #Ask for Player 2 input
            else: 
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board,col)
                    drop_piece(board, row, col, 2)
                    print_board(board)
                    draw_board(board)
                    if winning_move(board,2):
                        print("winning so far")
                        label = myfont.render("Player 2 wins! Congrats",1,COLOUR_PLAYER2)
                        screen.blit(label,(40,10))
                        game_over = True

            turn += 1
            turn = turn %2
            if game_over:
                pygame.time.wait(10000)