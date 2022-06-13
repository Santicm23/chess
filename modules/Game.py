import pygame

from modules.Piece import Piece
from modules.Board import Board
from game_rules import move_posible, lm_castle, capture_posible, en_passant, sum_tuples

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
        """rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"""
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

    def move(self, pos:list, piece:Piece):
        if not self.get_piece(pos) == np:
            if self.whites_turn:
                self.black_pieces.pop(self.black_pieces.index(self.get_piece(pos))).kill()
            else:
                self.white_pieces.pop(self.white_pieces.index(self.get_piece(pos))).kill()
        elif lm_castle(piece, pos, self):
            if pos[0] == 6:
                rook = self.get_piece(sum_tuples(pos,(1,0)))
                self.set_piece(sum_tuples(pos,(-1,0)), rook)
            else:
                rook = self.get_piece(sum_tuples(pos,(-2,0)))
                self.set_piece(sum_tuples(pos,(1,0)), rook)
        elif en_passant(piece, pos, self):
            if piece.type == 'P':
                pawn = self.get_piece(sum_tuples(pos,(0,1)))
                self.black_pieces.pop(self.black_pieces.index(pawn)).kill()
                self.del_piece(pawn.pos)
            elif piece.type == 'p':
                pawn = self.get_piece(sum_tuples(pos,(0,-1)))
                self.white_pieces.pop(self.white_pieces.index(pawn)).kill()
                self.del_piece(pawn.pos)
        self.set_piece(pos, piece)
        self.whites_turn = not self.whites_turn
        self.update_legal_moves()
        print(self)
        print(repr(self))

    def update_legal_moves(self):
        for p in self.white_pieces + self.black_pieces:
            p.legal_moves = []
            for i in range (8):
                for j in range(8):
                    if move_posible(p, (i,j), self) or capture_posible(p, (i,j), self):
                        p.legal_moves.append((i,j))

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