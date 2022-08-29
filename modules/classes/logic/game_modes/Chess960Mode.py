import random

from modules.classes.logic.Game import Game
from modules.classes.logic.game_modes.StandartMode import StandartMode

class Chess960Mode(StandartMode):
    def __init__(self):
        super().__init__(random_fen_generator())
    
    def __str__(self):
        return "\n          Variant chess960:" + Game.__str__(self)

def random_fen_generator() -> str:
    fen = ""
    remain_pieces = ['r','n','b','q','b','n','r']
    last_piece = ''
    while not last_piece == 'r':
        last_piece = remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
        fen += last_piece
    del remain_pieces[remain_pieces.index('r')]
    remain_pieces.append('k')
    while not last_piece == 'k':
        last_piece = remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
        fen += last_piece
    remain_pieces.append('r')
    while not len(remain_pieces) == 0:
        fen += remain_pieces.pop(random.randint(0, len(remain_pieces)-1))
    return fen + "/pppppppp/8/8/8/8/PPPPPPPP/" + fen.upper() + " w KQkq - 0 1"