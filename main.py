import pygame, sys
pygame.init()

import Board

screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("imgs/icon.png"))

running = True

clock = pygame.time.Clock()

board = Board.Board()
board_group = pygame.sprite.GroupSingle() #grupo del tablero
board_group.add(board) #añadir el tablero
board_group.draw(screen)
pygame.display.update()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    clock.tick(60)