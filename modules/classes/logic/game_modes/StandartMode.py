import pygame
import numpy as np

from modules.classes.logic.Game import Game, gp
from modules.classes.logic.Piece import Piece, move_sound, capture_sound
from modules.others.constants import delay
from modules.others.game_rules import lm_castle, en_passant

class StandartMode(Game):
    def __init__(self, fen_code:str="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        super().__init__(fen_code)
    
    def __str__(self):
        return "\n            Classic chess:" + super().__str__()

    def move(self, pos:np.ndarray, piece:Piece, surface:pygame.Surface=None, clock=None):
        pos = np.array(pos)
        if self.get_piece(pos) == gp:
            if piece.type.lower() == 'p':
                self.last_cpm = 0
                if en_passant(piece, pos, self):
                    if piece.type == 'P':
                        pawn = self.get_piece(pos+(0,1))
                        self.black_pieces.pop(self.black_pieces.index(pawn)).kill()
                    elif piece.type == 'p':
                        pawn = self.get_piece(pos-(0,1))
                        self.white_pieces.pop(self.white_pieces.index(pawn)).kill()
                    self.del_piece(pawn.pos)
                    if not surface == None:
                        piece.animate(surface, clock, self, pos, True)
                    else:
                        move_sound.play()
                        capture_sound.play()
                elif not surface == None:
                    piece.animate(surface, clock, self, pos)
                else:
                    move_sound.play()
            else:
                self.last_cpm += 1
                if lm_castle(piece, pos, self):
                    if pos[0] == 6:
                        rook = self.get_piece(pos+(1,0))
                        if not surface == None:
                            piece.animate_castle(surface, clock, self, pos, rook, pos-(1,0))
                        else:
                            move_sound.play()
                            pygame.time.delay(int(delay*400))
                            move_sound.play()
                        self.set_piece(pos-(1,0), rook)
                    else:
                        rook = self.get_piece(pos-(2,0))
                        if not surface == None:
                            piece.animate_castle(surface, clock, self, pos, rook, pos+(1,0))
                        else:
                            move_sound.play()
                            pygame.time.delay(int(delay*400))
                            move_sound.play()
                        self.set_piece(pos+(1,0), rook)
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
        print(self)
        print(repr(self))

    def promote(self, pos, piece:Piece, new_type:str):
        assert piece.type.lower() == 'p'
        piece.type = new_type
        if self.whites_turn:
            piece.type = piece.type.upper()
        piece.set_image()
        move_sound.play()
        if not self.get_piece(pos) == gp:
            if self.whites_turn:
                self.black_pieces.pop(self.black_pieces.index(self.get_piece(pos))).kill()
            else:
                self.white_pieces.pop(self.white_pieces.index(self.get_piece(pos))).kill()
            capture_sound.play()
        self.update_right_castle(piece)
        self.update_en_passant(pos, piece)
        self.set_piece(pos, piece)
        self.whites_turn = not self.whites_turn
        self.update_legal_moves()
        if self.whites_turn: self.number_moves += 1
        self.check = self.update_check()
        print(self)
        print(repr(self))