import pygame

from constants import sqr_size

WHITE = (225,225,225)
GREY = (125,125,125)
LGREY = (155,155,155)

lines = ['8','7','6','5','4','3','2','1'] #filas (al revez para la impresión)
files = ['a','b','c','d','e','f','g','h'] #columnas

font = pygame.font.SysFont("Gerbera", int(1/5*sqr_size))

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((sqr_size*8,sqr_size*8))
        self.rect = self.image.get_rect()
        self.update(True)
    
    def update(self, whites_pov:bool):
        pygame.draw.rect(self.image, GREY, (0, 0, sqr_size*8, sqr_size*8))
        for i in range (8):
            for j in range (i%2, 8, 2):
                pygame.draw.rect(self.image, LGREY, (i*sqr_size, j*sqr_size, sqr_size, sqr_size))
        for l in range (8):
            nbr=font.render(lines[l],1,WHITE)
            L=l
            if not whites_pov:
                L=7-l
            self.image.blit(nbr,(1/40*sqr_size, (1/40+L)*sqr_size))
        for c in range (8):
            ltr=font.render(files[c],1,WHITE)
            C=c
            if not whites_pov:
                C=7-c
            self.image.blit(ltr,((71/80+C)*sqr_size, (67/80+7)*sqr_size))