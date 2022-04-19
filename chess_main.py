#|-   -   -   -   -   -   -Codigo de Santiago Castro Muñoz (2021-2022)-   -   -   -   -   -   -|#


#|      ~~~~~      Inicio codigo (constantes)      ~~~~~      |#

#|   ++++   Importaciones e inicio de pygame y su pantalla   ++++   |#

import pygame, sys
from pygame.locals import *
pygame.init()
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")
icon = pygame.image.load("imgs/icon.png")
pygame.display.set_icon(icon)

#|   ++++   Fuentes   ++++   |#

font = pygame.font.SysFont("Gerbera", 16)
font2 = pygame.font.SysFont("Gerbera", 40)
font3 = pygame.font.SysFont("Gerbera", 30)
chessfont = pygame.font.Font("fonts/CASEFONT.TTF", 80)

#|   ++++   Colores en RGB   ++++   |#

BLACK = (0,0,0)
WHITE = (225,225,225)
GREY = (125,125,125)
LGREY = (155,155,155)
GREEN = (107,142,35)
LGREEN = (163,217,54)
RED = (205,92,92)

#|   ++++   variables en posicion inicial  ++++   |#

running = True #Si el progrma esta corriendo
mode = 0 #el modo en el que esta (0: jugar, 1: analisis)
menu = True #si esta en el menu o no
move = False #si la pieza seleccionada tiene que moverse o el usuario la arrastro
check=[False,None] #datos del jaque [hay jaque?, que pieza?]
clock = pygame.time.Clock() #reloj de pygame

fps = 60 #fotos por segundo
delay = 0.2 #delay del sonido en segundos
frames = int(fps*delay) #fotos

score = [0,0] #puntaje [puntos del blanco, puntos del negro]

orientation = 0 #orinetation del juego 0:blanco, 1:negro
fo = orientation #primera orientación
rotate = True #rotar el tablero despues de cada jugada

piece_raised = 0 #pieza seleccionada (levantada)
pcd = None #pieza capturada

promoting = [False,None,None,None] #datos de la coronación [coronacion?, peon coronando,
#pieza capturada, posición anterior del peon]
en_pssnt = [False,None] #datos de la captura al paso [captura al paso?, ]
mouse_sq = []

cnt = 0 #contador de jugadas

m_arw = 0 #flecha del ultimo movimiento
cnt_arws = 0 
cnt_sqrs = 0
arws = []
sqrs = []

#|   ++++   Imagenes de diseño   ++++   |#

r_sq = pygame.image.load("imgs/raised_square.png").convert_alpha()
mp = pygame.image.load("imgs/mp.png").convert_alpha()
cp = pygame.image.load("imgs/cp.png").convert_alpha()
ms_mp = pygame.image.load("imgs/ms_mp.png").convert_alpha()

#|   ++++   Sonidos   ++++   |#

move_sound = pygame.mixer.Sound("sounds/piece_dropped.mp3")
capture_sound = pygame.mixer.Sound("sounds/piece_capturing.mp3")

#|   ++++   Variables principales   ++++   |#

rc_Q = True #si las blancas pueden enrrocarse largo
rc_K = True #si las blancas pueden enrrocarse corto
rc_q = True #si las negras pueden enrrocarse largo
rc_k = True #si las negras pueden enrrocarse corto
turn = 0 #turno 0:blanco, 1:negro
noturn = 0 #el opuesto del valor del turno
color_turn = [WHITE,BLACK] #color según el turno
last_cpm = 0 #cantidad de jugadas desde la última captura
flcpm = 0
Nmove = 1
fmove = 1
go_type = '' #tipo de fin de juego


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
        ps.image2 = chessfont.render(types[ps.type-1], 1, WHITE)
        ps.image.blit(ps.image2,(0,0))

def change_orintation(pov):
    board.reset()
    if pov == 0:
        for p in Pieces:
            p.update((p.pos[1]*80, p.pos[0]*80))
    else:
        for p in Pieces:
            p.update(((7-p.pos[1])*80, (7-p.pos[0])*80))
    reset()

#|   ++++   Principales   ++++   |#

def change_turn():
    global turn, noturn
    if turn == 0:
        (turn,noturn)=(1,0)
    else:
        (turn,noturn)=(0,1)

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

def reset():
    boardgroup.draw(screen)
    piecegroup.draw(screen)
    reset_draws()

#|      ~~~~~      Clases      ~~~~~      |#

#|   ++++   Clase tablero   ++++   |#

class Board(pygame.sprite.Sprite):
    def __init__(self,brd:str):#creacion de la posicion inicial
        super().__init__()
        self.position = fen(brd)
        self.image = pygame.Surface((640,640))
        self.rect = self.image.get_rect()

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
                else:
                    rt += ' ' + types[self.position[i][j].type-1] + ' |'
            rt += '\n'
            rt += ln
        rt += cols
        return rt + '\n'

    def __repr__(self) -> str:
        """rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"""
        fencode = ""
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

    def set_piece(self,i,j,piece):#colocar pieza en posicion (i,j)
        (x,y) = (lines.index(j),columnes.index(i))
        piece.pos = [x,y]
        self.position[x][y] = piece

    def reset(self):#reiniciar el tablero según el turno y la orientación indicada
        if mode == 0:
            pygame.draw.rect(self.image, LGREY, (0, 0, 640, 640))
            for i in range (8):
                for j in range ((i-1)%2, 8, 2):
                    pygame.draw.rect(self.image, GREY, (i*80, j*80, 80, 80))
        else:
            lsq = chessfont.render("+",1,GREY)
            pygame.draw.rect(self.image, BLACK, (0, 0, 640, 640))
            for i in range (8):
                for j in range ((i)%2, 8, 2):
                    self.image.blit(lsq,(i*80,j*80))
        for l in range (8):
            nbr=font.render(lines[l],1,WHITE)
            l1=l
            if orientation==1:
                l1=7-l
            self.image.blit(nbr,(2, l1*80+2))
        for c in range (8):
            ltr=font.render(columnes[c],1,WHITE)
            c1=c
            if orientation==1:
                c1=7-c
            self.image.blit(ltr,(71+c1*80, 67+7*80))

    def show_lm(self,piece):#mostrar jugadas posibles de la pieza seleccionada
        for m in piece.lm:
            (i,j) = m
            (i1,j1) = (i,j)
            if orientation == 1: (i1,j1) = (7-i, 7-j)
            if move_posible(piece,[i,j],turn,self) or lm_castle(piece,[i,j],turn,self):
                screen.blit(mp,(j1*80+30,i1*80+30))
            elif capture_posible(piece,[i,j],turn,self):
                if not self.position[i][j] == 0:
                    self.position[i][j].draw(j1*80,i1*80)
                    screen.blit(cp,(j1*80,i1*80))
                else:
                    screen.blit(mp,(j1*80+30,i1*80+30))

    def reset_lm(self):#resetear las jugadas posibles de todas la piezas presentes en el tablero
        for wp in Wpieces:
            wp.rsrch_lm(self)
        for bp in Bpieces:
            bp.rsrch_lm(self)

    def check(self,t):#detenerminar si hay Jaque en la posicion
        tc=[False,None]
        counter=0
        if t == 0:
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

    def promote(self,new_pos,color):#mostrar recuadro de pizas para elegir que pieza coronar
        (c,r) = new_pos
        s = 1
        z = 0
        if orientation == 1:
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
        global last_cpm, flcpm, orientation, fo
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
                    piecegroup.add(p)
            elif p.color == BLACK:
                if not p in Bpieces:
                    Bpieces.append(p)
                    piecegroup.add(p)
            p.update((x*80,y*80))
        orientation = fo
        change_orintation(fo)

#|   ++++   Clase piezas   ++++   |#

class Piece(pygame.sprite.Sprite):
    def __init__(self,img:pygame.Surface,color:tuple,piece:int,pos:list):#*#info general de pieza,
    #*# Tipo de pieza: 0 <=> nada, 1 <=> peon, 2 <=> caballo, 3 <=> alfil, 4 <=> torre, 5 <=> reina, 6 <=> rey
        super().__init__()
        self.image = img
        self.image2 = None
        self.pos = pos
        self.start_pos = pos
        if color == WHITE or color == BLACK:
            self.color = color
        assert piece>0 and piece<7
        self.type = piece
        self.lm = []
        self.rect = img.get_rect(topleft = (pos[1]*80,pos[0]*80))

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
            (py, px) = self.pos
            (npy,npx) = new_pos
            cstl = False
            if turn == 0:
                ep = 1
            else:
                ep = -1
            if lm_castle(self,new_pos,turn,new_board) and not check[0]: cstl = True
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
                if self.type == 1 and self.pos[0]-new_pos[0] == ep*2: en_pssnt = [True,[new_pos[0]+ep,new_pos[1]]]
                else: en_pssnt = [False,None]
                if cstl:
                    if new_pos[1] == 2:
                        if self.color == WHITE: rm = [[7,3],[7,0]]
                        else: rm = [[0,3],[0,0]]
                    elif new_pos[1] == 6:
                        if self.color == WHITE: rm = [[7,5],[7,7]]
                        else: rm = [[0,5],[0,7]]
                    ry = rm[1][0]
                    rx = rm[1][1]
                    dr_x = (rm[0][0]-ry)/frames
                    dr_y = (rm[0][1]-rx)/frames
                    rook = new_board.position[ry][rx]
                    new_board.position[ry][rx] = 0
                new_board.position[py][px] = 0
                if orientation == 1:
                    (npx,npy) = (7-npx,7-npy)
                if not anim:
                    move_sound.play()
                else:
                    (fpy,fpx) = self.pos
                    if cstl: (fry,frx) = rm[1]
                    if orientation == 1:
                        (px,py) = (7-px,7-py)
                        (distance_x,distance_y) = (-distance_x,-distance_y)
                        (fpx,fpy) = (7-fpx,7-fpy)
                        if cstl:
                            (rx,ry) = (7-rx,7-ry)
                            (dr_x,dr_y) = (-dr_x,-dr_y)
                            (frx,fry) = (7-frx,7-fry)
                    for i in range (frames+1):
                        boardgroup.draw(screen)
                        piecegroup.draw(screen)
                        if cstl:
                            ry = fry + dr_x * i
                            rx = frx + dr_y * i
                            rook.update((rx*80,ry*80))
                        py = fpy + distance_x * i
                        px = fpx + distance_y * i
                        self.update((px*80,py*80))
                        boardgroup.draw(screen)
                        piecegroup.draw(screen)
                        pygame.display.update()
                        if i == frames*2/3: move_sound.play()
                        clock.tick(60)
                new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                self.update((npx*80,npy*80))
                if cstl:
                    new_board.set_piece(columnes[rm[0][1]],lines[rm[0][0]],rook)
                    rook.update((rm[0][1]*80,rm[0][0]*80))
                    if not anim: pygame.time.delay(int(delay*400))
                    move_sound.play()
                change_turn()
                if piece_raised.type == 1: last_cpm = 0
                else: last_cpm += 1
                if turn == 0: Nmove += 1

    def capture(self,new_pos,new_board,anim):#*#funcion capturar pieza
    #*#(verifica si la captura es posible y si es asi, la efectua, si es necesario hace la animación del movimiento)
    #*#(Reproduce un sonido de colocar y capturar una pieza)
        global turn, noturn, check, en_pssnt, rc_K, rc_Q, rc_k, rc_q, last_cpm, Nmove
        if not new_pos == self.pos:
            distance_x = (new_pos[0] - self.pos[0])/frames
            distance_y = (new_pos[1] - self.pos[1])/frames
            (npy,npx) = new_pos
            py = self.pos[0]
            px = self.pos[1]
            if new_pos in self.lm:
                pd = new_board.position[new_pos[0]][new_pos[1]]
                if not pd == 0 and pd.type == 4:
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
                if orientation == 1:
                    (npx,npy) = (7-npx,7-npy)
                if not anim:
                    move_sound.play()
                    capture_sound.play()
                else:
                    (fpy,fpx) = self.pos
                    if orientation == 1:
                        (px,py) = (7-px,7-py)
                        (distance_x,distance_y) = (-distance_x,-distance_y)
                        (fpx,fpy) = (7-fpx,7-fpy)
                    for i in range (frames+1):
                        boardgroup.draw(screen)
                        piecegroup.draw(screen)
                        py = fpy + distance_x * i
                        px = fpx + distance_y * i
                        self.update((px*80,py*80))
                        pygame.display.update()
                        if i == frames/2:
                            move_sound.play()
                            capture_sound.play()
                        clock.tick(60)
                new_board.set_piece(columnes[new_pos[1]],lines[new_pos[0]],self)
                self.update((npx*80,npy*80))
                change_turn()
                pd.kill()
                if self.color == WHITE:
                    del Bpieces[Bpieces.index(pd)]
                else:
                    del Wpieces[Wpieces.index(pd)]
                last_cpm = 0
                if turn == 0:
                    Nmove += 1

    def rsrch_lm(self,new_board):#*#calcular jugadas posibles de la pieza misma y guradarlas en una lista
        (y,x) = self.pos
        self.lm = []
        for i in range (8):
            for j in range(8):
                if move_posible(self,[i,j],turn,new_board) or lm_castle(self,[i,j],turn,new_board):
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[j],lines[i],self)
                    ilegal = new_board.check(noturn)
                    if not ilegal[0]:
                        self.lm.append([i,j])
                    new_board.position[self.pos[0]][self.pos[1]] = 0
                    new_board.set_piece(columnes[x],lines[y],self)
                elif capture_posible(self,[i,j],turn,new_board):
                    if not new_board.position[i][j] == 0:
                        pd = new_board.position[i][j]
                        new_board.position[self.pos[0]][self.pos[1]] = 0
                        new_board.set_piece(columnes[j],lines[i],self)
                        if pd.color == WHITE:
                            del Wpieces[Wpieces.index(pd)]
                            ilegal = new_board.check(noturn)
                            Wpieces.append(pd)
                        else:
                            del Bpieces[Bpieces.index(pd)]
                            ilegal = new_board.check(noturn)
                            Bpieces.append(pd)
                        if not ilegal[0]:
                            self.lm.append([i,j])
                        new_board.set_piece(columnes[x],lines[y],self)
                        new_board.set_piece(columnes[j],lines[i],pd)
                    elif en_passant(self,[i,j],turn,new_board):
                        if self.color == WHITE:
                            a,b = i+1,j
                        else:
                            a,b = i-1,j
                        pd = new_board.position[a][b]
                        new_board.position[a][b] = 0
                        new_board.position[self.pos[0]][self.pos[1]] = 0
                        new_board.set_piece(columnes[j],lines[i],self)
                        ilegal = new_board.check(noturn)
                        if not ilegal[0]:
                            self.lm.append([i,j])
                        new_board.position[a][b] = pd
                        new_board.position[self.pos[0]][self.pos[1]] = 0
                        new_board.set_piece(columnes[x],lines[y],self)

    def draw(self,i,j):
        screen.blit(self.image,(i,j))

    def update(self,pos):
        self.rect = self.image.get_rect(topleft = (pos[0],pos[1]))

#|   ++++   Clase flechas   ++++   |#

class Arrows(pygame.sprite.Sprite):
    def __init__(self,color:tuple,p1:list,p2:list):
        super().__init__()
        self.color = color
        self.bottom = (p1[1],p1[0])
        self.top = (p2[1],p2[0])
        self.image = pygame.Surface((640, 640))

    def draw(self):
        (ax,ay) = (self.bottom[0]*80+40,self.bottom[1]*80+40)
        (bx,by) = (self.top[0]*80+40,self.top[1]*80+40)
        vec = (ax-bx,ay-by)
        invec = (-vec[1], vec[0])
        norm = ((ax-bx)**2+(ay-by)**2)**0.5
        scal1 = (vec[0]/norm, vec[1]/norm)
        scal2 = (invec[0]/norm, invec[1]/norm)
        if self.top[0]-self.bottom[0] == self.top[1]-self.bottom[1]:
            c1 = 44
            c2 = 49
        else:
            c1 = 37
            c2 = 42
        c3 = 3
        p1 = (ax,ay)
        p2 = (bx+c1*scal1[0],by+c1*scal1[1])
        p3 = (bx+c2*scal1[0]-c3*scal2[0],by+c2*scal1[1]-c3*scal2[1])
        p4 = (bx+c2*scal1[0]+c3*scal2[0],by+c2*scal1[1]+c3*scal2[1])
        pygame.draw.aaline(self.image, self.color, p1, p2, 1)
        pygame.draw.aaline(self.image, self.color, p2, p3, 1)
        pygame.draw.aaline(self.image, self.color, p2, p4, 1)

    def update(self, p1, p2):
        pass

#|   ++++   Clase casillas   ++++   |#

class Squares(pygame.sprite.Sprite):
    def __init__(self,color:tuple,pos:list):
        super().__init__()
        self.color = color
        self.pos = pos

    def draw(self):
        global orientation
        (i1,j1) = self.pos
        if orientation == 1:
            (i1,j1) = (7-self.pos[0],7-self.pos[1])
        pygame.draw.rect(screen, self.color, (j1*80, i1*80, 80, 80))
        if not board.position[self.pos[0]][self.pos[1]] == 0:
            screen.blit (board.position[self.pos[0]][self.pos[1]].image,(j1*80,i1*80))

    def update(self, pos):
        pass

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
                        if new_pos[0] == self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.position[new_pos[0]][new_pos[1]].color == BLACK:
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
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.position[new_pos[0]][new_pos[1]].color == WHITE:
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
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b and new_board.position[new_pos[0]][new_pos[1]].color == BLACK:
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
                        if new_pos[0]==self.pos[0]+q*a and new_pos[1]==self.pos[1]+q*b and  new_board.position[new_pos[0]][new_pos[1]].color == WHITE:
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
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and  new_board.position[new_pos[0]][new_pos[1]].color == BLACK:
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
                        if new_pos[0]==self.pos[0]+q*c and new_pos[1]==self.pos[1]+q*d and new_board.position[new_pos[0]][new_pos[1]].color == WHITE:
                            return True
def lmc_king(self,new_pos,t,new_board):#calcula si la posicion dada es una jugada o captura del rey dado
    if new_board.position[self.pos[0]][self.pos[1]].type == 6:
        if new_board.position[self.pos[0]][self.pos[1]].color == WHITE and t == 0:#blanco
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==self.pos[0]+c and new_pos[1]==self.pos[1]+d:
                        if not  new_board.position[new_pos[0]][new_pos[1]] == 0 and new_board.position[new_pos[0]][new_pos[1]].color == BLACK:
                            return True
                        elif new_board.position[new_pos[0]][new_pos[1]] == 0:
                            return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            for c in range (-1,2):
                for d in range (-1,2):
                    if new_pos[0]==self.pos[0]+c and new_pos[1]==self.pos[1]+d:
                        if not  new_board.position[new_pos[0]][new_pos[1]] == 0 and new_board.position[new_pos[0]][new_pos[1]].color == WHITE:
                            return True
                        elif new_board.position[new_pos[0]][new_pos[1]] == 0:
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
                    if new_board.position[new_pos[0]][new_pos[1]] == 0 or new_board.position[new_pos[0]][new_pos[1]].color == BLACK:
                        return True
        elif new_board.position[self.pos[0]][self.pos[1]].color == BLACK and t == 1:#negro
            if new_pos[0] == self.pos[0]+1:
                if new_pos[1] == self.pos[1]-1 or new_pos[1] == self.pos[1]+1:
                    if new_board.position[new_pos[0]][new_pos[1]] == 0 or new_board.position[new_pos[0]][new_pos[1]].color == WHITE:
                        return True
def en_passant(self,new_pos,t,new_board):#calcula si la posicion dada es una captura al paso del peón dado
    if lc_pawn(self,new_pos,t,new_board):
        if new_board.position[new_pos[0]][new_pos[1]] == 0:
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

P_img = chessfont.render('o', 1, WHITE)
p_img = chessfont.render('o', 1, BLACK)
N_img = chessfont.render('m', 1, WHITE)
n_img = chessfont.render('m', 1, BLACK)
B_img = chessfont.render('v', 1, WHITE)
b_img = chessfont.render('v', 1, BLACK)
R_img = chessfont.render('t', 1, WHITE)
r_img = chessfont.render('t', 1, BLACK)
Q_img = chessfont.render('w', 1, WHITE)
q_img = chessfont.render('w', 1, BLACK)
K_img = chessfont.render('l', 1, WHITE)
k_img = chessfont.render('l', 1, BLACK)

p2_img = chessfont.render('p', 1, WHITE)
n2_img = chessfont.render('n', 1, WHITE)
b2_img = chessfont.render('b', 1, WHITE)
r2_img = chessfont.render('r', 1, WHITE)
q2_img = chessfont.render('q', 1, WHITE)
k2_img = chessfont.render('k', 1, WHITE)
images = [P_img,p_img,N_img,n_img,B_img,b_img,R_img,r_img,Q_img,q_img,K_img,k_img] #lista de imagenes

types = ['p','n','b','r','q','k'] #tipos de piezas
imgtypes = ['o','m','v','t','w','l'] #tipos de imagenes

brd = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #Codigo FEN de la posición inicial del ajedrez

Wpieces = [] #lista de piezas blancas
Bpieces = [] #lista de piezas negras
Pieces = [] #lista de todas las piezas
K = 0 #rey blanco
k = 0 #rey negro

board = Board(brd) #tablero
lines = ['8','7','6','5','4','3','2','1'] #filas (al revez para la impresión)
columnes = ['a','b','c','d','e','f','g','h'] #columnas

#groups (para un mejor uso de las imagenes)

boardgroup = pygame.sprite.GroupSingle() #grupo del tablero
boardgroup.add(board) #añadir el tablero

piecegroup = pygame.sprite.Group() #grupo de las piezas
for ps in Pieces:
    piecegroup.add(ps) #añadir todas las piezas

arrowsgroup = pygame.sprite.Group()

#|      ~~~~~      Interaccion grafica con el juego      ~~~~~      |#

#|   ++++   funciones al empezar el juego   ++++   |#

print(board)
print(repr(board))
board.reset_lm()
board.reset()
change_orintation(fo)
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
        if orientation == 1:
            (M,N) = (7-m,7-n)
            (I,J) = (7-i,7-j)
        if not move:
            (m1,m2) = pos
        reset()
        board.show_lm(piece_raised)
        screen.blit(r_sq,(I*80,J*80))
        if len(mouse_sq) == 2 and not mouse_sq == (N,M):
            (a,b) = mouse_sq
            (a1,b1) = mouse_sq
            if orientation == 1:
                (a1,b1) = (7-a1,7-b1)
            if mselect == mp:
                screen.blit(mp,(b1*80+30,a1*80+30))
            elif mselect == cp:
                screen.blit(cp,(b1*80,a1*80))
                if not board.position[a][b] == 0:
                    board.position[a][b].draw(b1*80,a1*80)
        if [N,M] in piece_raised.lm:
            reset()
            board.show_lm(piece_raised)
            screen.blit(r_sq,(I*80,J*80))
            mselect = mp
            if not board.position[N][M] == 0:
                mselect = cp
            screen.blit(ms_mp,(m*80,n*80))
            mouse_sq = [N,M]
        if move:
            piece_raised.draw(I*80,J*80)
        else:
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
                    if orientation == 1:
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
                            if not pcd == None:
                                Bpieces.append(pcd)
                                board.position[r][c] = pcd
                                piecegroup.add(pcd)
                                pcd.update((pcd.pos[1]*80, pcd.pos[1]*80))
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
                            if not pcd == None:
                                Wpieces.append(pcd)
                                board.position[r][c] = pcd
                                pcd.update((pcd.pos[1]*80, pcd.pos[1]*80))
                                pcd = None
                            else:
                                board.position[r][c] = 0
                            board.set_piece(columnes[x],lines[y],pawn)
                            (turn,noturn)=(1,0)
                    if rotate:
                        if fo == 0: orientation = turn
                        else: orientation = noturn
                        change_orintation(orientation)
                    promoting = [False,None,None,None]
                    board.reset_lm()
                    reset()
                    pygame.display.update()
                    print(board)
                    print(repr(board))
                elif game_over():#interfaz de fin de juego
                    (i,j) = Pos
                    if 190<i and i<310:
                        if 390<j and j<430:
                            m_arw = 0
                            board.restart()
                            turn = 0
                            noturn = 1
                            check = board.check(noturn)
                            board.reset_lm()
                            board.reset()
                            reset()
                            pygame.display.update()
                    elif 330<i and i<450:
                        if 390<j and j<430:
                            pygame.quit()
                            running = False
                            sys.exit()
                elif menu:
                    menu = False
                    (i,j) = Pos
                    turn = 0
                    noturn = 1
                    if (190<i and i<310) and (390<j and j<430):
                        mode = 0
                    elif (330<i and i<450) and (390<j and j<430):
                        mode = 1
                        change_font()
                    board.reset_lm()
                    board.reset()
                    reset()
                    pygame.display.update()
                elif piece_raised == 0:#levantar pieza (1° click)
                    if orientation == 1:
                        (i,j) = (7-i,7-j)
                    if not board.position[j][i] == 0:
                        piece_raised = board.position[j][i]#saber cual pieza y su posicion
                        if piece_raised.color == color_turn[noturn]:
                            piece_raised = 0
                        if board.position[j][i].color == color_turn[turn]:#saber cuando la pieza este en el aire
                            piece_raised.rsrch_lm(board)
                            board.show_lm(piece_raised)
                            screen.blit(r_sq,(i*80,j*80))
                else:#colocar pieza(2° click)
                    (I,J) = (i,j)
                    if orientation == 1:
                        (i,j) = (7-i,7-j)
                    old_pos = piece_raised.pos
                    if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                        piece_raised.move([j,i],board,True)
                    elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                        pcd = board.position[j][i]
                        piece_raised.capture([j,i],board,True)
                    if not old_pos == piece_raised.pos:
                        m_arw = Arrows(color_turn[noturn],old_pos,piece_raised.pos)
                        if piece_raised.type == 1:
                            if piece_raised.pos[0] == 0:
                                promoting = [True,piece_raised,pcd,old_pos]
                            elif piece_raised.pos[0] == 7:
                                promoting = [True,piece_raised,pcd,old_pos]
                            else:
                                board.reset_lm()
                                print(board)
                                print(repr(board))
                        else:
                            board.reset_lm()
                            print(board)
                            print(repr(board))
                        if rotate and not promoting[0]:
                            if fo == 0: orientation = turn
                            else: orientation = noturn
                            change_orintation(orientation)
                        check = board.check(noturn)
                    if not board.position[j][i] == piece_raised and not board.position[j][i] == 0:
                        board.reset()
                        piece_raised = board.position[j][i]
                        screen.blit(r_sq,(I*80,J*80))
                        board.position[j][i].draw(I*80,J*80)
                        piece_raised.rsrch_lm(board)
                        board.show_lm(piece_raised)
                        pygame.display.update()
                    else:
                        piece_raised = 0
                        reset()
                        pygame.display.update()
                    if promoting[0]:
                        board.promote(promoting[1].pos,promoting[1].color)
                    elif game_over():
                        if check[0]:
                            if color_turn[noturn] == WHITE:
                                score[0] += 1
                            elif color_turn[noturn] == BLACK:
                                score[1] += 1
                        else:
                            score[0] += 0.5
                            score[1] += 0.5
                        board.finish_game()
                        pygame.display.update()
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
                    if orientation == 1:
                        (i,j) = (7-i,7-j)
                    old_pos = piece_raised.pos
                    if [j,i] == piece_raised.pos:
                        move = True
                        reset()
                        screen.blit(r_sq,(I*80,J*80))
                        board.position[j][i].draw(I*80,J*80)
                        board.show_lm(piece_raised)
                        break
                    if board.position[j][i] == 0 and not en_passant(piece_raised,[j,i],turn,board):
                        piece_raised.move([j,i],board,False)
                    elif not board.position[j][i] == 0 or en_passant(piece_raised,[j,i],turn,board):
                        pcd = board.position[j][i]
                        piece_raised.capture([j,i],board,False)
                    if not old_pos == piece_raised.pos:
                        m_arw = Arrows(color_turn[noturn],old_pos,piece_raised.pos)
                        if piece_raised.type == 1:
                            if piece_raised.pos[0] == 0:
                                promoting = [True,piece_raised,pcd,old_pos]
                            elif piece_raised.pos[0] == 7:
                                promoting = [True,piece_raised,pcd,old_pos]
                            else:
                                board.reset_lm()
                                print(board)
                                print(repr(board))
                        else:
                            board.reset_lm()
                            print(board)
                            print(repr(board))
                        if rotate and not promoting[0]:
                            if fo == 0: orientation = turn
                            else: orientation = noturn
                            change_orintation(orientation)
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
                    reset()
                    pygame.display.update()
                    if promoting[0]:
                        board.promote(promoting[1].pos,promoting[1].color)
                    elif game_over() and not promoting[0]:
                        if check[0]:
                            if color_turn[noturn] == WHITE:
                                score[0] = score[0] + 1
                            elif color_turn[noturn] == BLACK:
                                score[1] = score[1] + 1
                        else:
                            score[0] = score[0] + 0.5
                            score[1] = score[1] + 0.5
                        board.finish_game()
                        pygame.display.update()
                    move = False      
            elif event.button == BUTTON_RIGHT and not menu:
                if not piece_raised == 0:
                    piece_raised = 0
                    board.reset()
                (j,i)=event.pos
                i = int(i/80)
                j = int(j/80)
                (i1,j1) = (i,j)
                if orientation == 1:
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
                        arw = Arrows(LGREEN,(x,y),(i,j))
                        arws.append(arw)
                        arws[cnt_arws].draw()
                        cnt_arws += 1
                    else:
                        cnt_arws += -1
                        arws.remove(get_arw((x,y),(i,j)))
                        board.reset()
                pygame.display.update()
    clock.tick(60)