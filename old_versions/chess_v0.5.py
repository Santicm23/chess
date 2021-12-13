#*#*#inicio y variables fundamentales
import pygame
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,640))

#*#*#colores y fuentes

font = pygame.font.SysFont(None, 30)
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
    def __init__(self,img,color,piece):#*#info general de piezas, 0 <=> nada, 1 <=> peon, 2 <=> caballo, 3 <=> alfil, 4 <=> torre, 5 <=> reina, 6 <=> rey
    #*# piezas blancas <=> valor_pieza x 2 - 1, piezas negras <=> valor_pieza x 2
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
                if not check_w:
                    board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
                    turn=1
                else:
                    if self.type == 6:
                        board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
                        turn=1
            elif self.color == BLACK:
                if not check_b:
                    board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
                    turn=0
                else:
                    if self.type == 6:
                        board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
                        turn=1
                    
        elif self.lm_castle(new_pos,old_pos):
            board.position[old_pos[0]][old_pos[1]]=0
            board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
            if new_pos[1] == 2:
                if self.color == WHITE:
                    turn=1
                    board.position[7][0]=0
                    board.position[7][3]=7
                else:
                    turn=0
                    board.position[0][0]=0
                    board.position[0][3]=8
            elif new_pos[1] == 6:
                if self.color == WHITE:
                    turn=1
                    board.position[7][7]=0
                    board.position[7][5]=7
                else:
                    turn=0
                    board.position[0][7]=0
                    board.position[0][5]=8
    def capture(self,new_pos,old_pos):
        global turn
        if self.capture_posible(new_pos,old_pos):
            board.position[old_pos[0]][old_pos[1]]=0
            board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
            if self.color == WHITE:
                turn=1
            elif self.color == BLACK:
                turn=0

#*# movimientos legales

    def lm_pawn(self,new_pos,old_pos):
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
    def lmc_knight(self,new_pos,old_pos):
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
                            if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                                return True
                            elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                                return True
        elif board.position[old_pos[0]][old_pos[1]] == 4 and turn == 1:#negro
            for k0 in range (2):
                for k1 in range (2):
                    for k2 in range (2):
                        if k0==0:
                            (a,b)=(1,2)
                        else:
                            (a,b)=(2,1)
                        if k1==0:
                            a=a*-1
                            b=b*-1
                        if k2==0:
                            a=a*-1
                        if new_pos[0]+a==old_pos[0] and new_pos[1]+b==old_pos[1]:
                            if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                                return True
                            elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                                return True
    def lm_bishop(self,new_pos,old_pos):
        if board.position[old_pos[0]][old_pos[1]] == 5 and turn == 0:#blanco
            for c in range (-1,2,2):
                for d in range (-1,2,2):
                    q=1
                    while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                            return True
                        q=q+1
                    if old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and not board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif board.position[old_pos[0]][old_pos[1]] == 6 and turn == 1:#negro
            for c in range (-1,2,2):
                for d in range (-1,2,2):
                    q=1
                    while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                            return True
                        q=q+1
                    if old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and not board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
    def lm_rook(self,new_pos,old_pos):
        if board.position[old_pos[0]][old_pos[1]] == 7 and turn == 0:#blanco
            for i in range (2):
                for j in range (2):
                    if i==0:
                        if j==0:
                            (a,b)=(1,0)
                        else:
                            (a,b)=(-1,0)
                    else:
                        if j==0:
                            (a,b)=(0,1)
                        else:
                            (a,b)=(0,-1)
                    q=1
                    while old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                        if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b:
                            return True
                        q=q+1
                    if old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and not board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                        if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif board.position[old_pos[0]][old_pos[1]] == 8 and turn == 1:#negro
            for i in range (2):
                for j in range (2):
                    if i==0:
                        if j==0:
                            (a,b)=(1,0)
                        else:
                            (a,b)=(-1,0)
                    else:
                        if j==0:
                            (a,b)=(0,1)
                        else:
                            (a,b)=(0,-1)
                    q=1
                    while old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                        if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b:
                            return True
                        q=q+1
                    if old_pos[0]+q*a>-1 and old_pos[0]+q*a<8 and old_pos[1]+q*b>-1 and old_pos[1]+q*b<8 and not board.position[old_pos[0]+q*a][old_pos[1]+q*b] == 0:
                        if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
    def lm_queen(self,new_pos,old_pos):
        if board.position[old_pos[0]][old_pos[1]] == 9 and turn == 0:#blanco
            for c in range (-1,2):
                for d in range (-1,2):
                    q=1
                    while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                            return True
                        q=q+1
                    if old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and not board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif board.position[old_pos[0]][old_pos[1]] == 10 and turn == 1:#negro
            for c in range (-1,2):
                for d in range (-1,2):
                    q=1
                    while old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d:
                            return True
                        q=q+1
                    if old_pos[0]+q*c>-1 and old_pos[0]+q*c<8 and old_pos[1]+q*d>-1 and old_pos[1]+q*d<8 and not board.position[old_pos[0]+q*c][old_pos[1]+q*d] == 0:
                        if new_pos[0]==old_pos[0]+q*c and new_pos[1]==old_pos[1]+q*d and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
    def lm_king(self,new_pos,old_pos):
        if board.position[old_pos[0]][old_pos[1]] == 11 and turn == 0:#blanco
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==old_pos[0]+c and new_pos[1]==old_pos[1]+d:
                        pos_K=new_pos
                        if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
                        elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                            return True
        elif board.position[old_pos[0]][old_pos[1]] == 12 and turn == 1:#negro
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==old_pos[0]+c and new_pos[1]==old_pos[1]+d:
                        pos_k=new_pos
                        if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
                        elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                            return True
    def lm_castle(self,new_pos,old_pos):#*enroque
        if board.position[new_pos[0]][new_pos[1]]==0 and self.type == 6:
            if board.position[old_pos[0]][old_pos[1]] == 11 and turn == 0:
                if rc_Q:
                    if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]-2:
                        if R.move_posible([7,3],[7,0]):
                            pos_K=new_pos
                            return True
                if rc_K:
                    if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]+2:
                        if R.move_posible([7,5],[7,7]):
                            pos_K=new_pos
                            return True
            elif board.position[old_pos[0]][old_pos[1]] == 12 and turn == 1:
                if rc_q:
                    if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]-2:
                        if r.move_posible([0,3],[0,0]):
                            pos_k=new_pos
                            return True
                if rc_k:
                    if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]+2:
                        if r.move_posible([0,5],[0,7]):
                            pos_k=new_pos
                            return True
    def move_posible(self,new_pos,old_pos):#*#verificar si el movimiento es legal
        if board.position[new_pos[0]][new_pos[1]]==0:
            if self.type == 1:#*para el peon
                return self.lm_pawn(new_pos,old_pos)
            elif self.type == 2:#*para el caballo
                return self.lmc_knight(new_pos,old_pos)
            elif self.type == 3:#*para el alfil
                return self.lm_bishop(new_pos,old_pos)
            elif self.type == 4:#*para la torre
                return self.lm_rook(new_pos,old_pos)     
            elif self.type == 5:#*para la reina
                return self.lm_queen(new_pos,old_pos)
            elif self.type == 6:#*para el rey
                return self.lm_king(new_pos,old_pos)

#*# capturas legales

    def lc_pawn(self,new_pos,old_pos):
        if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
            if board.position[old_pos[0]][old_pos[1]] == 1 and turn == 0:#blanco
                if new_pos[0] == old_pos[0]-1:
                    if new_pos[1] == old_pos[1]-1 or new_pos[1] == old_pos[1]+1:
                        if board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
            elif board.position[old_pos[0]][old_pos[1]] == 2 and turn == 1:#negro
                if new_pos[0] == old_pos[0]+1:
                    if new_pos[1] == old_pos[1]-1 or new_pos[1] == old_pos[1]+1:
                        if board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
    def capture_posible(self,new_pos,old_pos):
        if self.type == 1:#*para el peon
            return self.lc_pawn(new_pos,old_pos)
        elif self.type == 2:#*para el caballo
            return self.lmc_knight(new_pos,old_pos)
        elif self.type == 3:#*para el alfil
            return self.lm_bishop(new_pos,old_pos)
        elif self.type == 4:#*para la torre
            return self.lm_rook(new_pos,old_pos)     
        elif self.type == 5:#*para la reina
            return self.lm_queen(new_pos,old_pos)
        elif self.type == 6:#*para el rey
            return self.lm_king(new_pos,old_pos)

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
lines=['8','7','6','5','4','3','2','1']
columnes=['a','b','c','d','e','f','g','h']

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
                    if i == 7:
                        ltr=font.render(columnes[j],0,DGREY)
                        screen.blit(ltr,(5+j*80, 5+i*80))
                    elif j == 0:
                        nbr=font.render(lines[i],0,DGREY)
                        screen.blit(nbr,(5+j*80, 5+i*80))
                else:
                    pygame.draw.rect(screen, DGREY, (j*80, i*80, 80, 80))
                    if i == 7:
                        ltr=font.render(columnes[j],0,GREY)
                        screen.blit(ltr,(5+j*80, 5+i*80))
                    elif j == 0:
                        nbr=font.render(lines[i],0,GREY)
                        screen.blit(nbr,(5+j*80, 5+i*80))
        pygame.display.update()
    def get_piece(self,i,j):#*#obtener info de pieza
        (x,y)=(lines.index(j),columnes.index(i))
        if not board.position[x][y]==0:
            return pieces[board.position[x][y]-1]
        else:
            return 0
    def set_piece(self,i,j,piece,color):#*#colocar pieza
        (x,y)=(lines.index(j),columnes.index(i))
        if color == WHITE:
            board.position[x][y] = piece*2-1
        elif color == BLACK:
            board.position[x][y] = piece*2
        else:
            board.position[x][y] = 0
    def reset(self):#*#reiniciar la parte grafica
        board.draw_board()
        for j in range (8):
            for i in range (8):
                if not board.position[j][i]==0:
                    screen.blit(board.get_piece(columnes[i],lines[j]).image,(i*80,j*80))
        pygame.display.update()
    def reset_mouse(self,x,y):
        pygame.display.update()

#*#*variables en posicion inicial e inicio grafico

board = Board()
board.reset()
rc_Q=True
rc_K=True
rc_q=True
rc_k=True
running = True
turn = 0
check_w=False
check_b=False
pos_K=[7,4]
pos_k=[0,4]
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
                                piece_raised = [board.get_piece(columnes[i],lines[j]),[j,i]]#saber cual pieza y su posicion
                                if not board.position[j][i]==0:
                                    if board.get_piece(columnes[i],lines[j]).color == color_turn[turn]:#saber cuando la pieza este en el aire
                                        screen.blit(r_sq,(i*80,j*80))
                                        screen.blit(board.get_piece(columnes[i],lines[j]).image,(i*80,j*80))
                                        pygame.display.update()
            else:#*colocar pieza(2° click)
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                if board.position[j][i] == 0:
                                    piece_raised[0].move([j,i],piece_raised[1])
                                    if board.get_piece('e','1') == 0 or not board.get_piece('e','1').type == 6:
                                        (rc_Q,rc_K) = (False,False)
                                    elif board.get_piece('e','8') == 0 or not board.get_piece('e','8').type == 6:
                                        (rc_q,rc_k) = (False,False)
                                    if board.get_piece('a','8') == 0 or not board.get_piece('a','8').type == 4:
                                        rc_q = False
                                    elif board.get_piece('h','8') == 0 or not board.get_piece('h','8').type == 4:
                                        rc_k = False
                                    elif board.get_piece('a','1') == 0 or not board.get_piece('a','1').type == 4:
                                        rc_Q = False
                                    elif board.get_piece('h','1') == 0 or not board.get_piece('h','1').type == 4:
                                        rc_K = False
                                else:
                                    piece_raised[0].capture([j,i],piece_raised[1])
                                if piece_raised[0].capture_posible(pos_K,[j,i]):
                                    check_w=True
                                elif piece_raised[0].capture_posible(pos_k,[j,i]):
                                    check_b=True
                                piece_raised = [0]
                board.reset()
