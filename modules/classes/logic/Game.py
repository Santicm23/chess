import pygame
import numpy as np

from modules.classes.logic.Piece import Piece
from modules.classes.esthetic.Board import Board
from modules.others.game_rules import move_posible, capture_posible

gp = Piece() #gap piece

class Game:
    def __init__(self, fen_code:str): # Constructor
        self.start_fen = fen_code
        self.position = np.full((8,8), gp)
        self.white_pieces = []
        self.black_pieces = []
        self.whites_turn = True
        self.check = False
        self.en_passant = None
        self.right_castle = {'K': False, 'Q': False, 'k': False, 'q': False}
        self.last_cpm = 0 #last capture or pawn move
        self.number_moves = 0
        fen(self, fen_code)
        self.board = Board()
        self.group = pygame.sprite.Group()
        self.group.add(self.board)
        for p in self.white_pieces + self.black_pieces:
            self.group.add(p)
        self.update(self.whites_turn)

    def __str__(self):
        ln = "  +---+---+---+---+---+---+---+---+\n"
        str_pos = '\n' + ln
        for i in range (8):
            str_pos += str(7-i+1) + ' |'
            for j in range (8):
                str_pos += ' ' + self.position[i,j].type + ' |'
            str_pos += '\n'
            str_pos += ln
        str_pos += "    a   b   c   d   e   f   g   h"
        return str_pos + '\n'

    def __repr__(self):
        fencode = ""
        rc = False
        for i in range (8):
            ctr = 0
            for j in range (8):
                if self.position[i,j].type == ' ':
                    ctr += 1
                else:
                    if ctr > 0:
                        fencode += str(ctr)
                        ctr = 0
                    fencode += self.position[i,j].type
            if ctr > 0:
                fencode += str(ctr)
            if i<7:
                fencode += '/'
        if self.whites_turn:
            fencode += ' w '
        else:
            fencode += ' b '
        for i in self.right_castle:
            if self.right_castle[i]:
                rc = True
                fencode += i
        if not rc:
            fencode += '-'
        fencode += ' - ' + str(self.last_cpm) + ' ' + str(self.number_moves)
        return fencode + '\n'

    def draw(self, surface:pygame.Surface):
        self.group.draw(surface)

    def update(self, pov:bool):
        self.board.update(pov, self.check)
        for p in self.white_pieces + self.black_pieces:
            p.update(pov)

    def get_piece(self, pos:np.ndarray):
        return self.position[pos[1],pos[0]]

    def set_piece(self, pos:np.array, piece:Piece):
        self.del_piece(piece.pos)
        piece.pos = np.array(pos)
        piece.update()
        self.position[pos[1],pos[0]] = piece

    def del_piece(self, pos:np.ndarray):
        self.position[pos[1],pos[0]] = gp

    def update_check(self):
        check = False
        self.whites_turn = not self.whites_turn
        if self.whites_turn:
            for p in self.white_pieces:
                if capture_posible(p, self.black_pieces[0].pos, self):
                    check = True
                    break
        else:
            for p in self.black_pieces:
                if capture_posible(p, self.white_pieces[0].pos, self):
                    check = True
                    break
        self.whites_turn = not self.whites_turn
        return check

    def move_is_legal(self, pos:np.ndarray, piece:Piece):
        t_piece = self.get_piece(pos)
        t_pos = piece.pos
        self.set_piece(pos, piece)
        if t_piece.type == ' ':
            legal = not self.update_check()
        else:
            if t_piece.type.isupper():
                del self.white_pieces[self.white_pieces.index(t_piece)]
                legal = not self.update_check()
                self.white_pieces.append(t_piece)
            else:
                del self.black_pieces[self.black_pieces.index(t_piece)]
                legal = not self.update_check()
                self.black_pieces.append(t_piece)
        self.set_piece(t_pos, piece)
        if not t_piece == gp:
            self.set_piece(pos, t_piece)
        return legal

    def update_piece_lm(self, piece):
        piece.legal_moves = []
        for i in range (8):
            for j in range(8):
                if move_posible(piece, (i,j), self) or capture_posible(piece, (i,j), self):
                    if self.move_is_legal((i,j), piece):
                        piece.legal_moves.append(np.array([i,j]))

    def update_legal_moves(self):
        for p in self.white_pieces + self.black_pieces:
            self.update_piece_lm(p)

    def update_right_castle(self, piece:Piece):
        if piece.type == 'k':
            self.right_castle['k'] = False
            self.right_castle['q'] = False
        elif piece.type == 'K':
            self.right_castle['K'] = False
            self.right_castle['Q'] = False
        elif piece.type.lower() == 'r':
            if (piece.pos == (0,0)).all():
                self.right_castle['q'] = False
            elif (piece.pos == (0,7)).all():
                self.right_castle['Q'] = False
            elif (piece.pos == (7,0)).all():
                self.right_castle['k'] = False
            elif( piece.pos == (7,7)).all():
                self.right_castle['K'] = False

    def update_en_passant(self, pos:np.ndarray, piece:Piece):
        self.en_passant = None
        if piece.type == 'p' and piece.pos[1]-pos[1] == -2:
            self.en_passant = piece.pos + (0,1)
        elif piece.type == 'P' and piece.pos[1]-pos[1] == 2:
            self.en_passant = piece.pos + (0,-1)

def fen(game, fen_code:str):# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 #
    fen_code = fen_code.split()
    fen_pos = fen_code[0].replace('/',' ').split()
    for i in range(len(fen_pos)):
        k = 0
        for j in fen_pos[i]:
            if j.isalpha():
                p = Piece(j, np.array([k,i]))
                game.position[i,k] = p
                if j.isupper():
                    if j == 'K':
                        game.white_pieces = [p] + game.white_pieces
                    else:
                        game.white_pieces.append(p)
                else:
                    if j == 'k':
                        game.black_pieces = [p] + game.black_pieces
                    else:
                        game.black_pieces.append(p)
                k += 1
            else:
                k += int(j)
    game.whites_turn = fen_code[1] == 'w'
    for i in game.right_castle.keys():
        game.right_castle[i] = i in fen_code[2]
    game.last_cpm = int(fen_code[4])
    game.number_moves = int(fen_code[5])