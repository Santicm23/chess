import pygame, sys
pygame.init()

from constants import sqr_size
from modules import Game

screen = pygame.display.set_mode((sqr_size*8,sqr_size*8))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("imgs/icon.png"))

running = True

clock = pygame.time.Clock()

game = Game.Game(screen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

print(game)
print(repr(game))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    clock.tick(60)