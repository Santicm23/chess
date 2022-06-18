import pygame

from modules.others.constants import sqr_size, WHITE, BLACK

chessfont = pygame.font.Font("source/fonts/CASEFONT.TTF", sqr_size)
rsq = pygame.image.load("source/imgs/raised_square.png").convert_alpha() #pos where the piece was raised
ms_mp = pygame.image.load("source/imgs/ms_mp.png").convert_alpha() #mouse on move posible
mp = pygame.image.load("source/imgs/mp.png").convert_alpha() #move posible
cp = pygame.image.load("source/imgs/cp.png").convert_alpha() #capture posible

def get_color(type:str):
    if type.isupper():
        return WHITE
    else:
        return BLACK

class Piece(pygame.sprite.Sprite):
    def __init__(self, type:str=' ', pos:list=[0,0]):
        super().__init__()
        assert type in ['P','p','N','n','B','b','R','r','Q','q','K','k',' ']
        assert 0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8 and len(pos) == 2
        self.type = type
        self.pos = pos
        self.color = get_color(self.type)
        self.set_image()
        self.legal_moves = []
    
    def __str__(self):
        return self.type

    def set_image(self):
        self.image = chessfont.render(
            {'p': 'o', 'n': 'm', 'b': 'v', 'r': 't', 'q': 'w', 'k': 'l', ' ': None}[self.type.lower()], 1, self.color)
        self.rect = self.image.get_rect(topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size))
    
    def draw(self, surface:pygame.Surface, pos:tuple, pov:bool=True):
        if pov:
            surface.blit(self.image, pos)
        else:
            surface.blit(self.image, (7*sqr_size-pos[0],7*sqr_size-pos[1]))

    def update(self, pov:bool=True):
        if pov:
            self.rect.topleft = ((self.pos[0])*sqr_size,(self.pos[1])*sqr_size)
        else:
            self.rect.topleft = ((7-self.pos[0])*sqr_size,(7-self.pos[1])*sqr_size)
    
    def show_legal_moves(self, game, surface:pygame.Surface, pos:tuple, pov:bool=True):
        if pov:
            surface.blit(rsq,(self.pos[0]*sqr_size,self.pos[1]*sqr_size))
        else:
            surface.blit(rsq,((7-self.pos[0])*sqr_size,(7-self.pos[1])*sqr_size))
        for m in self.legal_moves:
            if pov:
                M = m
            else:
                M = (7-m[0],7-m[1])
            if M == pos:
                surface.blit(ms_mp,(M[0]*sqr_size,M[1]*sqr_size))
            elif game.get_piece(m).type == ' ':
                surface.blit(mp,(M[0]*sqr_size+30,M[1]*sqr_size+30))
            else:
                surface.blit(cp,(M[0]*sqr_size,M[1]*sqr_size))