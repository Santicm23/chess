import pygame, sys
pygame.init()

from modules.others.constants import sqr_size
screen = pygame.display.set_mode((sqr_size*8,sqr_size*8))

from modules.classes.Game import Game, Piece, np

pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("source/imgs/icon.png"))

default_cursor = pygame.cursors.Cursor(pygame.mouse.get_cursor())
hand = pygame.cursors.Cursor((9, 9), pygame.image.load("source/imgs/hand.png"))
closed_hand = pygame.cursors.Cursor((7, 7), pygame.image.load("source/imgs/closed_hand.png"))

def reset(surface:pygame.Surface):
    game.draw(surface)
    pygame.display.update()

def reset_piece(surface:pygame.Surface, pos:tuple, piece:Piece, draw:bool=True):
    game.draw(surface)
    piece.show_legal_moves(game, surface, (int(pos[0]/sqr_size),int(pos[1]/sqr_size)), game.whites_turn)
    if draw:
        piece.draw(surface, (int(pos[0]-sqr_size/2),int(pos[1]-sqr_size/2)))
    else:
        piece.draw(surface, (piece.pos[0]*sqr_size,piece.pos[1]*sqr_size), game.whites_turn)
    pygame.display.update()

running = True

clock = pygame.time.Clock()

game = Game("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
reset(screen)
pygame.mouse.set_cursor(hand)

print(game)
print(repr(game))

piece_raised = np
draw = False
game.update_legal_moves()

while running:
    (x,y) = pygame.mouse.get_pos() #coordinates
    (i,j) = (int(x/sqr_size),int(y/sqr_size)) #indices
    if game.whites_turn:
        (I,J) = (i,j)
    else:
        (I,J) = (7-i,7-j)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not piece_raised == np:
                if (I,J) in piece_raised.legal_moves:
                    game.move((I,J), piece_raised)
                piece_raised = np
                game.update(game.whites_turn)
                reset(screen)
                break
            pygame.mouse.set_cursor(closed_hand)
            if not game.get_piece((I,J)) == np:
                piece_raised = game.get_piece((I,J))
                reset_piece(screen, (x,y), piece_raised)
                draw = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.mouse.set_cursor(hand)
            draw = False
            if (I,J) == piece_raised.pos:
                reset_piece(screen, (x,y), piece_raised, draw)
                pygame.mouse.set_cursor(default_cursor)
            else:
                if not piece_raised == np:
                    if (I,J) in piece_raised.legal_moves:
                        game.move((I,J), piece_raised)
                    piece_raised = np
                    game.update(game.whites_turn)
                    reset(screen)
        elif event.type == pygame.MOUSEMOTION and not piece_raised == np:
            reset_piece(screen, (x,y), piece_raised, draw)
    clock.tick(60)