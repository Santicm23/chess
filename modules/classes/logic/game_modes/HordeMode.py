from modules.classes.logic.Game import Game
from modules.classes.logic.game_modes.StandartMode import StandartMode
from modules.others.game_rules import capture_posible

class HordeMode(StandartMode):
    def __init__(self, fen_code:str="rnbqkbnr/pppppppp/8/1PP2PP1/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP w kq - 0 1"):
        super().__init__(fen_code)
    
    def __str__(self):
        return "\n            Horde chess:" + Game.__str__(self)

    def update_check(self):
        check = False
        self.whites_turn = not self.whites_turn
        if self.whites_turn:
            for p in self.white_pieces:
                if capture_posible(p, self.black_pieces[0].pos, self) and self.black_pieces[0].type == 'k':
                    check = True
                    break
        self.whites_turn = not self.whites_turn
        return check