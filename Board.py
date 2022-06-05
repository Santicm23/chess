import pygame

WHITE = (225,225,225)
GREY = (125,125,125)
LGREY = (155,155,155)

lines = ['8','7','6','5','4','3','2','1'] #filas (al revez para la impresión)
files = ['a','b','c','d','e','f','g','h'] #columnas

font = pygame.font.SysFont("Gerbera", 16)

class Board(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((640,640))
        self.rect = self.image.get_rect()
        self.update(0)
    
    def update(self, pov):
        pygame.draw.rect(self.image, LGREY, (0, 0, 640, 640))
        for i in range (8):
            for j in range ((i-1)%2, 8, 2):
                pygame.draw.rect(self.image, GREY, (i*80, j*80, 80, 80))
        for l in range (8):
            nbr=font.render(lines[l],1,WHITE)
            l1=l
            if pov==1:
                l1=7-l
            self.image.blit(nbr,(2, l1*80+2))
        for c in range (8):
            ltr=font.render(files[c],1,WHITE)
            c1=c
            if pov==1:
                c1=7-c
            self.image.blit(ltr,(71+c1*80, 67+7*80))