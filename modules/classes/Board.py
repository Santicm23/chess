import pygame

from modules.others.constants import sqr_size, WHITE, GREY, LGREY

lines = ['8','7','6','5','4','3','2','1'] #lines (in reverse for the impresion)
files = ['a','b','c','d','e','f','g','h'] #files

font = pygame.font.SysFont("Gerbera", int(1/5*sqr_size))

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((sqr_size*8,sqr_size*8))
        self.rect = self.image.get_rect()
        self.update(True)
    
    def update(self, pov:bool):
        pygame.draw.rect(self.image, GREY, (0, 0, sqr_size*8, sqr_size*8))
        for i in range (8):
            for j in range (i%2, 8, 2):
                pygame.draw.rect(self.image, LGREY, (i*sqr_size, j*sqr_size, sqr_size, sqr_size))
        for l in range (8):
            nbr=font.render(lines[l],1,WHITE)
            L=l
            if not pov:
                L=7-l
            self.image.blit(nbr,(1/40*sqr_size, (1/40+L)*sqr_size))
        for c in range (8):
            ltr=font.render(files[c],1,WHITE)
            C=c
            if not pov:
                C=7-c
            self.image.blit(ltr,((71/80+C)*sqr_size, (67/80+7)*sqr_size))