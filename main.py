import pygame, sys
import numpy as np
pygame.init()

from modules.others.constants import sqr_size, fps, color_turn
screen = pygame.display.set_mode((sqr_size*8,sqr_size*8))

from modules.classes.logic.Piece import Piece, chessfont
from modules.classes.logic.game_modes.StandartMode import StandartMode, gp
# from modules.classes.logic.game_modes.Chess960Mode import Chess960Mode
# from modules.classes.logic.game_modes.HordeMode import HordeMode

pygame.display.set_caption("Chess")
pygame.display.set_icon(pygame.image.load("source/imgs/icon.png"))

default_cursor = pygame.cursors.Cursor(pygame.mouse.get_cursor())
open_hand = pygame.cursors.Cursor((9,9), pygame.image.load("source/imgs/hand.png"))
closed_hand = pygame.cursors.Cursor((7,7), pygame.image.load("source/imgs/closed_hand.png"))

def reset(surface:pygame.Surface):
    game.draw(surface)
    pygame.display.update()

def reset_piece(surface:pygame.Surface, pos:np.ndarray, piece, draw:bool=True):
    game.draw(surface)
    piece.show_legal_moves(game, surface, (int(pos[0]/sqr_size),int(pos[1]/sqr_size)), game.whites_turn)
    if draw:
        piece.draw(surface, (int(pos[0]-sqr_size/2),int(pos[1]-sqr_size/2)))
    else:
        piece.draw(surface, (piece.pos[0]*sqr_size,piece.pos[1]*sqr_size), game.whites_turn)
    pygame.display.update()

def on_movement(move_parameter, pos:np.ndarray, *args, **kwargs):
    game.board.move_arrow.change_arrow(piece_raised.pos,pos,color=color_turn[game.whites_turn])
    if piece_raised.type.isupper():
        game.board.move_arrow.rotate()
    move_parameter(pos, *args, **kwargs)
    if game.check:
        if piece_raised.type.isupper():
            game.board.check_square.update(game.black_pieces[0].pos)
            game.board.check_square.rotate()
        else:
            game.board.check_square.update(game.white_pieces[0].pos)
    game.update(game.whites_turn)

def show_promotion_menu(whites_turn:bool, pos:tuple, surface:pygame.Surface):
    pos = (pos[0]*sqr_size, pos[1]*sqr_size)
    pygame.draw.rect(surface, color_turn[not whites_turn], (pos[0], pos[1], sqr_size, sqr_size*4))
    surface.blit(chessfont.render('w', 1, color_turn[whites_turn]), pos)
    surface.blit(chessfont.render('m', 1, color_turn[whites_turn]), (pos[0], pos[1]+sqr_size))
    surface.blit(chessfont.render('t', 1, color_turn[whites_turn]), (pos[0], pos[1]+2*sqr_size))
    surface.blit(chessfont.render('v', 1, color_turn[whites_turn]), (pos[0], pos[1]+3*sqr_size))
    pygame.display.update()

def set_promotion(anim:bool):
    assert piece_raised.type.lower() == 'p'
    global promoting, promotion_pos
    promoting = True
    if anim:
        piece_raised.animate(screen, clock, game, (I,J), play_sound=False)
    else:
        piece_raised.update(pos=(i,j))
        reset(screen)
    show_promotion_menu(game.whites_turn, (i,j), screen)
    promotion_pos = (i,j)
    piece_raised.legal_moves = []
    if game.whites_turn:
        piece_raised.legal_moves.append((I,0))
        piece_raised.legal_moves.append((I,1))
        piece_raised.legal_moves.append((I,2))
        piece_raised.legal_moves.append((I,3))
    else:
        piece_raised.legal_moves.append((I,7))
        piece_raised.legal_moves.append((I,6))
        piece_raised.legal_moves.append((I,5))
        piece_raised.legal_moves.append((I,4))

def unset_promotion():
    global promoting
    promoting = False
    (a,b) = piece_raised.pos
    piece_raised.pos = promotion_pos
    game.del_piece((a,b)) #the animation has to think that there is no piece to not play the capture sound
    piece_raised.animate(screen, clock, game, (a,b))
    piece_raised.pos = (a,b)
    game.set_piece((a,b), piece_raised)
    game.update_piece_lm(piece_raised)

def play(pos:np.ndarray, piece_raised:Piece, surface=None, clock=None):
    global promoting
    if promoting:
        assert piece_raised.type.lower() == 'p'
        on_movement(game.promote, (I,(7,0)[game.whites_turn]), piece_raised, ('q','n','r','b')[j])
        promoting = False
    else:
        on_movement(game.move, pos, piece_raised, surface=surface, clock=clock)

def change_cursor(cursor):
    try:
        pygame.mouse.set_cursor(cursor)
    except:
        print("could not change cursor")

running = True

clock = pygame.time.Clock()

game = StandartMode()
# game = Chess960Mode()
# game = HordeMode()

reset(screen)
change_cursor(open_hand)

print(game)
print(repr(game))

piece_raised = gp

draw = False
promoting = False
promotion_pos = (0,0)

game.update_legal_moves()
# pygame.time.delay(300) #delay to prevent compile errors

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
            if (I,J) in map(tuple, piece_raised.legal_moves):
                if piece_raised.type.lower() == 'p' and j==0 and not promoting:
                    set_promotion(True)
                else:
                    play((I,J), piece_raised, surface=screen, clock=clock)
            else:
                reset(screen)
                if promoting:
                    unset_promotion()
                    piece_raised = gp
                elif not game.get_piece((I,J)) == gp:
                    piece_raised = game.get_piece((I,J))
                    reset_piece(screen, (x,y), piece_raised)
                    draw = True
                else:
                    piece_raised = gp
            pygame.mouse.set_cursor(closed_hand)
        elif event.type == pygame.MOUSEBUTTONUP:
            draw = False
            if (I,J) == tuple(piece_raised.pos):
                reset_piece(screen, (x,y), piece_raised, draw=False)
            else:
                if not piece_raised == gp and not promoting:
                    if (I,J) in map(tuple, piece_raised.legal_moves):
                        if piece_raised.type.lower() == 'p' and j==0 and not promoting:
                            set_promotion(False)
                        else:
                            play((I,J), piece_raised)
                            piece_raised = gp
                            reset(screen)
                    else:
                        piece_raised = gp
                        reset(screen)
            change_cursor(open_hand)
        elif event.type == pygame.MOUSEMOTION:
            if not piece_raised == gp and not promoting:
                reset_piece(screen, (x,y), piece_raised, draw=draw)
                if not draw:
                    if (I,J) in map(tuple, piece_raised.legal_moves):
                        change_cursor(default_cursor)
                    else:
                        change_cursor(open_hand)
    clock.tick(fps)