#*#*#inicio y variables fundamentales
import pygame
from pygame.locals import *
import time
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
r_sq = pygame.image.load("imgs/raised_square.png").convert_alpha()
mp = pygame.image.load("imgs/mp.png").convert_alpha()
cp = pygame.image.load("imgs/cp.png").convert_alpha()
ms_mp = pygame.image.load("imgs/ms_mp.png").convert_alpha()
color_turn=[WHITE,BLACK]

#*#*#tablero

class Board:#*#*molde del tablero
    def __init__(self,brd):#*#posicion con sus piezas
        self.position = brd

    def draw_board (self):#*#tablero grafico
        for i in range (8):
            for j in range (8):
                board.reset_sq((i,j))
        pygame.display.update()

    def get_piece(self,i,j):#*#obtener info de pieza
        (x,y) = (lines.index(j),columnes.index(i))
        return self.position[x][y]
        
    def set_piece(self,i,j,piece):#*#colocar pieza
        (x,y) = (lines.index(j),columnes.index(i))
        piece.pos = [x,y]
        self.position[x][y] = piece
            
    def reset(self):#*#reiniciar la parte grafica
        self.draw_board()
        for j in range (8):
            for i in range (8):
                if not self.position[j][i] == 0:
                    screen.blit (self.get_piece(columnes[i],lines[j]).image,(i*80,j*80))
        pygame.display.update()
        
    def show_lm(self,piece):#*#mostrar jugadas posibles con la pieza seleccionada
        for i in range(8):
            for j in range(8):
                if move_posible(piece,[i,j],turn,self) or lm_castle(piece,[i,j],turn,self):
                    for m in piece.lm:
                        if m == [i,j]:
                            screen.blit(mp,(j*80+30,i*80+30))
                elif capture_posible(piece,[i,j],turn,self):
                    if not self.position[i][j] == 0:
                        if check[0]:
                            if piece.type == 6 or [i,j] == check[1].pos:
                                for m in piece.lm:
                                    if m == [i,j]:
                                        screen.blit(cp,(j*80,i*80))
                        elif not check[0]:
                            for m in piece.lm:
                                if m == [i,j]:
                                    screen.blit(cp,(j*80,i*80))
                if en_passant(piece,[i,j],turn,self):
                    if check[0]:
                        if [i,j] == check[1].pos:
                            screen.blit(mp,(j*80+30,i*80+30))
                    elif not check[0]:
                        screen.blit(mp,(j*80+30,i*80+30))
    
    def reset_lm(self):
        for wp in Wpieces:
            wp.rsrch_lm(self)
        for bp in Bpieces:
            bp.rsrch_lm(self)
    
    def reset_sq(self,pos):#*#repinta una sola casilla del tablero
        xp = pos [0]
        yp = pos [1]
        if xp % 2 and yp % 2 or (xp-1) % 2 and (yp-1) % 2:
            pygame.draw.rect(screen, GREY, (yp*80, xp*80, 80, 80))
            if xp == 7:
                ltr=font.render(columnes[yp],0,DGREY)
                screen.blit(ltr,(65+yp*80, 60+xp*80))
            elif yp == 0:
                nbr=font.render(lines[xp],0,DGREY)
                screen.blit(nbr,(5+yp*80, 5+xp*80))
        else:
            pygame.draw.rect(screen, DGREY, (yp*80, xp*80, 80, 80))
            if xp == 7:
                ltr=font.render(columnes[yp],0,GREY)
                screen.blit(ltr,(65+yp*80, 60+xp*80))
            if yp == 0:
                nbr=font.render(lines[xp],0,GREY)
                screen.blit(nbr,(5+yp*80, 5+xp*80))
    
    def reset_zone(self,pos):
        for i in range(1,7):
            for j in range(1,7):
                if pos[0]>40+i*80 and pos[0]<120+i*80:
                    if pos[1]>40+j*80 and pos[1]<120+j*80:
                        board.reset_sq((j,i))
                        board.reset_sq((j+1,i))
                        board.reset_sq((j,i+1))
                        board.reset_sq((j+1,i+1))

    def check(self,t):#*#Jaque
        tc=[False,None]
        counter=0
        if color_turn[t] == WHITE:
            for piece in Wpieces:
                if capture_posible(piece,k.pos,t,self):
                    tc=[True,piece]
                    counter=counter+1
        else:
            for piece in Bpieces:
                if capture_posible(piece,K.pos,t,self):
                    tc=[True,piece]
                    counter=counter+1
        if counter>1:
            tc.append(True)
        else:
            tc.append(False)
        return tc

    def next_pos_check(self,new_pos,piece):#*#calcular si en la jugada designada el rey es capturable
        (x,y) = new_pos
        new_b = Board(self.position,self.wp,self.bp)
        new_b.position[piece.pos[0]][piece.pos[1]] = 0
        new_b.set_piece(columnes[y],lines[x],piece)
        next_check = new_b.check(turn)
        if next_check[0]:
            return True
    
    def promote(self,new_pos,color):#*#mostrar recuadro de pizas para coronar
        (c,r) = new_pos
        if color == BLACK:
            pygame.draw.rect(screen, WHITE, (r*80, c*80, 80, 320))
            screen.blit (Q_img,(r*80,c*80))
            screen.blit (N_img,(r*80,c*80+80))
            screen.blit (R_img,(r*80,c*80+160))
            screen.blit (B_img,(r*80,c*80+240))

        else:
            pygame.draw.rect(screen, WHITE, (r*80, c*80-240, 80, 320))
            screen.blit (q_img,(r*80,c*80))
            screen.blit (n_img,(r*80,c*80-80))
            screen.blit (r_img,(r*80,c*80-160))
            screen.blit (b_img,(r*80,c*80-240))
        pygame.display.update()
    
    def game_over(self):
        k=0
        if color_turn[turn] == WHITE:
            for p in Wpieces:
                if len(p.lm) == 0:
                    k=k+1
                if k == len(Wpieces):
                    return True
        else:
            for p in Bpieces:
                if len(p.lm) == 0:
                    k=k+1
                if k == len(Bpieces):
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
        self.lm = []
            
    def move(self,new_pos,new_board):#*#funcion mover pieza
        global turn, noturn, check, en_pssnt
        if not new_pos == self.pos:
            distance_x = (new_pos[0] - self.pos[0])/frames
            distance_y = (new_pos[1] - self.pos[1])/frames
            py = self.pos[0]
            px = self.pos[1]
            cstl = False
            if turn == 0:
                ep = 1
            else:
                ep = -1
            if lm_castle(self,new_pos,turn,new_board) and not check[0]:
                cstl = True
            for m in self.lm:
                if m == new_pos:
                    if self.type == 1 and self.pos[0]-new_pos[0] == ep*2:
                        en_pssnt = [True,[new_pos[0]+ep,new_pos[1]]]
                    else:
                        en_pssnt = [False,None]
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    for i in range (frames):
                        time.sleep(df)
                        new_board.reset_zone((px*80,py*80))
                        py = self.pos[0] + distance_x * i
                        px = self.pos[1] + distance_y * i
                        screen.blit (self.image,(px*80,py*80))
                        pygame.display.update()
                    new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                    if self.color == WHITE:
                        (turn,noturn)=(1,0)
                    elif self.color == BLACK:
                        (turn,noturn)=(0,1)
        if cstl:
            if new_pos[1] == 2:
                if self.color == WHITE:
                    (turn,noturn) = (1,0)
                    new_board.set_piece(columnes[3],lines[7],new_board.position[7][0])
                    new_board.position[7][0] = 0
                else:
                    (turn,noturn) = (0,1)
                    new_board.set_piece(columnes[3],lines[0],new_board.position[0][0])
                    new_board.position[0][0] = 0
            elif new_pos[1] == 6:
                if self.color == WHITE:
                    (turn,noturn) = (1,0)
                    new_board.set_piece(columnes[5],lines[7],new_board.position[7][7])
                    new_board.position[7][7] = 0
                else:
                    (turn,noturn) = (0,1)
                    new_board.set_piece(columnes[5],lines[0],new_board.position[0][7])
                    new_board.position[0][7] = 0
                    
    def capture(self,new_pos,new_board):#*#funcion capturar pieza
        global turn, noturn, check, en_pssnt
        if not new_pos == self.pos:
            distance_x = (new_pos[0] - self.pos[0])/frames
            distance_y = (new_pos[1] - self.pos[1])/frames
            py = self.pos[0]
            px = self.pos[1]
            for m in self.lm:
                if m == new_pos:
                    pd = new_board.position[new_pos[0]][new_pos[1]]
                    if en_pssnt and en_passant(self,new_pos,turn,new_board):
                        pd = new_board.position[self.pos[0]][new_pos[1]]
                        new_board.position[self.pos[0]][new_pos[1]] = 0
                    en_pssnt = [False,None]
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    for i in range (frames):
                        time.sleep(df)
                        new_board.reset_zone((px*80,py*80))
                        py = self.pos[0] + distance_x * i
                        px = self.pos[1] + distance_y * i
                        screen.blit (self.image,(px*80,py*80))
                        pygame.display.update()
                    new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                    if self.color == WHITE:
                        (turn,noturn)=(1,0)
                        del Bpieces[Bpieces.index(pd)]
                    elif self.color == BLACK:
                        (turn,noturn)=(0,1)
                        del Wpieces[Wpieces.index(pd)]
    
    def rsrch_lm(self,new_board):#*#calcular jugadas posibles
        (y,x) = self.pos
        moves = []
        for i in range (8):
            for j in range(8):
                if not self == 0 and move_posible(self,[i,j],turn,new_board) or lm_castle(self,[i,j],turn,new_board):
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[j],lines[i],self)
                    ilegal = new_board.check(noturn)
                    if not ilegal[0]:
                        moves.append([i,j])
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[x],lines[y],self)
                elif not self == 0 and capture_posible(self,[i,j],turn,new_board): 
                    if not new_board.position[i][j] == 0:
                        pd = new_board.position[i][j]
                        new_board.position[self.pos[0]][self.pos[1]] = 0
                        new_board.set_piece(columnes[j],lines[i],self)
                        ilegal = new_board.check(noturn)
                        if not ilegal[0]:
                            moves.append([i,j])
                        new_board.set_piece(columnes[x],lines[y],self)
                        new_board.set_piece(columnes[j],lines[i],pd)
                if not self == 0 and en_passant(self,[i,j],turn,new_board):
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[j],lines[i],self)
                    ilegal = new_board.check(noturn)
                    if not ilegal[0]:
                        moves.append([i,j])
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[x],lines[y],self)
        self.lm = moves

#*# movimientos legales

def lm_pawn(self,new_pos,t,new_board):
    if not new_board.position[self.pos[0]][self.pos[1]] == 0 and new_board.position[self.pos[0]][self.pos[1]].type == 1:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            if new_pos[0] == self.pos[0]-1 and new_pos[1] == self.pos[1]:
                return True
            elif self.pos[0] == 6 and new_pos[0] == self.pos[0]-2 and new_pos[1] == self.pos[1] and new_board.position[self.pos[0]-1][self.pos[1]] == 0:
                return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if new_pos[0] == self.pos[0]+1 and new_pos[1] == self.pos[1]:
                return True
            elif self.pos[0] == 1 and new_pos[0] == self.pos[0]+2 and new_pos[1] == self.pos[1] and new_board.position[self.pos[0]+1][self.pos[1]] == 0:
                return True
def lmc_knight(self,new_pos,t,new_board):
    if new_board.position[self.pos[0]][self.pos[1]].type == 2:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
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
                        if new_pos[0]+a == self.pos[0] and new_pos[1]+b == self.pos[1]:
                            if not  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                                return True
                            elif new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                                return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
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
                        if new_pos[0]+a==self.pos[0] and new_pos[1]+b==self.pos[1]:
                            if not  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                                return True
                            elif new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                                return True
def lm_bishop(self,new_pos,t,new_board):
    if new_board.position[self.pos[0]][self.pos[1]].type == 3:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            for c in range (-1,2,2):
                for d in range (-1,2,2):
                    q=1
                    while self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d:
                            return True
                        q=q+1
                    if self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and not new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            for c in range (-1,2,2):
                for d in range (-1,2,2):
                    q=1
                    while self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d:
                            return True
                        q=q+1
                    if self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and not new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
def lm_rook(self,new_pos,t,new_board):
    if not new_board.position[self.pos[0]][self.pos[1]] == 0 and new_board.position[self.pos[0]][self.pos[1]].type == 4:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
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
                    while self.pos[0]+q*a>-1 and self.pos[0]+q*a<8 and self.pos[1]+q*b>-1 and self.pos[1]+q*b<8 and new_board.position[self.pos[0]+q*a][self.pos[1]+q*b] == 0:
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b:
                            return True
                        q=q+1
                    if self.pos[0]+q*a>-1 and self.pos[0]+q*a<8 and self.pos[1]+q*b>-1 and self.pos[1]+q*b<8 and not new_board.position[self.pos[0]+q*a][self.pos[1]+q*b] == 0:
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
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
                    while self.pos[0]+q*a>-1 and self.pos[0]+q*a<8 and self.pos[1]+q*b>-1 and self.pos[1]+q*b<8 and new_board.position[self.pos[0]+q*a][self.pos[1]+q*b] == 0:
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b:
                            return True
                        q=q+1
                    if self.pos[0]+q*a>-1 and self.pos[0]+q*a<8 and self.pos[1]+q*b>-1 and self.pos[1]+q*b<8 and not new_board.position[self.pos[0]+q*a][self.pos[1]+q*b] == 0:
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b and  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
def lm_queen(self,new_pos,t,new_board):
    if new_board.position[self.pos[0]][self.pos[1]].type == 5:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            for c in range (-1,2):
                for d in range (-1,2):
                    q=1
                    while self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d:
                            return True
                        q=q+1
                    if self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and not new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            for c in range (-1,2):
                for d in range (-1,2):
                    q=1
                    while self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d:
                            return True
                        q=q+1
                    if self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and not new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
def lm_king(self,new_pos,t,new_board):
    if new_board.position[self.pos[0]][self.pos[1]].type == 6:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==self.pos[0]+c and new_pos[1]==self.pos[1]+d:
                        if not  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                            return True
                        elif new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==self.pos[0]+c and new_pos[1]==self.pos[1]+d:
                        if not  new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                            return True
                        elif new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
                            return True
def lm_castle(self,new_pos,t,new_board):#*enroque
    if not new_board.position[self.pos[0]][self.pos[1]].type == 0 and new_board.position[self.pos[0]][self.pos[1]].type == 6 and not check[0]:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            if rc_Q:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]-2:
                    if move_posible (new_board.position[7][0],[7,3],turn,new_board):
                        return True
            if rc_K:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if move_posible (new_board.position[7][7],[7,5],turn,new_board):
                        return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if rc_q:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]-2:
                    if move_posible (new_board.position[0][0],[0,3],turn,new_board):
                        return True
            if rc_k:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if move_posible (new_board.position[0][7],[0,5],turn,new_board):
                        return True
def move_posible(self,new_pos,t,new_board):#*#verificar si el movimiento es de acuerdo con la pieza
    if new_board.position[new_pos[0]][new_pos[1]]==0:
        if self.type == 1:#*para el peon
            return lm_pawn(self,new_pos,t,new_board)
        elif self.type == 2:#*para el caballo
            return lmc_knight(self,new_pos,t,new_board)
        elif self.type == 3:#*para el alfil
            return lm_bishop(self,new_pos,t,new_board)
        elif self.type == 4:#*para la torre
                return lm_rook(self,new_pos,t,new_board)     
        elif self.type == 5:#*para la reina
            return lm_queen(self,new_pos,t,new_board)
        elif self.type == 6:#*para el rey
            return lm_king(self,new_pos,t,new_board)

#*# capturas legales

def lc_pawn(self,new_pos,t,new_board):
    if new_board.position[self.pos[0]][self.pos[1]].type == 1:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            if new_pos[0] == self.pos[0]-1:
                if new_pos[1] == self.pos[1]-1 or new_pos[1] == self.pos[1]+1:
                    if new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 or new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
                        return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if new_pos[0] == self.pos[0]+1:
                if new_pos[1] == self.pos[1]-1 or new_pos[1] == self.pos[1]+1:
                    if new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0 or new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == WHITE:
                        return True
def en_passant(self,new_pos,t,new_board):
    if lc_pawn(self,new_pos,t,new_board):
        if new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
            if en_pssnt[0] and new_pos == en_pssnt[1]:
                return True
def capture_posible(self,new_pos,t,new_board):#*#verificar si la captura es de acuerdo con la pieza
    if self.type == 1:#*para el peon
        return lc_pawn(self,new_pos,t,new_board)
    elif self.type == 2:#*para el caballo
        return lmc_knight(self,new_pos,t,new_board)
    elif self.type == 3:#*para el alfil
        return lm_bishop(self,new_pos,t,new_board)
    elif self.type == 4:#*para la torre
        return lm_rook(self,new_pos,t,new_board)     
    elif self.type == 5:#*para la reina
        return lm_queen(self,new_pos,t,new_board)
    elif self.type == 6:#*para el rey
        return lm_king(self,new_pos,t,new_board)

#*#*codigo de piezas e imagenes

P_img = pygame.image.load("imgs/Pawn0.png").convert_alpha()
p_img = pygame.image.load("imgs/Pawn1.png").convert_alpha()
N_img = pygame.image.load("imgs/Knight0.png").convert_alpha()
n_img = pygame.image.load("imgs/Knight1.png").convert_alpha()
B_img = pygame.image.load("imgs/Bishop0.png").convert_alpha()
b_img = pygame.image.load("imgs/Bishop1.png").convert_alpha()
R_img = pygame.image.load("imgs/Rook0.png").convert_alpha()
r_img = pygame.image.load("imgs/Rook1.png").convert_alpha()
Q_img = pygame.image.load("imgs/Queen0.png").convert_alpha()
q_img = pygame.image.load("imgs/Queen1.png").convert_alpha()
K_img = pygame.image.load("imgs/King0.png").convert_alpha()
k_img = pygame.image.load("imgs/King1.png").convert_alpha()
images = [P_img,p_img,N_img,n_img,B_img,b_img,R_img,r_img,Q_img,q_img,K_img,k_img]

brd = [[ 8, 4, 6,10,12, 6, 4, 8],
       [ 2, 2, 2, 2, 2, 2, 2, 2],
       [ 0, 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0, 0],
       [ 0, 0, 0, 0, 0, 0, 0, 0],
       [ 1, 1, 1, 1, 1, 1, 1, 1],
       [ 7, 3, 5, 9,11, 5, 3, 7]]

Wpieces = []
Bpieces = []
K = 0
k = 0
for l in range (8):
    for s in range(8):
        ps = brd[l][s]
        if not ps==0:
            if ps % 2 == 1:
                pc = Piece(images[ps-1],WHITE,int((ps+1)/2),[l,s])
                Wpieces.append(pc)
            else:
                pc = Piece(images[ps-1],BLACK,int(ps/2),[l,s])
                Bpieces.append(pc)
            if pc.type == 6: 
                if pc.color == WHITE:
                    K = pc
                else:
                    k = pc
            brd[l][s] = pc

board = Board(brd)
lines = ['8','7','6','5','4','3','2','1']
columnes = ['a','b','c','d','e','f','g','h']

#*#*variables en posicion inicial e inicio grafico

rc_Q=True
rc_K=True
rc_q=True
rc_k=True
turn = 0
noturn = 1
check=[False,None,False]
running = True 
board.reset()
pygame.display.update()
fps = 30
delay = 0.2
frames = int(fps*delay)
df = 1/fps

#*#*#codigo y funcionamiento del juego

piece_raised = 0
pcd = None
promoting = [False,None,None,None]
en_pssnt = [False,None]
board.reset_lm()
while running:#*#*bucle
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:#*#correcto apagado
            running = False
        if event.type == MOUSEBUTTONDOWN:#*#click
            Pos = event.pos
            if piece_raised == 0 and not promoting[0]:#*levantar pieza (1° click)
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                piece_raised = board.get_piece(columnes[i],lines[j])#saber cual pieza y su posicion
                                if not board.position[j][i]==0:
                                    if board.get_piece(columnes[i],lines[j]).color == color_turn[turn]:#saber cuando la pieza este en el aire
                                        screen.blit(r_sq,(i*80,j*80))
                                        screen.blit(board.get_piece(columnes[i],lines[j]).image,(i*80,j*80))
                                        piece_raised.rsrch_lm(board)
                                        board.show_lm(piece_raised)
                        pygame.display.update()
            elif not piece_raised == 0 and not promoting[0]:#*colocar pieza(2° click)
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                old_pos = piece_raised.pos
                                if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                                    piece_raised.move([j,i],board)
                                    if not promoting[0]:
                                        board.reset()
                                        board.reset_lm()
                                elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                                    pcd = board.get_piece(columnes[i],lines[j])
                                    piece_raised.capture([j,i],board)
                                    if not promoting[0]:
                                        board.reset()
                                        board.reset_lm()
                                if not old_pos == piece_raised.pos:
                                    if piece_raised.type == 1:
                                        if piece_raised.pos[0] == 0:
                                            board.promote(piece_raised.pos,BLACK)
                                            promoting = [True,piece_raised,pcd,old_pos]
                                        elif piece_raised.pos[0] == 7:
                                            board.promote(piece_raised.pos,WHITE)
                                            promoting = [True,piece_raised,pcd,old_pos]
                                    check = board.check(noturn)
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
                                piece_raised = 0
            elif promoting[0]:#*solo si esta coronando un peon(3°click)
                (r,c) = promoting[1].pos
                (y,x) = promoting[3]
                for i in range (8):
                    for j in range (8):
                        if Pos[0]>i*80 and Pos[0]<80+i*80:
                            if Pos[1]>j*80 and Pos[1]<80+j*80:
                                pawn = promoting[1]
                                if pawn.color == WHITE:
                                    if [j,i] == [r,c]:
                                        pawn.type = 5
                                        pawn.image = Q_img
                                    elif [j,i] == [r+1,c]:
                                        pawn.type = 2
                                        pawn.image = N_img
                                    elif [j,i] == [r+2,c]:
                                        pawn.type = 4
                                        pawn.image = R_img
                                    elif [j,i] == [r+3,c]:
                                        pawn.type = 3
                                        pawn.image = B_img
                                    else:
                                        if not promoting[2] == None:
                                            Bpieces.append(promoting[2])
                                            board.position[r][c] = promoting[2]
                                            pcd = None
                                        else:
                                            board.position[r][c] = 0
                                        board.set_piece(columnes[x],lines[y],pawn)
                                        (turn,noturn)=(0,1)
                                    if turn == 1:
                                        pawn.rsrch_lm(board)
                                elif pawn.color == BLACK:
                                    if [j,i] == [r,c]:
                                        pawn.type = 5
                                        pawn.image = q_img
                                    elif [j,i] == [r-1,c]:
                                        pawn.type = 2
                                        pawn.image = n_img
                                    elif [j,i] == [r-2,c]:
                                        pawn.type = 4
                                        pawn.image = r_img
                                    elif [j,i] == [r-3,c]:
                                        pawn.type = 3
                                        pawn.image = b_img
                                    else:
                                        if not promoting[2] == None:
                                            Wpieces.append(promoting[2])
                                            board.position[r][c] = promoting[2]
                                            pcd = None
                                        else:
                                            board.position[r][c] = 0
                                        board.set_piece(columnes[x],lines[y],pawn)
                                        (turn,noturn)=(1,0)
                                    if turn == 0:
                                        pawn.rsrch_lm(board)
                promoting = [False,None,None,None]
                board.reset()