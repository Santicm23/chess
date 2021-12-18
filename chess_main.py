#|-   -   -   -   -   -   -Codigo de Santiago Castro Muñoz (2021)-   -   -   -   -   -   -|#


#|      ~~~~~      Inicio codigo (constantes)      ~~~~~      |#

#|   ++++   Importaciones e inicio de pygame y su pantalla   ++++   |#

import pygame, sys, time
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")
icon = pygame.image.load("imgs/icon.png")
pygame.display.set_icon(icon)

#|   ++++   Fuentes   ++++   |#

font = pygame.font.SysFont('Gerbera', 16)
font2 = pygame.font.SysFont('Gerbera', 40)
font3 = pygame.font.SysFont('Gerbera', 30)
chessfont = pygame.font.Font('fonts/CASEFONT.TTF', 80)

#|   ++++   Colores en RGB   ++++   |#

BROWN = (139,69,19)
BLACK = (0,0,0)
WHITE = (225,225,225)
GREY = (125,125,125)
LGREY = (155,155,155)
BEIGE = (255,206,158,255)
GREEN = (107,142,35)
LGREEN = (163,217,54)
RED = (205,92,92)
YELLOW = (255,179,25)

#|   ++++   Imagenes de diseño   ++++   |#

r_sq = pygame.image.load("imgs/raised_square.png").convert_alpha()
mp = pygame.image.load("imgs/mp.png").convert_alpha()
cp = pygame.image.load("imgs/cp.png").convert_alpha()
ms_mp = pygame.image.load("imgs/ms_mp.png").convert_alpha()

#|   ++++   Sonidos   ++++   |#

move_sound = pygame.mixer.Sound("sounds/piece_dropped.mp3")
capture_sound = pygame.mixer.Sound("sounds/piece_capturing.mp3")

#|   ++++   Variables principales   ++++   |#

rc_Q=True
rc_K=True
rc_q=True
rc_k=True
turn = 0
noturn = 0
color_turn = [WHITE,BLACK]
last_cpm = 0
flcpm = 0
Nmove = 1
fmove = 1
go_type = ''


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

def change_font():
    for ps in Bpieces:
        if ps.type == 1:
            ps.image2 = chessfont.render("p", 1, WHITE)
        elif ps.type == 2:
            ps.image2 = chessfont.render("n", 1, WHITE)
        elif ps.type == 3:
            ps.image2 = chessfont.render("b", 1, WHITE)
        elif ps.type == 4:
            ps.image2 = chessfont.render("r", 1, WHITE)
        elif ps.type == 5:
            ps.image2 = chessfont.render("q", 1, WHITE)
        elif ps.type == 6:
            ps.image2 = chessfont.render("k", 1, WHITE)

#|   ++++   Principales   ++++   |#

def game_over():#*#saber si se acabo el juego (solo en jaquemate, ahogo o regla de 50 movimientos)
    global go_type
    k=0
    if color_turn[turn] == WHITE:
        for ps in Wpieces:
            if len(ps.lm) == 0:
                k=k+1
        if k == len(Wpieces):
            go_type = 'm'
            return True
    elif color_turn[turn] == BLACK:
        for ps in Bpieces:
            if len(ps.lm) == 0:
                k=k+1
        if k == len(Bpieces):
            go_type = 'm'
            return True
    if last_cpm == 50:
        go_type = 'f'
        return True

def fen(position):#*#transformar codigo FEN en matriz, saber si se puede enrocar y de quien es el turno
    global K, k, turn, noturn, rc_Q, rc_K, rc_q, rc_k, last_cpm, flcpm, Nmove, fmove
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
            elif ktr == 11:
                last_cpm = int(i)
                flcpm = last_cpm
            elif ktr == 12:
                Nmove = int(i)
                fmove = Nmove
        ktr = ktr + 1
    return brd

def get_sqr(pos):
    for i in sqrs:
        if i.pos == pos:
            return i

def get_arw(p1,p2):
    for i in arws:
        if i.bottom == p1 and i.top == p2:
            return i

def reset_draws():
    if not m_arw == 0:
        m_arw.draw()
    if check[0]:
        if turn == 0:
            c_sqr = Squares(RED,K.pos)
        else:
            c_sqr = Squares(RED,k.pos)
        c_sqr.draw()
    for i in sqrs:
        i.draw()
    for j in arws:
        j.draw()

def display_menu():
    rect_circle(WHITE, 140, 165, 360, 310)
    rect_circle(GREEN, 140, 165, 360, 100)
    pygame.draw.rect(screen, GREEN, (140, 215, 360, 50))
    pygame.draw.rect(screen,GREY, (190, 390, 120, 42))
    pygame.draw.rect(screen,GREY, (330, 390, 120, 42))
    pygame.draw.rect(screen,LGREY, (190, 390, 120, 40))
    pygame.draw.rect(screen,LGREY, (330, 390, 120, 40))
    b1 = font3.render("Play", 1, GREY)
    b2 = font3.render("Analize", 1, GREY)
    screen.blit(b1,(230,400))
    screen.blit(b2,(352,400))
    title = font2.render("Menu", 1, WHITE)
    screen.blit(title,(275,200))

#|      ~~~~~      Clases      ~~~~~      |#

#|   ++++   Clase tablero   ++++   |#

class Board:
    def __init__(self,brd:str):#creacion de la posicion inicial
        self.position = fen(brd)

    def __str__(self) -> str:

        """+---+---+---+---+---+---+---+---+
         8 | r | n | b | q | k | b | n | r |
           +---+---+---+---+---+---+---+---+
         7 | p | p | p | p | p | p | p | p |
           +---+---+---+---+---+---+---+---+
         6 |   |   |   |   |   |   |   |   |
           +---+---+---+---+---+---+---+---+
         5 |   |   |   |   |   |   |   |   |
           +---+---+---+---+---+---+---+---+
         4 |   |   |   |   |   |   |   |   |
           +---+---+---+---+---+---+---+---+
         3 |   |   |   |   |   |   |   |   |
           +---+---+---+---+---+---+---+---+
         2 | P | P | P | P | P | P | P | P |
           +---+---+---+---+---+---+---+---+
         1 | R | N | B | Q | K | B | N | R |
           +---+---+---+---+---+---+---+---+
             a   b   c   d   e   f   g   h  """

        ln = "  +---+---+---+---+---+---+---+---+\n"
        rt = '\n' + ln
        cols = "    a   b   c   d   e   f   g   h"
        for i in range (8):
            rt += str(7-i+1) + ' |'
            for j in range (8):
                if self.position[i][j] == 0:
                    rt += '  ' + ' |'
                elif self.position[i][j].color == WHITE:
                    rt += ' ' + types[self.position[i][j].type-1].capitalize() + ' |'
                elif self.position[i][j].color == BLACK:
                    rt += ' ' + types[self.position[i][j].type-1] + ' |'
            rt += '\n'
            rt += ln
        rt += cols
        return rt + '\n'

    def __repr__(self) -> str:
        """rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"""
        fencode = ''
        rc = False
        for i in range (8):
            ctr = 0
            for j in range (8):
                ps = self.position[i][j]
                if ps == 0:
                    ctr += 1
                else:
                    if ctr > 0:
                        fencode += str(ctr)
                        ctr = 0
                    if ps.color == WHITE:
                        fencode += types[self.position[i][j].type-1].capitalize()
                    elif ps.color == BLACK:
                        fencode += types[self.position[i][j].type-1]
            if ctr > 0:
                fencode += str(ctr)
            if i<7:
                fencode += '/'
        if turn == 0:
            fencode += ' w '
        else:
            fencode += ' b '
        if rc_K:
            fencode += 'K'
            rc = True
        if rc_Q:
            fencode += 'Q'
            rc = True
        if rc_k:
            fencode += 'k'
            rc = True
        if rc_q:
            fencode += 'q'
            rc = True
        if not rc:
            fencode += '-'
        fencode += ' - ' + str(last_cpm) + ' ' + str(Nmove)
        return fencode + '\n'

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
                    self.position[j1][i1].draw(i*80,j*80)
        reset_draws()
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
                            self.position[i][j].draw(j1*80,i1*80)
                            screen.blit(cp,(j1*80,i1*80))
                    elif not check[0]:
                        self.reset_sq([i1,j1],GREY,LGREY)
                        self.position[i][j].draw(j1*80,i1*80)
                        screen.blit(cp,(j1*80,i1*80))
            if en_passant(piece,[i,j],turn,self):
                if check[0]:
                    if [i,j] == check[1].pos:
                        self.reset_sq([i1,j1],GREY,LGREY)
                        self.position[i][j].draw(j1*80,i1*80)
                        screen.blit(mp,(j1*80+30,i1*60+30))
                elif not check[0]:
                    self.reset_sq([i1,j1],GREY,LGREY)
                    screen.blit(mp,(j1*80+30,i1*80+30))

    def reset_lm(self):#resetear las jugadas posibles de todas la piezas presentes en el tablero
        for wp in Wpieces:
            wp.rsrch_lm(self)
        for bp in Bpieces:
            bp.rsrch_lm(self)

    def reset_sq(self,pos,c1,c2):#repinta una sola casilla del tablero
        (xp, yp) = pos
        (x,y) = pos
        bsq = chessfont.render("+",1,GREY)
        if (rotate and fo == noturn) or (not rotate and fo == 1):
            (x,y) = (7-xp,7-yp)
        if xp % 2 and yp % 2 or (xp-1) % 2 and (yp-1) % 2:
            if mode == 0:
                pygame.draw.rect(screen, c2, (yp*80, xp*80, 80, 80))
            elif mode == 1:
                pygame.draw.rect(screen, BLACK, (yp*80, xp*80, 80, 80))
            if xp == 7:
                ltr=font.render(columnes[y],1,WHITE)
                screen.blit(ltr,(71+yp*80, 67+xp*80))
            elif yp == 0:
                nbr=font.render(lines[x],1,WHITE)
                screen.blit(nbr,(2+yp*80, xp*80+2))
        else:
            if mode == 0:
                pygame.draw.rect(screen, c1, (yp*80, xp*80, 80, 80))
            elif mode == 1:
                pygame.draw.rect(screen, BLACK, (yp*80, xp*80, 80, 80))
                screen.blit(bsq,(yp*80,xp*80))
            if xp == 7:
                ltr=font.render(columnes[y],1,WHITE)
                screen.blit(ltr,(71+yp*80, 67+xp*80))
            if yp == 0:
                nbr=font.render(lines[x],1,WHITE)
                screen.blit(nbr,(2+yp*80, xp*80+2))

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
            self.position[j1][i1].draw(i*80,j*80)
        if not i == 7:
            board.reset_sq((j,i+1),GREY,LGREY)
            if not self.position[j1][i1+nxt] == 0:
                self.position[j1][i1+nxt].draw((i+1)*80,j*80)
        if not j == 7:
            board.reset_sq((j+1,i),GREY,LGREY)
            if not self.position[j1+nxt][i1] == 0:
                self.position[j1+nxt][i1].draw(i*80,(j+1)*80)
        if not i == 0:
            board.reset_sq((j,i-1),GREY,LGREY)
            if not self.position[j1][i1-nxt] == 0:
                self.position[j1][i1-nxt].draw((i-1)*80,j*80)
        if not j == 0:
            board.reset_sq((j-1,i),GREY,LGREY)
            if not self.position[j1-nxt][i1] == 0:
                self.position[j1-nxt][i1].draw(i*80,(j-1)*80)
        if not i == 7 and not j == 7:
            board.reset_sq((j+1,i+1),GREY,LGREY)
            if not self.position[j1+nxt][i1+nxt] == 0:
                self.position[j1+nxt][i1+nxt].draw((i+1)*80,(j+1)*80)
        if not i == 0 and not j == 0:
            board.reset_sq((j-1,i-1),GREY,LGREY)
            if not self.position[j1-nxt][i1-nxt] == 0:
                self.position[j1-nxt][i1-nxt].draw((i-1)*80,(j-1)*80)
        if not i == 0 and not j == 7:
            board.reset_sq((j+1,i-1),GREY,LGREY)
            if not self.position[j1+nxt][i1-nxt] == 0:
                self.position[j1+nxt][i1-nxt].draw((i-1)*80,(j+1)*80)
        if not i == 7 and not j == 0:
            board.reset_sq((j-1,i+1),GREY,LGREY)
            if not self.position[j1-nxt][i1+nxt] == 0:
                self.position[j1-nxt][i1+nxt].draw((i+1)*80,(j-1)*80)

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
            pygame.draw.rect(screen, BLACK, (r*80, c*80-z, 80, 320))
            screen.blit (Q_img,(r*80,c*80))
            screen.blit (N_img,(r*80,c*80+80*s))
            screen.blit (R_img,(r*80,c*80+160*s))
            screen.blit (B_img,(r*80,c*80+240*s))
        else:
            if mode == 0:
                pygame.draw.rect(screen, WHITE, (r*80, c*80-240+z, 80, 320))
                screen.blit (q_img,(r*80,c*80))
                screen.blit (n_img,(r*80,c*80-80*s))
                screen.blit (r_img,(r*80,c*80-160*s))
                screen.blit (b_img,(r*80,c*80-240*s))
            elif mode == 1:
                pygame.draw.rect(screen, BLACK, (r*80, c*80-240+z, 80, 320))
                screen.blit (q2_img,(r*80,c*80))
                screen.blit (n2_img,(r*80,c*80-80*s))
                screen.blit (r2_img,(r*80,c*80-160*s))
                screen.blit (b2_img,(r*80,c*80-240*s))
        pygame.display.update()

    def finish_game(self):#mostrar un mensaje de fin de juego
        global check, go_type
        check = board.check(noturn)
        rect_circle(WHITE, 140, 165, 360, 310)
        rect_circle(GREEN, 140, 165, 360, 100)
        pygame.draw.rect(screen, GREEN, (140, 215, 360, 50))
        pygame.draw.rect(screen,GREY, (190, 390, 120, 42))
        pygame.draw.rect(screen,GREY, (330, 390, 120, 42))
        pygame.draw.rect(screen,LGREY, (190, 390, 120, 40))
        pygame.draw.rect(screen,LGREY, (330, 390, 120, 40))
        b1 = font3.render("Rematch", 1, GREY)
        b2 = font3.render("Quit", 1, GREY)
        screen.blit(b1,(205,400))
        screen.blit(b2,(367,400))
        if go_type == 'm':
            if check[0]:
                if color_turn[noturn] == WHITE:
                    won = font2.render("White won!", 1, WHITE)
                    rect_circle(LGREY, 350, 290, 80, 80)
                    rect_circle(GREEN, 210, 290, 80, 80)
                elif color_turn[noturn] == BLACK:
                    won = font2.render("Black won!", 1, WHITE)
                    rect_circle(LGREY, 210, 290, 80, 80)
                    rect_circle(GREEN, 350, 290, 80, 80)
                screen.blit(won,(225,180))
                mate = font.render("By Checkmate", 1, LGREEN)
                sc = font.render(str(score[0])+'-'+str(score[1]), 1, GREY)
            else:
                draw=font2.render("Draw",1,WHITE)
                screen.blit(draw,(265,180))
                rect_circle(LGREY, 350, 290, 80, 80)
                rect_circle(LGREY, 210, 290, 80, 80)
                mate = font.render("By Stalemate", 1, LGREEN)
                sc = font.render(str(score[0])+'-'+str(score[1]), 1, GREY)
        if go_type == 'f':
            draw=font2.render("Draw",1,WHITE)
            screen.blit(draw,(265,180))
            rect_circle(LGREY, 350, 290, 80, 80)
            rect_circle(LGREY, 210, 290, 80, 80)
            mate = font.render("By 50 moves rule", 1, LGREEN)
            sc = font.render(str(score[0])+'-'+str(score[1]), 1, GREY)
        screen.blit(sc,(312,325))
        screen.blit(P_img,(210,290))
        screen.blit(p_img,(350,290))
        screen.blit(mate,(250,230))

    def restart(self):#resetear el tablero a la posición inicial designada
        global last_cpm, flcpm
        last_cpm = flcpm
        self.position = [[0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0]]
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
    def __init__(self,img:pygame.Surface,color:tuple,piece:int,pos:list):#*#info general de pieza,
    #*# Tipo de pieza: 0 <=> nada, 1 <=> peon, 2 <=> caballo, 3 <=> alfil, 4 <=> torre, 5 <=> reina, 6 <=> rey
        self.image = img
        self.image2 = None
        self.pos = pos
        self.start_pos = pos
        if color == WHITE or color == BLACK:
            self.color = color
        if piece>0 and piece<7:
            self.type = piece
        self.lm = []

    def __repr__(self) -> str:
        if self.color == WHITE:
            return types[self.type-1].capitalize()
        else:
            return types[self.type-1]

    def move(self,new_pos,new_board,anim):#*#funcion mover pieza
    #*#(verifica si el movimiento es posible y si es asi, lo efectua, si es necesario hace la animación del movimiento)
    #*#(reproduce un sonido de colocar pieza)
        global turn, noturn, check, en_pssnt, rc_K, rc_Q, rc_k, rc_q, last_cpm, Nmove
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
                if self.type == 6:
                    if self.color == WHITE:
                        rc_K = False
                        rc_Q = False
                    else:
                        rc_k = False
                        rc_q = False
                elif self.type == 4:
                    if self.color == WHITE:
                        if self.start_pos[1] == 0:
                            rc_Q = False
                        elif self.start_pos[1] == 7:
                            rc_K = False
                    else:
                        if self.start_pos[1] == 0:
                            rc_q = False
                        elif self.start_pos[1] == 7:
                            rc_k = False
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
                            rook.draw(rx*80,ry*80)
                        py = fpy + distance_x * i
                        px = fpx + distance_y * i
                        self.draw(px*80,py*80)
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
                if piece_raised.type == 1:
                    last_cpm = 0
                else:
                    last_cpm += 1
                if turn == 0:
                    Nmove += 1

    def capture(self,new_pos,new_board,anim):#*#funcion capturar pieza
    #*#(verifica si la captura es posible y si es asi, la efectua, si es necesario hace la animación del movimiento)
    #*#(Reproduce un sonido de colocar y capturar una pieza)
        global turn, noturn, check, en_pssnt, rc_K, rc_Q, rc_k, rc_q, last_cpm, Nmove
        if not new_pos == self.pos:
            distance_x = (new_pos[0] - self.pos[0])/frames
            distance_y = (new_pos[1] - self.pos[1])/frames
            py = self.pos[0]
            px = self.pos[1]
            if new_pos in self.lm:
                pd = new_board.position[new_pos[0]][new_pos[1]]
                if pd.type == 4:
                    if pd.color == WHITE:
                        if pd.start_pos[1] == 0:
                            rc_Q = False
                        elif pd.start_pos[1] == 7:
                            rc_K = False
                    else:
                        if pd.start_pos[1] == 0:
                            rc_q = False
                        elif pd.start_pos[1] == 7:
                            rc_k = False
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
                        self.draw(px*80,py*80)
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
                last_cpm = 0
                if turn == 0:
                    Nmove += 1

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

    def draw(self,i,j):
        screen.blit(self.image,(i,j))
        if not self.image2 == None:
            screen.blit(self.image2,(i,j))


#|   ++++   Clase flechas   ++++   |#

class Arrows:
    def __init__(self,color:tuple,p1:list,p2:list):
        self.color = color
        self.bottom = p1
        self.top = p2

    def draw(self):
        (ax,ay) = (self.bottom[0]*80+40,self.bottom[1]*80+40)
        (bx,by) = (self.top[0]*80+40,self.top[1]*80+40)
        vec = (ax-bx,ay-by)
        invec = (-vec[1], vec[0])
        norm = ((ax-bx)**2+(ay-by)**2)**0.5
        dist = 20*3**0.5
        scal1 = (vec[0]/norm, vec[1]/norm)
        scal2 = (invec[0]/norm, invec[1]/norm)
        p1 = (ax,ay)
        p2 = (bx+30*scal1[0],by+30*scal1[1])
        p3 = (bx+dist*scal1[0]-5*scal2[0],by+dist*scal1[1]-5*scal2[1])
        p4 = (bx+dist*scal1[0]+5*scal2[0],by+dist*scal1[1]+5*scal2[1])
        pygame.draw.aaline(screen, self.color, p1, p2, 1)
        pygame.draw.aaline(screen, self.color, p2, p3, 1)
        pygame.draw.aaline(screen, self.color, p2, p4, 1)

#|   ++++   Clase casillas   ++++   |#

class Squares:
    def __init__(self,color:tuple,pos:list):
        self.color = color
        self.pos = pos

    def draw(self):
        (i1,j1) = self.pos
        if (rotate and fo == noturn) or (not rotate and fo == 1):
            (i1,j1) = (7-self.pos[0],7-self.pos[1])
        pygame.draw.rect(screen, self.color, (self.pos[1]*80, self.pos[0]*80, 80, 80))
        if not board.position[i1][j1] == 0:
            screen.blit (board.position[i1][j1].image,(self.pos[1]*80,self.pos[0]*80))

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
                    if not new_board.position[7][0]==0 and move_posible (new_board.position[7][0],[7,3],turn,new_board):
                        if [7,3] in self.lm:
                            return True
            if rc_K:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if not new_board.position[7][7]==0 and move_posible (new_board.position[7][7],[7,5],turn,new_board):
                        if [7,5] in self.lm:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if rc_q:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]-2:
                    if not new_board.position[0][0]==0 and move_posible (new_board.position[0][0],[0,3],turn,new_board):
                        if [0,3] in self.lm:
                            return True
            if rc_k:
                if new_pos[0]==self.pos[0] and new_pos[1]==self.pos[1]+2:
                    if not new_board.position[0][7]==0 and move_posible (new_board.position[0][7],[0,5],turn,new_board):
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

P_img = chessfont.render("o", 1, WHITE)
p_img = chessfont.render("o", 1, BLACK)
N_img = chessfont.render("m", 1, WHITE)
n_img = chessfont.render("m", 1, BLACK)
B_img = chessfont.render("v", 1, WHITE)
b_img = chessfont.render("v", 1, BLACK)
R_img = chessfont.render("t", 1, WHITE)
r_img = chessfont.render("t", 1, BLACK)
Q_img = chessfont.render("w", 1, WHITE)
q_img = chessfont.render("w", 1, BLACK)
K_img = chessfont.render("l", 1, WHITE)
k_img = chessfont.render("l", 1, BLACK)

p2_img = chessfont.render("p", 1, WHITE)
n2_img = chessfont.render("n", 1, WHITE)
b2_img = chessfont.render("b", 1, WHITE)
r2_img = chessfont.render("r", 1, WHITE)
q2_img = chessfont.render("q", 1, WHITE)
k2_img = chessfont.render("k", 1, WHITE)
images = [P_img,p_img,N_img,n_img,B_img,b_img,R_img,r_img,Q_img,q_img,K_img,k_img]

types = ['p','n','b','r','q','k']
imgtypes = ['o','m','v','t','w','l']

brd = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'#Codigo FEN

Wpieces = []
Bpieces = []
Pieces = []
K = 0
k = 0

board = Board(brd)
lines = ['8','7','6','5','4','3','2','1']
columnes = ['a','b','c','d','e','f','g','h']

#|   ++++   variables en posicion inicial  ++++   |#

mode = 0
menu = True
move = False
check=[False,None,False]
running = True

fps = 60
delay = 0.2
frames = int(fps*delay)
df = 1/fps

score = [0,0]

orientation = 0
fo = orientation
rotate = False

piece_raised = 0
pcd = None

promoting = [False,None,None,None]
en_pssnt = [False,None]
mouse_sq = []

psr = 0
cnt = 0

m_arw = 0
cnt_arws = 0
cnt_sqrs = 0
arws = []
sqrs = []

#|      ~~~~~      Interaccion grafica con el juego      ~~~~~      |#

#|   ++++   funciones al empezar el juego   ++++   |#

print(board)
print(repr(board))
board.reset_lm()
board.reset()
display_menu()
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
                        board.position[a][b].draw(b1*80,a1*80)
            if [N,M] in piece_raised.lm:
                board.reset_sq((n,m),GREY,LGREY)
                mselect = mp
                if not board.position[N][M] == 0:
                    board.position[N][M].draw(m*80,n*80)
                    mselect = cp
                screen.blit(ms_mp,(m*80,n*80))
                mouse_sq = [N,M]
            if not move:
                piece_raised.draw(m1-40,m2-40)
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#correcto apagado
            running = False
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:#click
            if event.button == BUTTON_LEFT:
                arws = []
                sqrs = []
                cnt_arws = 0
                cnt_sqrs = 0
                mouse_sq = []
                mselect = None
                Pos = event.pos
                (i,j) = Pos
                i = int(i/80)
                j = int(j/80)
                if promoting[0]:#solo si se esta coronando un peon(3°click)
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
                            if mode == 1:
                                pawn.image2 = q2_img
                        elif [j,i] == [r-n1,c]:
                            pawn.type = 2
                            pawn.image = n_img
                            if mode == 1:
                                pawn.image2 = n2_img
                        elif [j,i] == [r-n2,c]:
                            pawn.type = 4
                            pawn.image2 = r_img
                            if mode == 1:
                                pawn.image2 = r2_img
                        elif [j,i] == [r-n3,c]:
                            pawn.type = 3
                            pawn.image = b_img
                            if mode == 1:
                                pawn.image2 = b2_img
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
                    print(board)
                    print(repr(board))
                elif game_over():#interfaz de fin de juego
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
                elif menu:
                    (i,j) = Pos
                    if 190<i and i<310:
                        if 390<j and j<430:
                            board.restart()
                            turn = 0
                            noturn = 1
                            board.reset_lm()
                            mode = 0
                            menu = False
                            board.reset()
                    elif 330<i and i<450:
                        if 390<j and j<430:
                            board.restart()
                            turn = 0
                            noturn = 1
                            board.reset_lm()
                            mode = 1
                            menu = False
                            change_font()
                            board.reset()
                elif piece_raised == 0:#levantar pieza (1° click)
                    board.reset()
                    if (rotate and fo == noturn) or (not rotate and fo == 1):
                        (i,j) = (7-i,7-j)
                    if not board.position[j][i] == 0:
                        psr = piece_raised
                        piece_raised = board.position[j][i]#saber cual pieza y su posicion
                        if piece_raised.color == color_turn[noturn]:
                            piece_raised = 0
                        if board.position[j][i].color == color_turn[turn]:#saber cuando la pieza este en el aire
                            piece_raised.rsrch_lm(board)
                else:#colocar pieza(2° click)
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
                        m_arw = Arrows(color_turn[noturn],(old_pos[1],old_pos[0]),(piece_raised.pos[1],piece_raised.pos[0]))
                        if not promoting[0]:
                            print(board)
                            print(repr(board))
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
                                board.get_piece(columnes[i],lines[j]).draw(I*80,J*80)
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
            elif event.button == BUTTON_RIGHT and not menu:
                (y,x)=event.pos
                x = int(x/80)
                y = int(y/80)
        elif event.type == MOUSEBUTTONUP:
            if event.button == BUTTON_LEFT:
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
                        board.get_piece(columnes[i],lines[j]).draw(I*80,J*80)
                        board.show_lm(piece_raised)
                        break
                    if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                        piece_raised.move([j,i],board,False)
                    elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                        pcd = board.position[j][i]
                        piece_raised.capture([j,i],board,False)
                    if not old_pos == piece_raised.pos:
                        nt = orientation
                        m_arw = Arrows(color_turn[noturn],(old_pos[1],old_pos[0]),(piece_raised.pos[1],piece_raised.pos[0]))
                        if not promoting[0]:
                            print(board)
                            print(repr(board))
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
            elif event.button == BUTTON_RIGHT and not menu:
                if not piece_raised == 0:
                    piece_raised = 0
                    board.reset()
                (j,i)=event.pos
                i = int(i/80)
                j = int(j/80)
                (i1,j1) = (i,j)
                if (rotate and fo == noturn) or (not rotate and fo == 1):
                    (i1,j1) = (7-i,7-j)
                if (x,y) == (i,j):
                    if get_sqr((x,y)) == None:
                        sqr = Squares(RED, (x,y))
                        sqrs.append(sqr)
                        sqrs[cnt_sqrs].draw()
                        cnt_sqrs += 1
                        board.reset()
                    else:
                        cnt_sqrs += -1
                        sqrs.remove(get_sqr((x,y)))
                        board.reset()
                else:
                    if get_arw((y,x),(j,i)) == None:
                        arw = Arrows(LGREEN,(y,x),(j,i))
                        arws.append(arw)
                        arws[cnt_arws].draw()
                        cnt_arws += 1
                    else:
                        cnt_arws += -1
                        arws.remove(get_arw((y,x),(j,i)))
                        board.reset()
                pygame.display.update()