import pygame

from constants import sqr_size

WHITE = (255,255,255)
BLACK = (0,0,0)
chessfont = pygame.font.Font("fonts/CASEFONT.TTF", sqr_size)

def get_color(type:str):
    if type.isupper():
        return WHITE
    else:
        return BLACK

class Piece(pygame.sprite.Sprite):
    def __init__(self, type:str=' ', pos:tuple=(0,0)):
        super().__init__()
        assert type in ['P','p','N','n','B','b','R','r','Q','q','K','k',' ']
        assert 0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8 and len(pos) == 2
        self.type = type
        self.pos = pos
        self.start_pos = pos
        self.color = get_color(self.type)
        self.set_image()
        self.legal_moves = []
    
    def __str__(self):
        return self.type

    def set_image(self):
        self.image = chessfont.render(
            {'p': 'o', 'n': 'm', 'b': 'v', 'r': 't', 'q': 'w', 'k': 'l', ' ': ' '}[self.type.lower()], 1, self.color)
        self.rect = self.image.get_rect(topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size))
    
    def update(self, pos:tuple, whites_pov:bool):
        if whites_pov:
            self.rect = self.image.get_rect(topleft = (pos[0],pos[1]))
        else:
            self.rect = self.image.get_rect(topleft = (sqr_size*7-pos[0],sqr_size*7-pos[1]))