# --- constants --- #

sqr_size = 80 #square size
fps = 60 #frames per second
delay = 0.2 #sound delay in seconds
frames = int(fps*delay)

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (125,125,125)
LGREY = (155,155,155)
color_turn = (BLACK, WHITE)

# --- lambda fonctions --- #

valid_pos = lambda pos: 0<=pos[0] and pos[0]<8 and 0<=pos[1] and pos[1]<8
sum_tuples = lambda p1, p2: (p1[0]+p2[0],p1[1]+p2[1])
scal_tuple = lambda p, k: (p[0]*k,p[1]*k)
invert_Ituple = lambda p: (7-p[0],7-p[1])
invert_Ntuple = lambda p: (7*sqr_size-p[0],7*sqr_size-p[1])