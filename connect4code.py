import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

DARK_RED = (200,0,0)
DARK_GREEN = (0,200,0)

ROW_COUNT = 6 
COLUMN_COUNT = 7
CONNECT_COUNT = 4
clock = pygame.time.Clock()

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r
def text_objects(text, font):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

def print_board(board):
	print(np.flip(board, 0))

# def winning_move(board, piece):
# 	# Check horizontal locations for win
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(ROW_COUNT):
# 			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
# 				return True

# 	# Check vertical locations for win
# 	for c in range(COLUMN_COUNT):
# 		for r in range(ROW_COUNT-3):
# 			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
# 				return True

# 	# Check positively sloped diaganols
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(ROW_COUNT-3):
# 			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
# 				return True

# 	# Check negatively sloped diaganols
# 	for c in range(COLUMN_COUNT-3):
# 		for r in range(3, ROW_COUNT):
# 			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
# 				return True

def winning_move(board, piece):
    #Checking all horizontal locations
    for c in range(COLUMN_COUNT-CONNECT_COUNT+1):
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
        for r in range(ROW_COUNT-CONNECT_COUNT+1):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r+i][c]==piece:
                    check = True
                    break
            if check==False:
                return True
    #Checking all positive sloping diagonal locations
    for c in range(COLUMN_COUNT-CONNECT_COUNT+1):
        for r in range(ROW_COUNT-CONNECT_COUNT+1):
            check = False
            for i in range(CONNECT_COUNT):
                if not board[r+i][c+i]==piece:
                    check = True
                    break
            if check==False:
                return True
    #Checking all negative sloping diagonal locations
    for c in range(COLUMN_COUNT-CONNECT_COUNT+1):
        for r in range(CONNECT_COUNT-1, ROW_COUNT):
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
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0]==1 and action !=None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def quitgame():
    pygame.quit()
    quit()

def game_intro():
    pygame.mixer.music.play(-1)
    create_board()
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        textSurf, textRect = text_objects("Welcome to Connect 4", myfont)
        textRect.center = ((size[0]/2),(size[1]/2))
        screen.blit(textSurf, textRect)
        button("Play",200,550,100,50,GREEN,DARK_GREEN,game_loop)
        button("Quit",400,550,100,50,RED,DARK_RED,quitgame)

        pygame.display.update()
        clock.tick(15)

def game_win(winner):
    print("game win1")
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        textSurf, textRect = text_objects(("The winner is Player " + winner), myfont)
        textRect.center = ((size[0]/2),(size[1]/2))
        screen.blit(textSurf, textRect)
        button("Quit",400,550,100,50,RED,DARK_RED,quitgame)
        button("Play Again",200,550,100,50,GREEN,DARK_GREEN,game_loop)
#        pygame.mixer.music.stop()
        pygame.display.update()
        clock.tick(15)

        #game_intro()

def game_loop():
    pygame.mixer.music.play(-1)
    board = create_board()
    draw_board(board)
    game_over = False
    turn = 0
    pygame.display.update()

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)

                        if winning_move(board, 1):
                            game_over = True
                            pygame.time.delay(10)
                            winner = "1"
                            #quitgame()


                # # Ask for Player 2 Input
                else:               
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)

                        if winning_move(board, 2):
                            game_over = True
                            pygame.time.delay(10)
                            winner = "2"
                            #quitgame()


                print_board(board)
                draw_board(board)


                turn += 1
                turn = turn % 2
    game_win(winner)

board = create_board()
print_board(board)
pygame.init()
pygame.mixer.music.load("background_music.wav")
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
myfont = pygame.font.SysFont("monospace", 50)


game_intro()
print("intro")
game_loop()
print("gameloop")
game_win()
print("game win")
quitgame()
