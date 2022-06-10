import pygame, sys
pygame.init()

from constants import sqr_size
from modules.Game import Game, np

screen = pygame.display.set_mode((sqr_size*8,sqr_size*8))
pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("imgs/icon.png"))

running = True

clock = pygame.time.Clock()

game = Game(screen, "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
pygame.display.update()

print(game)
print(repr(game))

piece_raised = np

while running:
    (x,y) = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            piece_raised = game.get_piece((int(x/sqr_size),int(y/sqr_size)))
            game.draw(screen)
            piece_raised.draw(screen,(x-int(sqr_size/2),y-int(sqr_size/2)))
            pygame.display.update()
        elif event.type == pygame.MOUSEBUTTONUP and not piece_raised == np:
            if not game.get_piece((int(x/sqr_size),int(y/sqr_size))) == np and not game.get_piece((int(x/sqr_size),int(y/sqr_size))) == piece_raised:
                game.get_piece((int(x/sqr_size),int(y/sqr_size))).kill()
            game.set_piece(piece_raised.pos, np)
            piece_raised.pos = [int(x/sqr_size),int(y/sqr_size)]
            piece_raised.update(game.whites_turn)
            game.set_piece(piece_raised.pos, piece_raised)
            piece_raised = np
            game.draw(screen)
            pygame.display.update()
        elif event.type == pygame.MOUSEMOTION and not piece_raised == np:
            game.draw(screen)
            piece_raised.draw(screen,(x-int(sqr_size/2),y-int(sqr_size/2)))
            pygame.display.update()
    clock.tick(60)