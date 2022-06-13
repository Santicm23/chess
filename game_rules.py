valid_pos = lambda pos: 0<=pos[0] and pos[0]<8 and 0<=pos[1] and pos[1]<8

sum_tuples = lambda p1, p2: (p1[0]+p2[0],p1[1]+p2[1])

def lm_pawn(piece, new_pos, game):
    if game.whites_turn:
        if new_pos == sum_tuples(piece.pos, (0,-1)):
            return True
        if piece.pos[1] == 6 and new_pos == (piece.pos[0],4) and game.get_piece((piece.pos[0],5)).type == ' ':
            return True
    else:
        if new_pos == sum_tuples(piece.pos, (0,1)):
            return True
        if piece.pos[1] == 1 and new_pos == (piece.pos[0],3) and game.get_piece((piece.pos[0],2)).type == ' ':
            return True
    return False
def lmc_knight(piece, new_pos):
    for k in range (2):
        for k1 in range (2):
            for k2 in range (2):
                if k == 0:
                    (a,b)=(1,2)
                else:
                    (a,b)=(2,1)
                if k1 == 0:
                    a=a*-1
                    b=b*-1
                if k2 == 0:
                    a=a*-1
                if new_pos == sum_tuples(piece.pos, (a,b)):
                    return True
    return False
def lmc_bishop(piece, new_pos, game):
    for c in range (-1,2,2):
        for d in range (-1,2,2):
            q=1
            while valid_pos(sum_tuples(piece.pos, (q*c,q*d))):
                if new_pos == sum_tuples(piece.pos, (q*c,q*d)):
                    return True
                if not game.get_piece(sum_tuples(piece.pos, (q*c,q*d))).type == ' ':
                    break
                q+=1
    return False
def lmc_rook(piece, new_pos, game):
    for i in range (4):
        if i == 0:
            (a,b)=(1,0)
        elif i == 1:
            (a,b)=(-1,0)
        elif i == 2:
            (a,b)=(0,1)
        else:
            (a,b)=(0,-1)
        q=1
        while valid_pos(sum_tuples(piece.pos, (q*a,q*b))):
            if new_pos == sum_tuples(piece.pos, (q*a,q*b)):
                return True
            if not game.get_piece(sum_tuples(piece.pos, (q*a,q*b))).type == ' ':
                break
            q+=1
    return False
def lmc_queen(piece, new_pos, game):
    for c in range (-1,2):
        for d in range (-1,2):
            q=1
            while valid_pos(sum_tuples(piece.pos, (q*c,q*d))):
                if new_pos == sum_tuples(piece.pos, (q*c,q*d)):
                    return True
                if not game.get_piece(sum_tuples(piece.pos, (q*c,q*d))).type == ' ':
                    break
                q+=1
    return False
def lmc_king(piece, new_pos):
    for c in range (-1,2):
        for d in range (-1,2):
            if new_pos == sum_tuples(piece.pos, (c,d)):
                return True
    return False
def lm_castle(piece, new_pos, game):
    if not game.check:
        if new_pos == sum_tuples(piece.pos, (2,0)):
            if game.right_castle['K']:
                if move_posible(game.get_piece((7,7)), (5,7), game):
                    return True
            if game.right_castle['k']:
                if move_posible(game.get_piece((7,0)), (5,0), game):
                    return True
        elif new_pos == sum_tuples(piece.pos, (-2,0)):
            if game.right_castle['Q']:
                if move_posible(game.get_piece((0,7)), (3,7), game):
                    return True
            if game.right_castle['q']:
                if move_posible(game.get_piece((0,0)), (3,0), game):
                    return True
    return False
def move_posible(piece, new_pos, game):
    if piece.type.isupper() == game.whites_turn and game.get_piece(new_pos).type == ' ':
        if piece.type.lower() == 'p':
            return lm_pawn(piece, new_pos, game)
        elif piece.type.lower() == 'n':
            return lmc_knight(piece, new_pos)
        elif piece.type.lower() == 'b':
            return lmc_bishop(piece, new_pos, game)
        elif piece.type.lower() == 'r':
            return lmc_rook(piece, new_pos, game)
        elif piece.type.lower() == 'q':
            return lmc_queen(piece, new_pos, game)
        elif piece.type.lower() == 'k':
            return lmc_king(piece, new_pos) or lm_castle(piece, new_pos, game)
    return False

def lc_pawn(piece, new_pos, game):
    if new_pos[0] == piece.pos[0]-1 or new_pos[0] == piece.pos[0]+1:
        if game.whites_turn and new_pos[1] == piece.pos[1]-1:
            return True
        if not game.whites_turn and new_pos[1] == piece.pos[1]+1:
            return True
    return False
def en_passant(piece, new_pos, game):
    if lc_pawn(piece, new_pos, game) and new_pos == game.en_passant:
        return True
    return False
def capture_posible(piece, new_pos, game):
    if piece.type.isupper() == game.whites_turn:
        if game.get_piece(new_pos).type == ' ':
            if piece.type.lower() == 'p':
                return en_passant(piece, new_pos, game)
        elif not game.get_piece(new_pos).type.isupper() == game.whites_turn:
            if piece.type.lower() == 'p':
                return lc_pawn(piece, new_pos, game)
            elif piece.type.lower() == 'n':
                return lmc_knight(piece, new_pos)
            elif piece.type.lower() == 'b':
                return lmc_bishop(piece, new_pos, game)
            elif piece.type.lower() == 'r':
                return lmc_rook(piece, new_pos, game)
            elif piece.type.lower() == 'q':
                return lmc_queen(piece, new_pos, game)
            elif piece.type.lower() == 'k':
                return lmc_king(piece, new_pos)
    return False