import pygame
import numpy as np

from modules.others.constants import sqr_size, frames, fps, color_turn

chessfont = pygame.font.Font("source/fonts/CASEFONT.TTF", sqr_size)
rsq = pygame.image.load("source/imgs/raised_square.png").convert_alpha() #pos where the piece was raised
ms_mp = pygame.image.load("source/imgs/ms_mp.png").convert_alpha() #mouse on move posible
mp = pygame.image.load("source/imgs/mp.png").convert_alpha() #move posible
cp = pygame.image.load("source/imgs/cp.png").convert_alpha() #capture posible

move_sound = pygame.mixer.Sound("source/sounds/piece_dropped.mp3")
capture_sound = pygame.mixer.Sound("source/sounds/piece_capturing.mp3")

class Piece(pygame.sprite.Sprite):
    def __init__(self, type:str=' ', pos:np.ndarray=np.array([0,0])):
        super().__init__()
        assert type in ['P','p','N','n','B','b','R','r','Q','q','K','k',' ']
        assert 0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8 and len(pos) == 2
        self.type = type
        self.pos = np.array(pos)
        self.color = color_turn[self.type.isupper()]
        self.set_image()
        self.legal_moves = []
    
    def __str__(self):
        return self.type

    def set_image(self):
        self.image = chessfont.render(
            {'p': 'o', 'n': 'm', 'b': 'v', 'r': 't', 'q': 'w', 'k': 'l', ' ': None}[self.type.lower()], 1, self.color)
        self.rect = self.image.get_rect(topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size))
    
    def draw(self, surface:pygame.Surface, pos:np.ndarray, pov:bool=True):
        if pov:
            surface.blit(self.image, pos)
        else:
            surface.blit(self.image, np.array([7,7])*sqr_size-(pos))

    def update(self, pov:bool=True, pos=None):
        if pos == None:
            pos = self.pos.copy()
        if pov:
            self.rect.topleft = (pos[0]*sqr_size,pos[1]*sqr_size)
        else:
            self.rect.topleft = ((7-pos[0])*sqr_size,(7-pos[1])*sqr_size)
    
    def animate(self, surface:pygame.Surface, clock, game, new_pos:np.ndarray, en_passant=False, play_sound=True):
        px,py = self.pos
        # frame distance for x and y direction
        fdx = (new_pos[0] - self.pos[0])/frames
        fdy = (new_pos[1] - self.pos[1])/frames
        for i in range (frames):
            px += fdx
            py += fdy
            self.kill()
            game.draw(surface)
            self.draw(surface, np.array([px,py])*sqr_size, game.whites_turn)
            pygame.display.update()
            if i == int(frames*2/3) and play_sound:
                move_sound.play()
                if not game.get_piece(new_pos).type == ' ' or en_passant:
                    capture_sound.play()
            clock.tick(fps)
        game.group.add(self)

    def animate_castle(self, surface:pygame.Surface, clock, game, new_pos:np.ndarray, rook, np_rook:np.ndarray):
        px,py = self.pos
        # frame distance for x and y direction
        fdx = (new_pos[0] - self.pos[0])/frames
        fdy = (new_pos[1] - self.pos[1])/frames
        rx,ry = rook.pos
        fdx_rook = (np_rook[0] - rook.pos[0])/frames
        fdy_rook = (np_rook[1] - rook.pos[1])/frames
        for i in range (frames):
            px += fdx
            py += fdy
            rx += fdx_rook
            ry += fdy_rook
            self.kill()
            rook.kill()
            game.draw(surface)
            self.draw(surface, np.array([px,py])*sqr_size, game.whites_turn)
            rook.draw(surface, np.array([rx,ry])*sqr_size, game.whites_turn)
            pygame.display.update()
            if i == int(frames*2/3):
                move_sound.play()
            clock.tick(fps)
        move_sound.play()
        game.group.add(self)
        game.group.add(rook)

    def show_legal_moves(self, game, surface:pygame.Surface, pos:np.ndarray, pov:bool=True):
        if pov:
            surface.blit(rsq, self.pos*sqr_size)
        else:
            surface.blit(rsq, ((7,7)-(self.pos))*sqr_size)
        for m in self.legal_moves:
            if pov:
                M = m.copy()
            else:
                M = (7,7)-m
            if (M == pos).all():
                surface.blit(ms_mp, M*sqr_size)
            elif game.get_piece(m).type == ' ':
                surface.blit(mp, M*sqr_size+(30,30))
            else:
                surface.blit(cp, M*sqr_size)