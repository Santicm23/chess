import pygame

from modules.others.constants import sqr_size

class Square(pygame.sprite.Sprite):
    def __init__(self, color:tuple=(205,92,92), pos:list=[0,0]):
        super().__init__()
        self.color = color
        self.pos = pos
        self.image = pygame.Surface((sqr_size,sqr_size))
        pygame.draw.rect(self.image, self.color, (0,0,sqr_size,sqr_size))
        self.show(False)
        self.rect = self.image.get_rect(topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size))

    def update(self, new_pos:tuple, pov:bool=True):
        if pov:
            self.pos = new_pos
        else:
            self.pos = [7-new_pos[0], 7-new_pos[1]]
        self.rect.topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size)
        self.show(True)
    
    def rotate(self):
        self.pos = [7-self.pos[0], 7-self.pos[1]]
        self.rect.topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size)

    def change_color(self, color):
        self.color = color

    def show(self, b:bool):
        if b:
            self.image.set_alpha(175)
        else:
            self.image.set_alpha(0)