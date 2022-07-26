from abc import abstractmethod
import pygame

class Figure(pygame.sprite.Sprite):
    def __init__(self, color:tuple):
        self.color = color

    def change_color(self, color):
        self.color = color
    
    @abstractmethod
    def show(): pass

    @abstractmethod
    def update(): pass