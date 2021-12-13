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
                        screen.blit(ltr,(65+j*80, 60+i*80))
                    elif j == 0:
                        nbr=font.render(lines[i],0,DGREY)
                        screen.blit(nbr,(5+j*80, 5+i*80))
                else:
                    pygame.draw.rect(screen, DGREY, (j*80, i*80, 80, 80))
                    if i == 7:
                        ltr=font.render(columnes[j],0,GREY)
                        screen.blit(ltr,(65+j*80, 60+i*80))
                    if j == 0:
                        nbr=font.render(lines[i],0,GREY)
                        screen.blit(nbr,(5+j*80, 5+i*80))
        pygame.display.update()
    def get_piece(self,i,j):#*#obtener info de pieza
        (x,y)=(lines.index(j),columnes.index(i))
        if not board.position[x][y]==0:
            return board.position[x][y]
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
    def check_square(self,x,y):
        if board.get_piece(columnes[x],lines[y]).color==WHITE:
            for i in range (8):
                for j in range (8):
                    if not board.get_piece(columnes[i],lines[j])==0 and board.get_piece(columnes[i],lines[j]).color==BLACK:
                        if capture_posible(board.get_piece(columnes[i],lines[j]),[x,y],[i,j],turn):
                            print(True)
                            return True
        elif board.get_piece(columnes[x],lines[y]).color==BLACK:
            for i in range (8):
                for j in range (8):
                    if not board.get_piece(columnes[i],lines[j])==0 and board.get_piece(columnes[i],lines[j]).color==WHITE:
                        if capture_posible(board.get_piece(columnes[i],lines[j]),[x,y],[i,j],turn):
                            print(True)
                            return True

#*#*#piezas

class Piece:#*#*molde de piezas
    def __init__(self,img,color,piece,pos):#*#info general de piezas, 0 <=> nada, 1 <=> peon, 2 <=> caballo, 3 <=> alfil, 4 <=> torre, 5 <=> reina, 6 <=> rey
    #*# piezas blancas <=> valor_pieza x 2 - 1, piezas negras <=> valor_pieza x 2
        self.image = img
        self.pos = pos
        if color == WHITE or color == BLACK:
            self.color = color
        if piece>0 and piece<7:
            self.type = piece
    def move(self,new_pos,old_pos):#*#funcion mover pieza
        global turn, pos_K, pos_k, noturn
        if move_posible(self,new_pos,old_pos,turn):
            board.position[old_pos[0]][old_pos[1]]=0
            board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
            if self.color == WHITE:
                (turn,noturn)=(1,0)
                if self.type == 6:
                    pos_K=new_pos
            elif self.color == BLACK:
                (turn,noturn)=(0,1)
                if self.type == 6:
                    pos_k=new_pos
        elif lm_castle(new_pos,old_pos,turn):
            board.position[old_pos[0]][old_pos[1]]=0
            board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
            if new_pos[1] == 2:
                if self.color == WHITE:
                    (turn,noturn)=(1,0)
                    board.position[7][0]=0
                    board.position[7][3]=7
                    pos_K=new_pos
                else:
                    (turn,noturn)=(0,1)
                    board.position[0][0]=0
                    board.position[0][3]=8
                    pos_k=new_pos
            elif new_pos[1] == 6:
                if self.color == WHITE:
                    (turn,noturn)=(1,0)
                    board.position[7][7]=0
                    board.position[7][5]=7
                    pos_K=new_pos
                else:
                    (turn,noturn)=(0,1)
                    board.position[0][7]=0
                    board.position[0][5]=8
                    pos_k=new_pos
    def capture(self,new_pos,old_pos):
        global turn, pos_K, pos_k, noturn
        if capture_posible(self,new_pos,old_pos,turn):
            board.position[old_pos[0]][old_pos[1]]=0
            board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self.type,self.color)
            if self.color == WHITE:
                (turn,noturn)=(1,0)
                if self.type == 6:
                    pos_K=new_pos
            elif self.color == BLACK:
                (turn,noturn)=(0,1)
                if self.type == 6:
                    pos_k=new_pos

#*# movimientos legales

def lm_pawn(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 1 and t == 0:#blanco
        if new_pos[0] == old_pos[0]-1 and new_pos[1] == old_pos[1]:
            return True
        elif old_pos[0] == 6 and new_pos[0] == old_pos[0]-2 and new_pos[1]==old_pos[1]:
            return True
    elif board.position[old_pos[0]][old_pos[1]] == 2 and t == 1:#negro
        if new_pos[0] == old_pos[0]+1 and new_pos[1]==old_pos[1]:
            return True
        elif old_pos[0] == 1 and new_pos[0] == old_pos[0]+2 and new_pos[1]==old_pos[1]:
            return True
def lmc_knight(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 3 and t == 0:#blanco
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
    elif board.position[old_pos[0]][old_pos[1]] == 4 and t == 1:#negro
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
def lm_bishop(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 5 and t == 0:#blanco
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
    elif board.position[old_pos[0]][old_pos[1]] == 6 and t == 1:#negro
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
def lm_rook(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 7 and t == 0:#blanco
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
    elif board.position[old_pos[0]][old_pos[1]] == 8 and t == 1:#negro
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
                    if new_pos[0]==old_pos[0]+q*a and new_pos[1]==old_pos[1]+q*b and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                        return True
def lm_queen(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 9 and t == 0:#blanco
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
    elif board.position[old_pos[0]][old_pos[1]] == 10 and t == 1:#negro
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
def lm_king(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 11 and t == 0:#blanco
        for c in range (-1,2):
            for d in range (-1,2):
                if new_pos[0]==old_pos[0]+c and new_pos[1]==old_pos[1]+d:
                    if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                        return True
                    elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                        return True
    elif board.position[old_pos[0]][old_pos[1]] == 12 and t == 1:#negro
        for c in range (-1,2):
            for d in range (-1,2):
                if new_pos[0]==old_pos[0]+c and new_pos[1]==old_pos[1]+d:
                    if not board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                        return True
                    elif board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                        return True
def lm_castle(new_pos,old_pos,t):#*enroque
    if board.position[old_pos[0]][old_pos[1]] == 11 and t == 0:
        if rc_Q:
            if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]-2:
                if move_posible(R,[7,3],[7,0],turn):
                    return True
        if rc_K:
            if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]+2:
                if move_posible(R,[7,5],[7,7],turn):
                    return True
    elif board.position[old_pos[0]][old_pos[1]] == 12 and t == 1:
        if rc_q:
            if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]-2:
                if move_posible(r,[0,3],[0,0],turn):
                    return True
        if rc_k:
            if new_pos[0]==old_pos[0] and new_pos[1]==old_pos[1]+2:
                if move_posible(r,[0,5],[0,7],turn):
                    return True
def move_posible(self,new_pos,old_pos,t):#*#verificar si el movimiento es legal
    if board.position[new_pos[0]][new_pos[1]]==0:
        if self.type == 1:#*para el peon
            return lm_pawn(new_pos,old_pos,t)
        elif self.type == 2:#*para el caballo
            return lmc_knight(new_pos,old_pos,t)
        elif self.type == 3:#*para el alfil
            return lm_bishop(new_pos,old_pos,t)
        elif self.type == 4:#*para la torre
            return lm_rook(new_pos,old_pos,t)     
        elif self.type == 5:#*para la reina
            return lm_queen(new_pos,old_pos,t)
        elif self.type == 6:#*para el rey
            return lm_king(new_pos,old_pos,t)

#*# capturas legales

def lc_pawn(new_pos,old_pos,t):
    if board.position[old_pos[0]][old_pos[1]] == 1 and t == 0:#blanco
        if new_pos[0] == old_pos[0]-1:
            if new_pos[1] == old_pos[1]-1 or new_pos[1] == old_pos[1]+1:
                if board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                    return True
    elif board.position[old_pos[0]][old_pos[1]] == 2 and t == 1:#negro
        if new_pos[0] == old_pos[0]+1:
            if new_pos[1] == old_pos[1]-1 or new_pos[1] == old_pos[1]+1:
                if board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                    return True
def capture_posible(self,new_pos,old_pos,t):
    if self.type == 1:#*para el peon
        return lc_pawn(new_pos,old_pos,t)
    elif self.type == 2:#*para el caballo
        return lmc_knight(new_pos,old_pos,t)
    elif self.type == 3:#*para el alfil
        return lm_bishop(new_pos,old_pos,t)
    elif self.type == 4:#*para la torre
        return lm_rook(new_pos,old_pos,t)     
    elif self.type == 5:#*para la reina
        return lm_queen(new_pos,old_pos,t)
    elif self.type == 6:#*para el rey
        return lm_king(new_pos,old_pos,t)


#*#*codigo de piezas e imagenes

board = Board()
lines = ['8','7','6','5','4','3','2','1']
columnes = ['a','b','c','d','e','f','g','h']

P = pygame.image.load("Pawn0.png").convert_alpha()
p = pygame.image.load("Pawn1.png").convert_alpha()
N = pygame.image.load("Knight0.png").convert_alpha()
n = pygame.image.load("Knight1.png").convert_alpha()
B = pygame.image.load("Bishop0.png").convert_alpha()
b = pygame.image.load("Bishop1.png").convert_alpha()
R = pygame.image.load("Rook0.png").convert_alpha()
r = pygame.image.load("Rook1.png").convert_alpha()
Q = pygame.image.load("Queen0.png").convert_alpha()
q = pygame.image.load("Queen1.png").convert_alpha()
K = pygame.image.load("King0.png").convert_alpha()
k = pygame.image.load("King1.png").convert_alpha()
images = [P,p,N,n,B,b,R,r,Q,q,K,k]

pieces = []
for l in range (8):
    for s in range(8):
        ps = board.position[l][s]
        if not ps==0:
            if ps % 2 == 1:
                pc = Piece(images[ps-1],WHITE,int((ps+1)/2),[columnes[l],lines[s]])
            else:
                pc = Piece(images[ps-1],BLACK,int(ps/2),[columnes[l],lines[s]])
            pieces.append(pc)
            board.position[l][s] = pc

#*#*variables en posicion inicial e inicio grafico

board.reset()
rc_Q=True
rc_K=True
rc_q=True
rc_k=True
running = True
turn = 0
noturn = 1
check=[False,None,None]
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
                                else:
                                    piece_raised[0].capture([j,i],piece_raised[1])
                                if capture_posible(piece_raised[0],pos_K,[j,i],noturn) or capture_posible(piece_raised[0],pos_k,[j,i],noturn):
                                    check=[True,piece_raised[0],[j,i]]
                                    print(check)
                                else:
                                    check=[False,None,None]
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
                                piece_raised = [0]
                board.reset()
