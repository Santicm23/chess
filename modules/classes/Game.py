from turtle import delay
import pygame

from modules.classes.logic.Piece import Piece, move_sound, capture_sound
from modules.classes.esthetic.Board import Board
from modules.others.constants import delay
from modules.others.game_rules import move_posible, lm_castle, capture_posible, en_passant, sum_tuples

np = Piece() #null piece

class Game:
    def __init__(self, fen_code:str):
        self.start_fen = fen_code
        self.position = [
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np],
            [np,np,np,np,np,np,np,np]
        ]
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
                str_pos += ' ' + self.position[i][j].type + ' |'
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
                if self.position[i][j].type == ' ':
                    ctr += 1
                else:
                    if ctr > 0:
                        fencode += str(ctr)
                        ctr = 0
                    fencode += self.position[i][j].type
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
        self.board.update(pov)
        for p in self.white_pieces + self.black_pieces:
            p.update(pov)

    def get_piece(self, pos:tuple):
        return self.position[pos[1]][pos[0]]

    def set_piece(self, pos:tuple, piece:Piece):
        self.del_piece(piece.pos)
        piece.pos = pos
        piece.update()
        self.position[pos[1]][pos[0]] = piece

    def del_piece(self, pos:tuple):
        self.position[pos[1]][pos[0]] = np

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

    def move(self, pos:list, piece:Piece, surface:pygame.Surface=None, clock=None):
        if self.get_piece(pos) == np:
            if piece.type.lower() == 'p':
                self.last_cpm = 0
                if en_passant(piece, pos, self):
                    if piece.type == 'P':
                        pawn = self.get_piece(sum_tuples(pos,(0,1)))
                        self.black_pieces.pop(self.black_pieces.index(pawn)).kill()
                    elif piece.type == 'p':
                        pawn = self.get_piece(sum_tuples(pos,(0,-1)))
                        self.white_pieces.pop(self.white_pieces.index(pawn)).kill()
                    self.del_piece(pawn.pos)
                    if not surface == None:
                        piece.animate(surface, clock, self, pos, True)
                    else:
                        capture_sound.play()
                elif not surface == None:
                    piece.animate(surface, clock, self, pos)
                else:
                    move_sound.play()
            else:
                self.last_cpm += 1
                if lm_castle(piece, pos, self):
                    if pos[0] == 6:
                        rook = self.get_piece(sum_tuples(pos,(1,0)))
                        if not surface == None:
                            piece.animate_castle(surface, clock, self, pos, rook, sum_tuples(pos,(-1,0)))
                        else:
                            move_sound.play()
                            pygame.time.delay(int(delay*400))
                            move_sound.play()
                        self.set_piece(sum_tuples(pos,(-1,0)), rook)
                    else:
                        rook = self.get_piece(sum_tuples(pos,(-2,0)))
                        if not surface == None:
                            piece.animate_castle(surface, clock, self, pos, rook, sum_tuples(pos,(1,0)))
                        else:
                            move_sound.play()
                            pygame.time.delay(int(delay*400))
                            move_sound.play()
                        self.set_piece(sum_tuples(pos,(1,0)), rook)
                elif not surface == None:
                    piece.animate(surface, clock, self, pos)
                else:
                    move_sound.play()
        else:
            if not surface == None:
                piece.animate(surface, clock, self, pos)
            else:
                move_sound.play()
                capture_sound.play()
            self.last_cpm = 0
            if self.whites_turn:
                self.black_pieces.pop(self.black_pieces.index(self.get_piece(pos))).kill()
            else:
                self.white_pieces.pop(self.white_pieces.index(self.get_piece(pos))).kill()
        self.update_right_castle(piece)
        self.update_en_passant(pos, piece)
        self.set_piece(pos, piece)
        self.whites_turn = not self.whites_turn
        self.update_legal_moves()
        if self.whites_turn: self.number_moves += 1
        self.check = self.update_check()
        print(self.check)
        print(self)
        print(repr(self))

    def move_is_legal(self, pos:tuple, piece:Piece):
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
        if not t_piece == np:
            self.set_piece(pos, t_piece)
        return legal

    def update_legal_moves(self):
        for p in self.white_pieces + self.black_pieces:
            p.legal_moves = []
            for i in range (8):
                for j in range(8):
                    if move_posible(p, (i,j), self) or capture_posible(p, (i,j), self):
                        if self.move_is_legal((i,j), p):
                            p.legal_moves.append((i,j))

    def update_right_castle(self, piece:Piece):
        if piece.type == 'k':
            self.right_castle['k'] = False
            self.right_castle['q'] = False
        elif piece.type == 'K':
            self.right_castle['K'] = False
            self.right_castle['Q'] = False
        elif piece.type.lower() == 'r':
            if piece.pos == (0,0):
                self.right_castle['q'] = False
            elif piece.pos == (0,7):
                self.right_castle['Q'] = False
            elif piece.pos == (7,0):
                self.right_castle['k'] = False
            elif piece.pos == (7,7):
                self.right_castle['K'] = False

    def update_en_passant(self, pos:list, piece:Piece):    
        self.en_passant = None
        if piece.type == 'p' and piece.pos[1]-pos[1] == -2:
            self.en_passant = sum_tuples(piece.pos, (0,1))
        elif piece.type == 'P' and piece.pos[1]-pos[1] == 2:
            self.en_passant = sum_tuples(piece.pos, (0,-1))

def fen(game:Game, fen_code:str):# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 #
    fen_code = fen_code.split()
    fen_pos = fen_code[0].replace('/',' ').split()
    for i in range(len(fen_pos)):
        k = 0
        for j in fen_pos[i]:
            if j.isalpha():
                p = Piece(j, (k,i))
                game.position[i][k] = p
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