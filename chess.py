import pygame, sys, time
from collections import defaultdict
from copy import deepcopy

pygame.init()

# ---------------- CONFIG ----------------
SIZE = 640
SQ = SIZE // 8
FONT = pygame.font.SysFont("arial", 36)
SMALL = pygame.font.SysFont("arial", 20)
CLOCK_FONT = pygame.font.SysFont("arial", 24)

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (186, 202, 68)
WHITE, BLACK = "w", "b"

UNICODE = {
    "wP":"♙","wR":"♖","wN":"♘","wB":"♗","wQ":"♕","wK":"♔",
    "bP":"♟","bR":"♜","bN":"♞","bB":"♝","bQ":"♛","bK":"♚",
}

screen = pygame.display.set_mode((SIZE, SIZE+60))
pygame.display.set_caption("Chess")

# ---------------- ENGINE STATE ----------------
def start_board():
    return [
        ["bR","bN","bB","bQ","bK","bB","bN","bR"],
        ["bP"]*8,
        [""]*8,
        [""]*8,
        [""]*8,
        [""]*8,
        ["wP"]*8,
        ["wR","wN","wB","wQ","wK","wB","wN","wR"],
    ]

board = start_board()
turn = WHITE
selected = None
legal_moves = []
move_log = []
halfmove_clock = 0
position_count = defaultdict(int)
en_passant = None
promotion_pending = None

# clocks
white_time = 5 * 60
black_time = 5 * 60
last_tick = time.time()

# ---------------- HELPERS ----------------
def inside(r,c): return 0 <= r < 8 and 0 <= c < 8
def enemy(p): return p and p[0] != turn
def clone(): return deepcopy(board)

# ---------------- MOVE GENERATION ----------------
def ray(r,c,dirs):
    moves=[]
    for dr,dc in dirs:
        nr,nc=r+dr,c+dc
        while inside(nr,nc):
            if board[nr][nc]=="":
                moves.append((nr,nc))
            else:
                if enemy(board[nr][nc]):
                    moves.append((nr,nc))
                break
            nr+=dr; nc+=dc
    return moves

def knight(r,c):
    s=[(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]
    return [(r+dr,c+dc) for dr,dc in s if inside(r+dr,c+dc)
            and (board[r+dr][c+dc]=="" or enemy(board[r+dr][c+dc]))]

def pawn(r,c,p):
    moves=[]
    d = -1 if p[0]==WHITE else 1
    start = 6 if p[0]==WHITE else 1

    if inside(r+d,c) and board[r+d][c]=="":
        moves.append((r+d,c))
        if r==start and board[r+2*d][c]=="":
            moves.append((r+2*d,c))

    for dc in (-1,1):
        if inside(r+d,c+dc):
            if enemy(board[r+d][c+dc]):
                moves.append((r+d,c+dc))
            if en_passant == (r+d,c+dc):
                moves.append((r+d,c+dc))

    return moves

def king(r,c):
    m=[]
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if dr or dc:
                nr,nc=r+dr,c+dc
                if inside(nr,nc) and (board[nr][nc]=="" or enemy(board[nr][nc])):
                    m.append((nr,nc))
    return m

def moves(r,c):
    p=board[r][c]
    if not p or p[0]!=turn: return []
    t=p[1]
    if t=="P": return pawn(r,c,p)
    if t=="R": return ray(r,c,[(1,0),(-1,0),(0,1),(0,-1)])
    if t=="B": return ray(r,c,[(1,1),(1,-1),(-1,1),(-1,-1)])
    if t=="Q": return ray(r,c,[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)])
    if t=="N": return knight(r,c)
    if t=="K": return king(r,c)
    return []

# ---------------- CHECK / END CONDITIONS ----------------
def find_king(color):
    for r in range(8):
        for c in range(8):
            if board[r][c]==color+"K":
                return r,c

def in_check(color):
    kr,kc=find_king(color)
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c][0]!=color:
                if (kr,kc) in moves(r,c):
                    return True
    return False

def legal(r,c):
    res=[]
    for tr,tc in moves(r,c):
        saved = board[tr][tc]
        piece = board[r][c]
        board[tr][tc]=piece
        board[r][c]=""
        ok = not in_check(turn)
        board[r][c]=piece
        board[tr][tc]=saved
        if ok: res.append((tr,tc))
    return res

def has_moves(color):
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c][0]==color:
                if legal(r,c): return True
    return False

# ---------------- AI (MINIMAX) ----------------
VAL = {"P":1,"N":3,"B":3,"R":5,"Q":9,"K":0}

def evaluate():
    s=0
    for r in range(8):
        for c in range(8):
            if board[r][c]:
                v=VAL[board[r][c][1]]
                s += v if board[r][c][0]==WHITE else -v
    return s

def minimax(depth, alpha, beta, maximizing):
    if depth==0:
        return evaluate(), None

    color = WHITE if maximizing else BLACK
    best = None

    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c][0]==color:
                for tr,tc in legal(r,c):
                    saved = board[tr][tc]
                    piece = board[r][c]
                    board[tr][tc]=piece
                    board[r][c]=""
                    val,_ = minimax(depth-1,alpha,beta,not maximizing)
                    board[r][c]=piece
                    board[tr][tc]=saved

                    if maximizing:
                        if val > alpha:
                            alpha, best = val, ((r,c),(tr,tc))
                        if alpha>=beta: return alpha, best
                    else:
                        if val < beta:
                            beta, best = val, ((r,c),(tr,tc))
                        if beta<=alpha: return beta, best
    return (alpha if maximizing else beta), best

# ---------------- DRAW ----------------
def draw():
    screen.fill((0,0,0))
    for r in range(8):
        for c in range(8):
            color = LIGHT if (r+c)%2==0 else DARK
            pygame.draw.rect(screen,color,(c*SQ,r*SQ,SQ,SQ))
            if (r,c) in legal_moves:
                pygame.draw.rect(screen,HIGHLIGHT,(c*SQ,r*SQ,SQ,SQ))
            if board[r][c]:
                txt=FONT.render(UNICODE[board[r][c]],True,(0,0,0))
                screen.blit(txt,(c*SQ+15,r*SQ+10))

    pygame.draw.rect(screen,(50,50,50),(0,640,640,60))
    screen.blit(CLOCK_FONT.render(f"White {white_time//60}:{white_time%60:02}",True,(255,255,255)),(20,650))
    screen.blit(CLOCK_FONT.render(f"Black {black_time//60}:{black_time%60:02}",True,(255,255,255)),(420,650))

# ---------------- MAIN LOOP ----------------
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    now=time.time()
    if turn==WHITE:
        white_time -= int(now-last_tick)
    else:
        black_time -= int(now-last_tick)
    last_tick=now

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type==pygame.MOUSEBUTTONDOWN:
            x,y=e.pos
            if y>=640: continue
            r,c=y//SQ,x//SQ

            if selected:
                sr,sc=selected
                if (r,c) in legal_moves:
                    board[r][c]=board[sr][sc]
                    board[sr][sc]=""
                    turn=BLACK if turn==WHITE else WHITE
                selected=None
                legal_moves=[]
            else:
                if board[r][c] and board[r][c][0]==turn:
                    selected=(r,c)
                    legal_moves=legal(r,c)

    if turn==BLACK:
        _, move = minimax(3, -999, 999, False)
        if move:
            (r,c),(tr,tc)=move
            board[tr][tc]=board[r][c]
            board[r][c]=""
            turn=WHITE

    draw()
    pygame.display.flip()
