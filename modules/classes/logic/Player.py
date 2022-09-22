import numpy as np

from modules.classes.logic.Game import gp

class Player:
    def __init__(self, color, max_pieces=16, name=None, elo=0, title=None, nationality=None):
        self.name = name
        self.elo = elo
        self.title = title
        self.nationality = nationality
        self.color = color
        self.pieces = np.full(max_pieces, gp)
        self.num_pieces = 0
    
    def add_piece(self, p):
        self.pieces[self.num_pieces] = p
        self.num_pieces+=1
    
    def del_piece(self, p, kill=True):
        if kill:
            p.kill()
        self.pieces[np.where(self.pieces == p)] = gp
        self.num_pieces-=1
    
    def get_amount_material(self):
        piece_value = {'p':1,'n':3,'b':3,'r':5,'q':9,'k':0}#the king is the most important piece
        # but should not be consider here
        return sum(np.vectorize(lambda p:piece_value[p.type])(self.pieces))