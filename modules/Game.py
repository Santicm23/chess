import pygame

from constants import sqr_size
from modules import Board, Piece

np = Piece.Piece() #null piece

class Game:
    def __init__(self, surface:pygame.Surface, fen_code:str):
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
        self.right_castle = {'K': False, 'Q': False, 'k': False, 'q': False}
        self.last_cpm = 0 #last capture or pawn move
        self.number_moves = 0
        fen(self, fen_code)
        self.board = Board.Board()
        self.board_group = pygame.sprite.GroupSingle()
        self.board_group.add(self.board)
        self.piece_group = pygame.sprite.Group()
        for p in self.white_pieces + self.black_pieces:
            self.piece_group.add(p)
        self.update(surface, self.whites_turn)
    
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
        self.board_group.draw(surface)
        self.piece_group.draw(surface)
        pygame.display.update()

    def update(self, surface:pygame.Surface, whites_pov:bool):
        self.board.update(whites_pov)
        for p in self.white_pieces + self.black_pieces:
            p.update((p.pos[0]*sqr_size, p.pos[1]*sqr_size), whites_pov)
        self.draw(surface)

def fen(game:Game, fen_code:str):# rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 #
    fen_code = fen_code.split()
    fen_pos = fen_code[0].replace('/',' ').split()
    for i in range(len(fen_pos)):
        k = 0
        for j in fen_pos[i]:
            if j.isalpha():
                p = Piece.Piece(j, (k,i))
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