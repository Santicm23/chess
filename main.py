import pygame, sys
pygame.init()

from constants import sqr_size
screen = pygame.display.set_mode((sqr_size*8,sqr_size*8))

from modules.Game import Game, Piece, np

pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("imgs/icon.png"))

def reset(surface:pygame.Surface, piece:Piece=np, pos:tuple=(0,0)):
    game.draw(surface)
    piece.show_legal_moves(game, surface)
    piece.draw(surface, (int(pos[0]-sqr_size/2),int(pos[1]-sqr_size/2)))
    pygame.display.update()

running = True

clock = pygame.time.Clock()

game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
reset(screen)

print(game)
print(repr(game))

piece_raised = np
game.update_legal_moves()

while running:
    (x,y) = pygame.mouse.get_pos() #coordinates
    (i,j) = (int(x/sqr_size),int(y/sqr_size)) #indices
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            piece_raised = game.get_piece((i,j))
            reset(screen, piece_raised, (x,y))
        elif event.type == pygame.MOUSEBUTTONUP and not piece_raised == np:
            if (i,j) in piece_raised.legal_moves:
                game.move((i,j), piece_raised)
            piece_raised = np
            reset(screen)
        elif event.type == pygame.MOUSEMOTION and not piece_raised == np:
            reset(screen, piece_raised, (x,y))
    clock.tick(60)