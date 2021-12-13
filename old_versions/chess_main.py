#|-   -   -   -   -   -   -Codigo de Santiago Castro Muñoz (2021)-   -   -   -   -   -   -|#


#|      ~~~~~      Inicio codigo (constantes)      ~~~~~      |#

#|   ++++   Importaciones e inicio de pygame y su pantalla   ++++   |#

import pygame, sys, time
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")
icon = pygame.image.load("chess_pepega/imgs/icon.png")
pygame.display.set_icon(icon)

#|   ++++   Fuentes   ++++   |#

font = pygame.font.SysFont('arial black', 16)
font2 = pygame.font.SysFont('arial black', 32)
font3 = pygame.font.SysFont('arial black', 20)

#|   ++++   Colores en RGB   ++++   |#

BROWN = (139,69,19)
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (105,105,105)
LGREY = (169,169,169)
BEIGE = (255,206,158,255)
GREEN = (107,142,35)
LGREEN = (163,217,54)

#|   ++++   Imagenes de diseño   ++++   |#

r_sq = pygame.image.load("chess_pepega/imgs/raised_square.png").convert_alpha()
mp = pygame.image.load("chess_pepega/imgs/mp.png").convert_alpha()
cp = pygame.image.load("chess_pepega/imgs/cp.png").convert_alpha()
ms_mp = pygame.image.load("chess_pepega/imgs/ms_mp.png").convert_alpha()

#|   ++++   Sonidos   ++++   |#

move_sound = pygame.mixer.Sound("chess_pepega/sounds/piece_dropped.mp3")
capture_sound = pygame.mixer.Sound("chess_pepega/sounds/piece_capturing.mp3")

#|   ++++   Variables principales   ++++   |#

rc_Q=True
rc_K=True
rc_q=True
rc_k=True
turn = 0
noturn = 0
color_turn = [WHITE,BLACK]

#|      ~~~~~      Funciones      ~~~~~      |#

#|   ++++   De diseño   ++++   |#

def rect_circle(color,x,y,lo,la):#*#dibujar un rectangulo con esquinas onduladas
    m = max(lo,la)
    pygame.draw.rect(screen,color,(x+m/10, y, lo-m/5, la))
    pygame.draw.rect(screen,color,(x, y+m/10, lo, la-m/5))
    pygame.draw.ellipse(screen,color,(x, y, m/5, m/5))
    pygame.draw.ellipse(screen,color,(x+(lo-m/5), y+(la-m/5), m/5, m/5))
    pygame.draw.ellipse(screen,color,(x+(lo-m/5), y, m/5, m/5))
    pygame.draw.ellipse(screen,color,(x, y+(la-m/5), m/5, m/5))

#|   ++++   Principales   ++++   |#

def game_over():#*#saber si se acabo el juego (solo en jaquemate o ahogo)
    k=0
    if color_turn[turn] == WHITE:
        for ps in Wpieces:
            if len(ps.lm) == 0:
                k=k+1
        if k == len(Wpieces):
            return True
    elif color_turn[turn] == BLACK:
        for ps in Bpieces:
            if len(ps.lm) == 0:
                k=k+1
        if k == len(Bpieces):
            return True

def fen(position):#*#transformar codigo FEN en matriz, saber si se puede enrocar y de quien es el turno
    global K, k, turn, noturn, rc_Q, rc_K, rc_q, rc_k
    brd = [[0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0]]
    position = position.replace('/',' ')
    position = position.split()
    ktr = 0
    for i in position:
        s = 0
        for j in i:
            if ktr<8:
                if j.isalpha():
                    if j.isupper():
                        clr = WHITE
                        img = types.index(j.lower())*2
                    else:
                        clr = BLACK
                        img = types.index(j.lower())*2+1
                    p = Piece(images[img],clr,types.index(j.lower())+1,[ktr,s])
                    brd[ktr][s] = p
                    if p.color == WHITE:
                        Wpieces.append(p)
                    if p.color == BLACK:
                        Bpieces.append(p)
                    Pieces.append(p)
                    if j == 'K':
                        K = p
                    elif j == 'k':
                        k = p
                elif j.isalnum():
                    s = s + (int(j)-1)
                s = s + 1
            elif ktr == 8:
                if i == 'w':
                    turn = 0
                    noturn = 1
                elif i == 'b':
                    turn = 1
                    noturn = 0
            elif ktr == 9:
                if i.isalpha():
                    if 'Q' not in i:
                        rc_Q = False
                    if 'K' not in i:
                        rc_K = False
                    if 'q' not in i:
                        rc_q = False
                    if 'k' not in i:
                        rc_k = False
                else:
                    rc_Q=False
                    rc_K=False
                    rc_q=False
                    rc_k=False
        ktr = ktr + 1
    return brd


#|      ~~~~~      Clases      ~~~~~      |#

#|   ++++   Clase tablero   ++++   |#

class Board:
    def __init__(self,brd):#matriz de la posicion inicial
        self.position = brd

    def get_piece(self,i,j):#obtener objeto pieza en posicion (i,j)
        (x,y) = (lines.index(j),columnes.index(i))
        return self.position[x][y]
        
    def set_piece(self,i,j,piece):#colocar pieza en posicion (i,j)
        (x,y) = (lines.index(j),columnes.index(i))
        piece.pos = [x,y]
        self.position[x][y] = piece

    def reset(self):#reiniciar el tablero según el turno y la orientación indicada
        for j in range (8):
            for i in range (8):
                self.reset_sq((j,i),GREY,LGREY)
                (i1,j1) = (i,j)
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (i1,j1) = (7-i,7-j)
                if promoting[0] and rotate:
                    (i1,j1) = (7-i1,7-j1)
                if not self.position[j1][i1] == 0:
                    screen.blit (self.position[j1][i1].image,(i*80,j*80))
        if game_over() and not promoting[0]:
            self.finish_game()
        pygame.display.update()

    def show_lm(self,piece):#mostrar jugadas posibles de la pieza seleccionada
       for m in piece.lm:
            (i,j) = m
            (i1,j1) = (i,j)
            if (rotate and fo == noturn) or (not rotate and fo == 1):
                (i1,j1) = (7-i, 7-j)
            if move_posible(piece,[i,j],turn,self) or lm_castle(piece,[i,j],turn,self):
                self.reset_sq([i1,j1],GREY,LGREY)
                screen.blit(mp,(j1*80+30,i1*80+30))
            elif capture_posible(piece,[i,j],turn,self):
                if not self.position[i][j] == 0:
                    if check[0]:
                        if piece.type == 6 or [i,j] == check[1].pos:
                            self.reset_sq([i1,j1],GREY,LGREY)
                            screen.blit (self.position[i][j].image,(j1*80,i1*80))
                            screen.blit(cp,(j1*80,i1*80))
                    elif not check[0]:
                        self.reset_sq([i1,j1],GREY,LGREY)
                        screen.blit (self.position[i][j].image,(j1*80,i1*80))
                        screen.blit(cp,(j1*80,i1*80))
            if en_passant(piece,[i,j],turn,self):
                if check[0]:
                    if [i,j] == check[1].pos:
                        self.reset_sq([i1,j1],GREY,LGREY)
                        screen.blit (self.position[i][j].image,(j1*80,i1*80))
                        screen.blit(mp,(j1*80+30,i1*80+30))
                elif not check[0]:
                    self.reset_sq([i1,j1],GREY,LGREY)
                    screen.blit(mp,(j1*80+30,i1*80+30))
    
    def reset_lm(self):#resetear las jugadas posibles de todas la piezas presentes en el tablero
        for wp in Wpieces:
            wp.rsrch_lm(self)
        for bp in Bpieces:
            bp.rsrch_lm(self)
    
    def reset_sq(self,pos,c1,c2):#repinta una sola casilla del tablero
        xp = pos [0]
        yp = pos [1]
        if xp % 2 and yp % 2 or (xp-1) % 2 and (yp-1) % 2:
            pygame.draw.rect(screen, c2, (yp*80, xp*80, 80, 80))
            if xp == 7:
                ltr=font.render(columnes[yp],0,c1)
                screen.blit(ltr,(68+yp*80, 60+xp*80))
            elif yp == 0:
                nbr=font.render(lines[xp],0,c1)
                screen.blit(nbr,(2+yp*80, xp*80-3))
        else:
            pygame.draw.rect(screen, c1, (yp*80, xp*80, 80, 80))
            if xp == 7:
                ltr=font.render(columnes[yp],0,c2)
                screen.blit(ltr,(68+yp*80, 60+xp*80))
            if yp == 0:
                nbr=font.render(lines[xp],0,c2)
                screen.blit(nbr,(2+yp*80, xp*80-3))
    
    def reset_zone(self,pos):#repintar una zona del tablero de 9x9 para el movimiento correcto de las piezas
        (i,j) = pos
        if i-int(i)>=0.5:
            i = int(i+1)
        elif i-int(i)<-0.5:
            i = int(i-1)
        else:
            i = int(i)
        if j-int(j)>=0.5:
            j = int(j+1)
        elif j-int(j)<-0.5:
            j = int(j-1)
        else:
            j = int(j)
        (i1,j1) = (i,j)
        nxt = 1
        if (rotate and fo == noturn) or (not rotate and fo == 1):
            (i1,j1) = (7-i, 7-j)
            nxt = -1
        board.reset_sq((j,i),GREY,LGREY)
        if not self.position[j1][i1] == 0:
            screen.blit (self.position[j1][i1].image,(i*80,j*80))
        if not i == 7:
            board.reset_sq((j,i+1),GREY,LGREY)
            if not self.position[j1][i1+nxt] == 0:
                screen.blit (self.position[j1][i1+nxt].image,((i+1)*80,j*80))
        if not j == 7:
            board.reset_sq((j+1,i),GREY,LGREY)
            if not self.position[j1+nxt][i1] == 0:
                screen.blit (self.position[j1+nxt][i1].image,(i*80,(j+1)*80))
        if not i == 0:
            board.reset_sq((j,i-1),GREY,LGREY)
            if not self.position[j1][i1-nxt] == 0:
                screen.blit (self.position[j1][i1-nxt].image,((i-1)*80,j*80))
        if not j == 0:
            board.reset_sq((j-1,i),GREY,LGREY)
            if not self.position[j1-nxt][i1] == 0:
                screen.blit (self.position[j1-nxt][i1].image,(i*80,(j-1)*80))
        if not i == 7 and not j == 7:
            board.reset_sq((j+1,i+1),GREY,LGREY)
            if not self.position[j1+nxt][i1+nxt] == 0:
                screen.blit (self.position[j1+nxt][i1+nxt].image,((i+1)*80,(j+1)*80))
        if not i == 0 and not j == 0:
            board.reset_sq((j-1,i-1),GREY,LGREY)
            if not self.position[j1-nxt][i1-nxt] == 0:
                screen.blit (self.position[j1-nxt][i1-nxt].image,((i-1)*80,(j-1)*80))
        if not i == 0 and not j == 7:
            board.reset_sq((j+1,i-1),GREY,LGREY)
            if not self.position[j1+nxt][i1-nxt] == 0:
                screen.blit (self.position[j1+nxt][i1-nxt].image,((i-1)*80,(j+1)*80))
        if not i == 7 and not j == 0:
            board.reset_sq((j-1,i+1),GREY,LGREY)
            if not self.position[j1-nxt][i1+nxt] == 0:
                screen.blit (self.position[j1-nxt][i1+nxt].image,((i+1)*80,(j-1)*80))     

    def check(self,t):#detenerminar si hay Jaque en la posicion
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

    def next_pos_check(self,new_pos,piece):#calcular si en la jugada designada el rey es capturable
        (x,y) = new_pos
        new_b = Board(self.position,self.wp,self.bp)
        new_b.position[piece.pos[0]][piece.pos[1]] = 0
        new_b.set_piece(columnes[y],lines[x],piece)
        next_check = new_b.check(turn)
        if next_check[0]:
            return True
    
    def promote(self,new_pos,color):#mostrar recuadro de pizas para elegir que pieza coronar
        (c,r) = new_pos
        s = 1
        z = 0
        if (rotate and fo == turn) or (not rotate and fo == 1):
            (c,r) = (7-c,7-r)
            z = 240
            s = -1
        if color == WHITE:
            pygame.draw.rect(screen, WHITE, (r*80, c*80-z, 80, 320))
            screen.blit (Q_img,(r*80,c*80))
            screen.blit (N_img,(r*80,c*80+80*s))
            screen.blit (R_img,(r*80,c*80+160*s))
            screen.blit (B_img,(r*80,c*80+240*s))
        else:
            pygame.draw.rect(screen, WHITE, (r*80, c*80-240+z, 80, 320))
            screen.blit (q_img,(r*80,c*80))
            screen.blit (n_img,(r*80,c*80-80*s))
            screen.blit (r_img,(r*80,c*80-160*s))
            screen.blit (b_img,(r*80,c*80-240*s))
        pygame.display.update()
    
    def finish_game(self):#mostrar un mensaje de fin de juego
        global check
        check = board.check(noturn)
        rect_circle(WHITE, 140, 165, 360, 310)
        rect_circle(GREEN, 140, 165, 360, 100)
        pygame.draw.rect(screen, GREEN, (140, 215, 360, 50))
        pygame.draw.rect(screen,GREY, (190, 390, 120, 42))
        pygame.draw.rect(screen,GREY, (330, 390, 120, 42))
        pygame.draw.rect(screen,LGREY, (190, 390, 120, 40))
        pygame.draw.rect(screen,LGREY, (330, 390, 120, 40))
        b1 = font3.render("Rematch", 0, GREY)
        b2 = font3.render("Quit", 0, GREY)
        screen.blit(b1,(200,395))
        screen.blit(b2,(365,395))
        if check[0]:
            if color_turn[noturn] == WHITE:
                won = font2.render("White won!", 0, WHITE)
                rect_circle(LGREY, 350, 290, 80, 80)
                rect_circle(GREEN, 210, 290, 80, 80)
            elif color_turn[noturn] == BLACK:
                won = font2.render("Black won!", 0, WHITE)
                rect_circle(LGREY, 210, 290, 80, 80)
                rect_circle(GREEN, 350, 290, 80, 80)
            screen.blit(won,(225,180))
            mate = font.render("By Checkmate", 0, LGREEN)
            sc = font3.render(str(score[0])+'-'+str(score[1]), 0, GREY)
            screen.blit(sc,(305,315))
        else:
            draw=font2.render("Draw",0,WHITE)
            screen.blit(draw,(265,180))
            rect_circle(LGREY, 350, 290, 80, 80)
            rect_circle(LGREY, 210, 290, 80, 80)
            mate = font.render("By Stalemate", 0, LGREEN)
            sc = font3.render(str(score[0])+'-'+str(score[1]), 0, GREY)
            screen.blit(sc,(300,315))
        screen.blit(P_img,(210,290))
        screen.blit(p_img,(350,290))
        screen.blit(mate,(250,230))
    
    def restart(self):#resetear el tablero a la posición inicial designada
        self.position = [[ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0],
                          [ 0, 0, 0, 0, 0, 0, 0, 0]]
        for p in Pieces:
            (y,x) = p.start_pos
            self.set_piece(columnes[x],lines[y],p)
            if p.color == WHITE:
                if not p in Wpieces:
                    Wpieces.append(p)
            elif p.color == BLACK:
                if not p in Bpieces:
                    Bpieces.append(p)

#|   ++++   Clase piezas   ++++   |#

class Piece:
    def __init__(self,img,color,piece,pos):#*#info general de pieza,
    #*# Tipo de pieza: 0 <=> nada, 1 <=> peon, 2 <=> caballo, 3 <=> alfil, 4 <=> torre, 5 <=> reina, 6 <=> rey
        self.image = img
        self.pos = pos
        self.start_pos = pos
        if color == WHITE or color == BLACK:
            self.color = color
        if piece>0 and piece<7:
            self.type = piece
        self.lm = []
            
    def move(self,new_pos,new_board,anim):#*#funcion mover pieza
    #*#(verifica si el movimiento es posible y si es asi, lo efectua, si es necesario hace la animación del movimiento)
    #*#(reproduce un sonido de colocar pieza)
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
            if new_pos in self.lm:
                if self.type == 1 and self.pos[0]-new_pos[0] == ep*2:
                    en_pssnt = [True,[new_pos[0]+ep,new_pos[1]]]
                else:
                    en_pssnt = [False,None]
                if cstl:
                    if new_pos[1] == 2:
                        if self.color == WHITE:
                            rm = [[7,3],[7,0]]
                        else:
                            rm = [[0,3],[0,0]]
                    elif new_pos[1] == 6:
                        if self.color == WHITE:
                            rm = [[7,5],[7,7]]
                        else:
                            rm = [[0,5],[0,7]]
                    ry = rm[1][0]
                    rx = rm[1][1]
                    dr_x = (rm[0][0]-ry)/frames
                    dr_y = (rm[0][1]-rx)/frames
                    rook = new_board.position[ry][rx]
                    new_board.position[ry][rx] = 0
                new_board.position[py][px] = 0
                if not anim:
                    move_sound.play()
                else:
                    (fpy,fpx) = self.pos
                    if cstl:
                        (fry,frx) = rm[1]
                    if (rotate and fo == noturn) or (not rotate and fo == 1):
                        (px,py) = (7-px,7-py)
                        (distance_x,distance_y) = (-distance_x,-distance_y)
                        (fpx,fpy) = (7-fpx,7-fpy)
                        if cstl:
                            (rx,ry) = (7-rx,7-ry)
                            (dr_x,dr_y) = (-dr_x,-dr_y)
                            (frx,fry) = (7-frx,7-fry)
                    for i in range (frames+1):
                        new_board.reset_zone((px,py))
                        if cstl:
                            new_board.reset_zone((rx,ry))
                            ry = fry + dr_x * i
                            rx = frx + dr_y * i
                            screen.blit(rook.image,(rx*80,ry*80))
                        py = fpy + distance_x * i
                        px = fpx + distance_y * i
                        screen.blit(self.image,(px*80,py*80))
                        pygame.display.update()
                        time.sleep(df)
                        if i == frames*2/3:
                            move_sound.play()
                new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                if cstl:
                    new_board.set_piece(columnes[rm[0][1]],lines[rm[0][0]],rook)
                    if not anim:
                        time.sleep(df*3)
                    move_sound.play()
                if self.color == WHITE:
                    (turn,noturn)=(1,0)
                elif self.color == BLACK:
                    (turn,noturn)=(0,1)
                    
    def capture(self,new_pos,new_board,anim):#*#funcion capturar pieza
    #*#(verifica si la captura es posible y si es asi, la efectua, si es necesario hace la animación del movimiento)
    #*#(Reproduce un sonido de colocar y capturar una pieza)
        global turn, noturn, check, en_pssnt
        if not new_pos == self.pos:
            distance_x = (new_pos[0] - self.pos[0])/frames
            distance_y = (new_pos[1] - self.pos[1])/frames
            py = self.pos[0]
            px = self.pos[1]
            if new_pos in self.lm:
                pd = new_board.position[new_pos[0]][new_pos[1]]
                if en_pssnt and en_passant(self,new_pos,turn,new_board):
                    pd = new_board.position[self.pos[0]][new_pos[1]]
                    new_board.position[self.pos[0]][new_pos[1]] = 0
                en_pssnt = [False,None]
                new_board.position[self.pos[0]][self.pos[1]] = 0
                if not anim:
                    move_sound.play()
                    capture_sound.play()
                else:
                    (fpy,fpx) = self.pos
                    if (rotate and fo == noturn) or (not rotate and fo == 1):
                        (px,py) = (7-px,7-py)
                        (distance_x,distance_y) = (-distance_x,-distance_y)
                        (fpx,fpy) = (7-fpx,7-fpy)
                    for i in range (frames+1):
                        new_board.reset_zone((px,py))
                        py = fpy + distance_x * i
                        px = fpx + distance_y * i
                        screen.blit (self.image,(px*80,py*80))
                        pygame.display.update()
                        time.sleep(df)
                        if i == frames/2:
                            move_sound.play()
                            capture_sound.play()
                new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                if self.color == WHITE:
                    (turn,noturn)=(1,0)
                    del Bpieces[Bpieces.index(pd)]
                elif self.color == BLACK:
                    (turn,noturn)=(0,1)
                    del Wpieces[Wpieces.index(pd)]
    
    def rsrch_lm(self,new_board):#*#calcular jugadas posibles de la pieza misma y guradarlas en una lista
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

#|***movimientos legales***|#

def lm_pawn(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada del peón dado
    if self.color == WHITE and t == 0:#blanco
        if new_pos[0] == self.pos[0]-1 and new_pos[1] == self.pos[1]:
            return True
        elif self.pos[0] == 6 and new_pos[0] == self.pos[0]-2 and new_pos[1] == self.pos[1] and new_board.position[self.pos[0]-1][self.pos[1]] == 0:
            return True
    elif self.color == BLACK and t == 1:#negro
        if new_pos[0] == self.pos[0]+1 and new_pos[1] == self.pos[1]:
            return True
        elif self.pos[0] == 1 and new_pos[0] == self.pos[0]+2 and new_pos[1] == self.pos[1] and new_board.position[self.pos[0]+1][self.pos[1]] == 0:
            return True
def lmc_knight(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura del caballo dado
    if self.color == color_turn[t]:#blanco y negro
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
                        if new_board.position[new_pos[0]][new_pos[1]] == 0 or new_board.position[new_pos[0]][new_pos[1]].color == color_turn[t-1]:
                            return True
def lmc_bishop(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura del alfil dado
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            for c in range (-1,2,2):
                for d in range (-1,2,2):
                    q=1
                    while self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0] == self.pos[0]+q*c and new_pos[1] == self.pos[1]+q*d:
                            return True
                        q=q+1
                    if self.pos[0]+q*c>-1 and self.pos[0]+q*c<8 and self.pos[1]+q*d>-1 and self.pos[1]+q*d<8 and not new_board.position[self.pos[0]+q*c][self.pos[1]+q*d] == 0:
                        if new_pos[0] == self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]).color == BLACK:
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
def lmc_rook(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura de la torre dada
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
def lmc_queen(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura de la reina dada
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
def lmc_king(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura del rey dado
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
def lm_castle(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada de enrroque
    if not new_board.position[self.pos[0]][self.pos[1]].type == 0 and new_board.position[self.pos[0]][self.pos[1]].type == 6 and not check[0]:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            if rc_Q:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]-2:
                    if move_posible (new_board.position[7][0],[7,3],turn,new_board):
                        if [7,3] in self.lm:
                            return True
            if rc_K:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if move_posible (new_board.position[7][7],[7,5],turn,new_board):
                        if [7,5] in self.lm:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if rc_q:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]-2:
                    if move_posible (new_board.position[0][0],[0,3],turn,new_board):
                        if [0,3] in self.lm:
                            return True
            if rc_k:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if move_posible (new_board.position[0][7],[0,5],turn,new_board):
                        if [0,5] in self.lm:
                            return True
def move_posible(self,new_pos,t,new_board):#verifica, para el tipo de pieza, si el movimiento es correcto
    if new_board.position[new_pos[0]][new_pos[1]]==0:
        if self.type == 1:#para el peon
            return lm_pawn(self,new_pos,t,new_board)
        elif self.type == 2:#para el caballo
            return lmc_knight(self,new_pos,t,new_board)
        elif self.type == 3:#para el alfil
            return lmc_bishop(self,new_pos,t,new_board)
        elif self.type == 4:#para la torre
                return lmc_rook(self,new_pos,t,new_board)     
        elif self.type == 5:#para la reina
            return lmc_queen(self,new_pos,t,new_board)
        elif self.type == 6:#para el rey
            return lmc_king(self,new_pos,t,new_board)

#|***capturas legales***|#

def lc_pawn(self,new_pos,t,new_board):#calcula si la posicion dada es una captura del peón dado
    if not new_board.position[self.pos[0]][self.pos[1]] == 0 and new_board.position[self.pos[0]][self.pos[1]].type == 1:
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
def en_passant(self,new_pos,t,new_board):#calcula si la posicion dada es una captura al paso del peón dado
    if lc_pawn(self,new_pos,t,new_board):
        if new_board.get_piece(columnes[new_pos[1]],lines[new_pos[0]]) == 0:
            if en_pssnt[0] and new_pos == en_pssnt[1]:
                return True
def capture_posible(self,new_pos,t,new_board):#verifica, para el tipo de pieza, si la captura es correcta
    if self.type == 1:#para el peon
        return lc_pawn(self,new_pos,t,new_board)
    elif self.type == 2:#para el caballo
        return lmc_knight(self,new_pos,t,new_board)
    elif self.type == 3:#para el alfil
        return lmc_bishop(self,new_pos,t,new_board)
    elif self.type == 4:#para la torre
        return lmc_rook(self,new_pos,t,new_board)     
    elif self.type == 5:#para la reina
        return lmc_queen(self,new_pos,t,new_board)
    elif self.type == 6:#para el rey
        return lmc_king(self,new_pos,t,new_board)

#|      ~~~~~      uso y creacion de tablero, piezas, imagenes de piezas, y variables      ~~~~~      |#

P_img = pygame.image.load("chess_pepega/imgs/Pawn0.png").convert_alpha()
p_img = pygame.image.load("chess_pepega/imgs/Pawn1.png").convert_alpha()
N_img = pygame.image.load("chess_pepega/imgs/Knight0.png").convert_alpha()
n_img = pygame.image.load("chess_pepega/imgs/Knight1.png").convert_alpha()
B_img = pygame.image.load("chess_pepega/imgs/Bishop0.png").convert_alpha()
b_img = pygame.image.load("chess_pepega/imgs/Bishop1.png").convert_alpha()
R_img = pygame.image.load("chess_pepega/imgs/Rook0.png").convert_alpha()
r_img = pygame.image.load("chess_pepega/imgs/Rook1.png").convert_alpha()
Q_img = pygame.image.load("chess_pepega/imgs/Queen0.png").convert_alpha()
q_img = pygame.image.load("chess_pepega/imgs/Queen1.png").convert_alpha()
K_img = pygame.image.load("chess_pepega/imgs/King0.png").convert_alpha()
k_img = pygame.image.load("chess_pepega/imgs/King1.png").convert_alpha()
images = [P_img,p_img,N_img,n_img,B_img,b_img,R_img,r_img,Q_img,q_img,K_img,k_img]

types = ['p','n','b','r','q','k']

brd = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'#Codigo FEN

Wpieces = []
Bpieces = []
Pieces = []
K = 0
k = 0

board = Board(fen(brd))
lines = ['8','7','6','5','4','3','2','1']
columnes = ['a','b','c','d','e','f','g','h']

#|   ++++   variables en posicion inicial  ++++   |#

move = False
check=[False,None,False]
running = True

fps = 60
delay = 0.2
frames = int(fps*delay)
df = 1/fps

score = [0,0]

orientation = 1
fo = orientation
rotate = False

piece_raised = 0
pcd = None

promoting = [False,None,None,None]
en_pssnt = [False,None] 
mouse_sq = []

psr = 0
cnt = 0

#|      ~~~~~      Interaccion grafica con el juego      ~~~~~      |#

#|   ++++   funciones al empezar el juego   ++++   |#

board.reset_lm()
board.reset()
pygame.display.update()

#|   ++++   bucle principal   ++++   |#

while running:
    pos = pygame.mouse.get_pos()
    (m,n) = pos
    cnt = cnt + 1
    if not piece_raised == 0 and not promoting[0] and not game_over():#diseño de cuando el mouse hace alguna accion
        m = int(m/80)
        n = int(n/80)
        (M,N) = (m,n)
        (I,J) = (i,j)
        if (rotate and fo == noturn) or (not rotate and fo == 1):
            (M,N) = (7-m,7-n)
            (I,J) = (7-i,7-j)
        if cnt % 6:
            if not move:
                (m1,m2) = pos
                M1 = int(m1/80)
                M2 = int(m2/80)
                board.reset_zone((M1,M2))
                board.show_lm(piece_raised)
                if M1 < I+2 and M1 > I-2 and M2 < J+2 and M2 > J-2:
                    screen.blit(r_sq,(I*80,J*80))
            if len(mouse_sq) == 2 and not mouse_sq == (N,M):
                (a,b) = mouse_sq
                (a1,b1) = mouse_sq
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (a1,b1) = (7-a1,7-b1)
                board.reset_sq((a1,b1),GREY,LGREY)
                if mselect == mp:
                    screen.blit(mp,(b1*80+30,a1*80+30))
                elif mselect == cp:
                    screen.blit(cp,(b1*80,a1*80))
                    if not board.position[a][b] == 0:
                        screen.blit(board.position[a][b].image,(b1*80,a1*80))
            if [N,M] in piece_raised.lm:
                board.reset_sq((n,m),GREY,LGREY)
                mselect = mp
                if not board.position[N][M] == 0:
                    screen.blit(board.position[N][M].image,(m*80,n*80))
                    mselect = cp
                screen.blit(ms_mp,(m*80,n*80))
                mouse_sq = [N,M]
            if not move:
                screen.blit(piece_raised.image,(m1-40,m2-40))
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#correcto apagado
            running = False
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:#click
            mouse_sq = []
            mselect = None
            Pos = event.pos
            (i,j) = Pos
            i = int(i/80)
            j = int(j/80)
            if piece_raised == 0 and not promoting[0] and not game_over():#levantar pieza (1° click)
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (i,j) = (7-i,7-j)
                if not board.position[j][i] == 0:
                    psr = piece_raised
                    piece_raised = board.position[j][i]#saber cual pieza y su posicion
                    if piece_raised.color == color_turn[noturn]:
                        piece_raised = 0
                    if board.position[j][i].color == color_turn[turn]:#saber cuando la pieza este en el aire
                        piece_raised.rsrch_lm(board)
            elif not piece_raised == 0 and not promoting[0] and not game_over() and move:#colocar pieza(2° click)
                (I,J) = (i,j)
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (i,j) = (7-i,7-j)
                old_pos = piece_raised.pos
                if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                    piece_raised.move([j,i],board,True)
                elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                    pcd = board.get_piece(columnes[i],lines[j])
                    piece_raised.capture([j,i],board,True)
                if not old_pos == piece_raised.pos:
                    nt = orientation
                    if rotate:
                        orientation = turn
                        nt = noturn
                    if piece_raised.type == 1:
                        if piece_raised.pos[0] == 0:
                            promoting = [True,piece_raised,pcd,old_pos]
                        elif piece_raised.pos[0] == 7:
                            promoting = [True,piece_raised,pcd,old_pos]
                        else:
                            board.reset_lm()
                    else: 
                        board.reset_lm()
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
                if game_over() and not promoting[0]:
                    if check[0]:
                        if color_turn[noturn] == WHITE:
                            score[0] = score[0] + 1
                        elif color_turn[noturn] == BLACK:
                            score[1] = score[1] + 1
                    else:
                        score[0] = score[0] + 0.5
                        score[1] = score[1] + 0.5
                if not board.position[j][i] == 0:
                    if board.get_piece(columnes[i],lines[j]).color == piece_raised.color:
                        if not board.get_piece(columnes[i],lines[j]) == piece_raised:
                            board.reset()
                            piece_raised = board.get_piece(columnes[i],lines[j])
                            screen.blit(r_sq,(I*80,J*80))
                            screen.blit(board.get_piece(columnes[i],lines[j]).image,(I*80,J*80))
                            piece_raised.rsrch_lm(board)
                            board.show_lm(piece_raised)
                            pygame.display.update()
                        else:
                            piece_raised = 0
                            board.reset()
                    else:
                        piece_raised = 0
                        board.reset()
                else:
                    piece_raised = 0
                    board.reset()
                if promoting[0]:
                    board.promote(promoting[1].pos,promoting[1].color)
                move = False
            elif promoting[0]:#solo si se esta coronando un peon(3°click)
                pawn = promoting[1]
                (r,c) = pawn.pos
                (y,x) = promoting[3]
                (n1,n2,n3) = (1,2,3)
                if (rotate and fo == turn) or (not rotate and fo == 1):
                    (n1,n2,n3) = (-n1,-n2,-n3)
                    (r,c) = (7-r,7-c)
                if pawn.color == WHITE:
                    if [j,i] == [r,c]:
                        pawn.type = 5
                        pawn.image = Q_img
                    elif [j,i] == [r+n1,c]:
                        pawn.type = 2
                        pawn.image = N_img
                    elif [j,i] == [r+n2,c]:
                        pawn.type = 4
                        pawn.image = R_img
                    elif [j,i] == [r+n3,c]:
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
                elif pawn.color == BLACK:
                    if [j,i] == [r,c]:
                        pawn.type = 5
                        pawn.image = q_img
                    elif [j,i] == [r-n1,c]:
                        pawn.type = 2
                        pawn.image = n_img
                    elif [j,i] == [r-n2,c]:
                        pawn.type = 4
                        pawn.image = r_img
                    elif [j,i] == [r-n3,c]:
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
                promoting = [False,None,None,None]
                board.reset_lm()
                board.reset()
            elif game_over() and not promoting[0]:#interfaz de fin de juego
                (i,j) = Pos
                if 190<i and i<310:
                    if 390<j and j<430:
                        board.restart()
                        turn = 0
                        noturn = 1
                        board.reset_lm()
                        board.reset()
                elif 330<i and i<450:
                    if 390<j and j<430:
                        pygame.quit()
                        running = False
                        sys.exit()
        if event.type == MOUSEBUTTONUP: 
            Pos = event.pos
            (i,j) = Pos
            i = int(i/80)
            j = int(j/80)
            if not piece_raised == 0:
                (I,J) = (i,j)
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (i,j) = (7-i,7-j)
                old_pos = piece_raised.pos
                if [j,i] == piece_raised.pos:
                    move = True
                    board.reset_zone((I,J))
                    screen.blit(r_sq,(I*80,J*80))
                    screen.blit(board.get_piece(columnes[i],lines[j]).image,(I*80,J*80))
                    board.show_lm(piece_raised)
                    break
                if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                    piece_raised.move([j,i],board,False)
                elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                    pcd = board.position[j][i]
                    piece_raised.capture([j,i],board,False)
                if not old_pos == piece_raised.pos:
                    nt = orientation
                    if rotate:
                        orientation = turn
                        nt = noturn
                    if piece_raised.type == 1:
                        if piece_raised.pos[0] == 0:
                            promoting = [True,piece_raised,pcd,old_pos]
                        elif piece_raised.pos[0] == 7:
                            promoting = [True,piece_raised,pcd,old_pos]
                        else:
                            board.reset_lm()
                    else:
                        board.reset_lm()
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
                if game_over() and not promoting[0]:
                    if check[0]:
                        if color_turn[noturn] == WHITE:
                            score[0] = score[0] + 1
                        elif color_turn[noturn] == BLACK:
                            score[1] = score[1] + 1
                    else:
                        score[0] = score[0] + 0.5
                        score[1] = score[1] + 0.5
                board.reset()
                if promoting[0]:
                    board.promote(promoting[1].pos,promoting[1].color)
                move = False