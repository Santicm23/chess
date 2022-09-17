import pygame
import numpy as np

from modules.others.constants import sqr_size

class Arrow(pygame.sprite.Sprite):
    def __init__(self, color:tuple, bottom:np.array=np.array([0,0]), top:np.array=np.array([0,0])):
        super().__init__()
        self.image = pygame.image.load("source/imgs/bg_arrow.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.change_arrow(bottom, top, color=color, show=False)

    def change_arrow(self, bottom:np.array, top:np.array, color:tuple=None, show=True):
        if not color == None:
            self.color = color
        self.bottom = np.array(bottom)
        self.top = np.array(top)
        self.image = pygame.image.load("source/imgs/bg_arrow.png").convert_alpha()
        self.show(show)
        self.update()
    
    def change_color(self, color):
        self.color = color

    def rotate(self):
        self.change_arrow(7-self.bottom,7-self.top)

    def show(self, b:bool):
        if b:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)

    def update(self):
        if (self.bottom == self.top).all(): return None
        (ax,ay) = ((self.bottom[0]+0.5)*sqr_size,(self.bottom[1]+0.5)*sqr_size)
        (bx,by) = ((self.top[0]+0.5)*sqr_size,(self.top[1]+0.5)*sqr_size)
        vec = (ax-bx,ay-by)
        invec = (-vec[1], vec[0])
        norm = ((vec[0])**2+(vec[1])**2)**0.5
        scal1 = (vec[0]/norm, vec[1]/norm)
        scal2 = (invec[0]/norm, invec[1]/norm)
        c1 = 38
        c2 = 42
        c3 = 3
        p1 = (ax,ay)
        p2 = (bx+c1*scal1[0],by+c1*scal1[1])
        p3 = (bx+c2*scal1[0]-c3*scal2[0],by+c2*scal1[1]-c3*scal2[1])
        p4 = (bx+c2*scal1[0]+c3*scal2[0],by+c2*scal1[1]+c3*scal2[1])
        pygame.draw.aaline(self.image, self.color, p1, p2, 1)
        pygame.draw.aaline(self.image, self.color, p2, p3, 1)
        pygame.draw.aaline(self.image, self.color, p2, p4, 1)