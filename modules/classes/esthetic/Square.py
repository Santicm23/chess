import pygame
import numpy as np

from modules.others.constants import sqr_size

class Square(pygame.sprite.Sprite):
    def __init__(self, color:tuple=(205,92,92), pos:np.array=np.array([0,0])):
        super().__init__()
        self.color = color
        self.pos = pos
        self.image = pygame.Surface((sqr_size,sqr_size))
        pygame.draw.rect(self.image, self.color, (0,0,sqr_size,sqr_size))
        self.show(False)
        self.rect = self.image.get_rect(topleft = (self.pos[0]*sqr_size,self.pos[1]*sqr_size))

    def update(self, new_pos:np.array, pov:bool=True):
        if pov:
            self.pos = np.array(new_pos)
        else:
            self.pos = 7-np.array(new_pos)
        self.rect.topleft = self.pos*sqr_size
        self.show(True)
    
    def rotate(self):
        self.pos = 7-self.pos
        self.rect.topleft = self.pos*sqr_size

    def change_color(self, color):
        self.color = color

    def show(self, b:bool):
        if b:
            self.image.set_alpha(175)
        else:
            self.image.set_alpha(0)