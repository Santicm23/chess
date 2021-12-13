#*#*#inicio y variables fundamentales
import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,640))
running = True
turn = 0

#*#*#colores y fuentes

font = pygame.font.SysFont('chalkduster.ttf', 50)
BROWN = (139,69,19)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (105,105,105)
DGREY = (169,169,169)
BEIGE = (255,206,158,255)
r_sq = pygame.image.load("raised_square.png").convert_alpha()
color_turn=[WHITE,BLACK]

#*#*#piezas

class Piece:#*#*molde de piezas
    def __init__(self,img,color,piece):#*#info general de piezas
        self.image = img
        if color == WHITE or color == BLACK:
            self.color = color
        if piece>0 and piece<7:
            self.type = piece
    def move(self,new_pos,old_pos):#*#funcion mover pieza
        global turn
        if self.move_posible(new_pos,old_pos):
            board.position[old_pos[0]][old_pos[1]]=0
            if self.color == WHITE:
                board.position[new_pos[0]][new_pos[1]]=2*self.type-1
                turn=1
            else:
                board.position[new_pos[0]][new_pos[1]]=2*self.type
                turn=0
    def move_posible(self,new_pos,old_pos):#*#verificar si el movimiento es legal
        if board.position[new_pos[0]][new_pos[1]]==0:
            if self.type == 1:#*para el peon
                if board.position[old_pos[0]][old_pos[1]] == 1 and turn == 0:#blanco
                    if new_pos[0] == old_pos[0]-1 and new_pos[1] == old_pos[1]:
                        return True
                    elif old_pos[0] == 6 and new_pos[0] == old_pos[0]-2 and new_pos[1]==old_pos[1]:
                        return True
                elif board.position[old_pos[0]][old_pos[1]] == 2 and turn == 1:#negro
                    if new_pos[0] == old_pos[0]+1 and new_pos[1]==old_pos[1]:
                        return True
                    elif old_pos[0] == 1 and new_pos[0] == old_pos[0]+2 and new_pos[1]==old_pos[1]:
                        return True
            elif self.type == 2:#*para el caballo
                if board.position[old_pos[0]][old_pos[1]] == 3 and turn == 0:#blanco
                    for k in range (2):
                        for k1 in range (2):
                            for k2 in range (2):
                                if k==0:
                                    (a,b)=(1,2)
                                else:
                                    (a,b)=(2,1)
                                if k1==0:
                                    a=a*-1
                                    b=b*-1
                                if k2==0:
                                    a=a*-1
                                if new_pos[0]+a == old_pos[0] and new_pos[1]+b == old_pos[1]:
                                    return True
                elif board.position[old_pos[0]][old_pos[1]] == 4 and turn == 1:#negro
                    for k in range (2):
                        for k1 in range (2):
                            for k2 in range (2):
                                if k==0:
                                    (a,b)=(1,2)
                                else:
                                    (a,b)=(2,1)
                                if k1==0:
                                    a=a*-1
                                    b=b*-1
                                if k2==0:
                                    a=a*-1
                                if new_pos[0]+a==old_pos[0] and new_pos[1]+b==old_pos[1]:
                                    return True
            elif self.type == 3:#*para el alfil
                if board.position[old_pos[0]][old_pos[1]] == 5 and turn == 0:#blanco
                    for c in range (-1,2,2):
                        for d in range (-1,2,2):
                            q=1
                            while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                                if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                                    return True
                                q=q+1
                elif board.position[old_pos[0]][old_pos[1]] == 6 and turn == 1:#negro
                    for c in range (-1,2,2):
                        for d in range (-1,2,2):
                            q=1
                            while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                                if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                                    return True
                                q=q+1
            elif self.type == 4:#*para la torre
                if board.position[old_pos[0]][old_pos[1]] == 7 and turn == 0:#blanco
                    for i in range (2):
                        for j in range (2):
                            if i==0:
                                if j==0:
                                    a=1
                                    b=0
                                else:
                                    a=-1
                                    b=0
                            else:
                                if j==0:
                                    a=0
                                    b=1
                                else:
                                    a=0
                                    b=-1
                            q=1
                            while old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                                if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b:
                                    return True
                                q=q+1
                elif board.position[old_pos[0]][old_pos[1]] == 8 and turn == 1:
                    for i in range (2):
                        for j in range (2):
                            if i==0:
                                if j==0:
                                    a=1
                                    b=0
                                else:
                                    a=-1
                                    b=0
                            else:
                                if j==0:
                                    a=0
                                    b=1
                                else:
                                    a=0
                                    b=-1
                            q=1
                            while old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                                if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b:
                                    return True
                                q=q+1     
            elif self.type == 5:#*para la reina
                if board.position[old_pos[0]][old_pos[1]] == 9 and turn == 0:#blanco
                    for c in range (-1,2):
                        if c==0:
                            for d in range (-1,2):
                                q=1
                        else:
                            q=1
                            d=0
                            while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                                if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                                    return True
                                q=q+1
                elif board.position[old_pos[0]][old_pos[1]] == 10 and turn == 1:#negro
                    for c in range (-1,2):
                        for d in range (-1,2):
                            q=1
                            while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                                if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                                    return True
                                q=q+1
            elif self.type == 6:#*para la reina
                if board.position[old_pos[0]][old_pos[1]] == 11 and turn == 0:#blanco
                    for c in range (-1,2):
                        if c==0:
                            for d in range (-1,2):
                                q=1
                        else:
                            q=1
                            d=0
                            while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                                if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                                    return True
                                q=q+1
        
#*#*codigo de piezas e imagenes

P = Piece(pygame.image.load("Pawn0.png").convert_alpha(),WHITE,1)
p = Piece(pygame.image.load("Pawn1.png").convert_alpha(),BLACK,1)
N = Piece(pygame.image.load("Knight0.png").convert_alpha(),WHITE,2)
n = Piece(pygame.image.load("Knight1.png").convert_alpha(),BLACK,2)
B = Piece(pygame.image.load("Bishop0.png").convert_alpha(),WHITE,3)
b = Piece(pygame.image.load("Bishop1.png").convert_alpha(),BLACK,3)
R = Piece(pygame.image.load("Rook0.png").convert_alpha(),WHITE,4)
r = Piece(pygame.image.load("Rook1.png").convert_alpha(),BLACK,4)
Q = Piece(pygame.image.load("Queen0.png").convert_alpha(),WHITE,5)
q = Piece(pygame.image.load("Queen1.png").convert_alpha(),BLACK,5)
K = Piece(pygame.image.load("King0.png").convert_alpha(),WHITE,6)
k = Piece(pygame.image.load("King1.png").convert_alpha(),BLACK,6)
pieces=[P,p,N,n,B,b,R,r,Q,q,K,k]

#*#*#tablero
class Board:#*#*molde del tablero
    def __init__(self):#*#posicion por defecto
        self.position=[[ 8, 4, 6,10,12, 6, 4, 8],
                       [ 2, 2, 2, 2, 2, 2, 2, 2],
                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 0, 0, 0, 0, 0, 0, 0, 0],
                       [ 1, 1, 1, 1, 1, 1, 1, 1],
                       [ 7, 3, 5, 9,11, 5, 3, 7]]
    def draw_board (self):#*#tablero grafico
        for i in range (8):
            for j in range (8):
                if i % 2 and j % 2 or (i-1) % 2 and (j-1) % 2:
                    pygame.draw.rect(screen, GREY, (j*80, i*80, 80, 80))
                else:
                    pygame.draw.rect(screen, DGREY, (j*80, i*80, 80, 80))
        pygame.display.update()
    def get_piece(self,i,j):#*#obtener info de pieza
        if not board.position[j][i]==0:
            return pieces[board.position[j][i]-1]
        else:
            return 0
    def set_piece(self,i,j,piece):#*#colocar pieza (en proceso)
        board.position[j][i]=piece+1
    def reset(self):#*#reiniciar la parte grafica
        board.draw_board()
        for j in range (8):
            for i in range (8):
                if not board.position[j][i]==0:
                    screen.blit(board.get_piece(i,j).image,(i*80,j*80))
        pygame.display.update()
    def reset_mouse(self,x,y):
        pygame.display.update()

#*#*variable del tablero e inicio grafico del juego

board = Board()
board.reset()
pygame.display.update()

#*#*#codigo y funcionamiento del juego

piece_raised = [0]
while running:#*#*bucle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#*#correcto apagado
            running = False
        if event.type == MOUSEBUTTONDOWN:#*#click
            Pos = event.pos
            if piece_raised[0] == 0:#*levantar pieza (1° click)
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                piece_raised = [board.get_piece(i,j),[j,i]]
                                if not board.position[j][i]==0:
                                    if board.get_piece(i,j).color == color_turn[turn]:#saber cuando la pieza este en el aire
                                        screen.blit(r_sq,(i*80,j*80))
                                        screen.blit(board.get_piece(i,j).image,(i*80,j*80))
                                        pygame.display.update()
            else:#*colocar pieza(2° click)
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                piece_raised[0].move([j,i],piece_raised[1])
                                piece_raised = [0]
                board.reset()
