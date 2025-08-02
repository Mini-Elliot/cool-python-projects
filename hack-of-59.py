import pygame, random, sys, json, heapq, hashlib
pygame.init()

WIDTH, HEIGHT = 960, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hack of 5/9")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("arial", 20)

WHITE=(255,255,255);BLACK=(0,0,0);GREEN=(50,200,50);RED=(200,50,50);BLUE=(50,50,200);YELLOW=(255,255,0);ORANGE=(255,165,0)

SAVE_FILE="save.json"
PASSWORD_FILE="hacked_password.json"

# ===================== SAVE / LOAD =====================
def save_game(data):
    with open(SAVE_FILE,"w") as f: json.dump(data,f)

def load_game():
    try:
        with open(SAVE_FILE,"r") as f: return json.load(f)
    except:
        return {"level":1,"score":0,"currency":0}

def save_password(password,code):
    with open(PASSWORD_FILE,"w") as f: json.dump({"password":password,"code":code},f)

def load_password():
    try:
        with open(PASSWORD_FILE,"r") as f: return json.load(f)
    except:
        return None

def simple_hash(word):
    return hashlib.sha256(word.encode()).hexdigest()[:6]

# ===================== HACKING GAME =====================
def hacking_game():
    words=["robot","fsociety","elliot","darkarmy","whiterose"]
    password=random.choice(words)
    hash_val=simple_hash(password)
    step=1
    user_input=""
    timer=600
    code=random.randint(1000,9999)

    while True:
        CLOCK.tick(30);WIN.fill(BLACK)

        if step==1:
            WIN.blit(FONT.render(f"Crack this hash: {hash_val}",True,WHITE),(250,250))
            WIN.blit(FONT.render(f"Type password guess: {user_input}",True,GREEN),(250,300))
        elif step==2:
            WIN.blit(FONT.render(f"Password correct! Retrieved file with code {code}",True,WHITE),(180,250))
            WIN.blit(FONT.render("Remember this code! Press ENTER to finish.",True,GREEN),(180,300))

        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if step==1:
                    if e.key==pygame.K_RETURN:
                        if user_input==password:
                            step=2
                            save_password(password,code)
                            user_input=""
                        else:
                            user_input=""
                    elif e.key==pygame.K_BACKSPACE:
                        user_input=user_input[:-1]
                    elif e.unicode.isalpha():
                        user_input+=e.unicode
                elif step==2 and e.key==pygame.K_RETURN:
                    return True

        timer-=1
        if timer<=0:
            return False

# ===================== A* PATHFINDING =====================
class Node:
    def __init__(self,x,y):
        self.x=x;self.y=y;self.g=self.h=self.f=0;self.parent=None
    def __lt__(self,o): return self.f<o.f

def astar(start,end,obstacles,grid_size=40):
    start_node,end_node=Node(*start),Node(*end)
    open_list,closed=[],[]
    heapq.heappush(open_list,(0,start_node))
    while open_list:
        _,curr=heapq.heappop(open_list)
        closed.append(curr)
        if (curr.x,curr.y)==(end_node.x,end_node.y):
            path=[]
            while curr:
                path.append((curr.x,curr.y));curr=curr.parent
            return path[::-1]
        for dx,dy in [(0,1),(1,0),(-1,0),(0,-1)]:
            nx,ny=curr.x+dx,curr.y+dy
            if nx<0 or ny<0 or nx>=WIDTH//grid_size or ny>=HEIGHT//grid_size: continue
            if any(abs(nx*grid_size-ox)<40 and abs(ny*grid_size-oy)<40 for ox,oy,_,_ in obstacles): continue
            node=Node(nx,ny)
            if any(c.x==nx and c.y==ny for c in closed): continue
            node.g=curr.g+1;node.h=abs(nx-end_node.x)+abs(ny-end_node.y);node.f=node.g+node.h;node.parent=curr
            if not any(o[1].x==nx and o[1].y==ny for o in open_list): heapq.heappush(open_list,(node.f,node))
    return []

# ===================== INVENTORY =====================
class Inventory:
    def __init__(self): self.items={"metal":0,"crystal":0}
    def add(self,item): self.items[item]=self.items.get(item,0)+1
    def craft(self):
        if self.items["metal"]>=2 and self.items["crystal"]>=1:
            self.items["metal"]-=2;self.items["crystal"]-=1
            return "super"
        return None

# ===================== PLAYER =====================
class Player:
    def __init__(self):
        self.x,self.y=WIDTH//2,HEIGHT-60;self.size=35;self.speed=5
        self.health=100;self.weapon="single";self.bullets=[]
        self.score=0;self.currency=0;self.inventory=Inventory()
    def draw(self):
        pygame.draw.rect(WIN,BLUE,(self.x,self.y,self.size,self.size))
        for b in self.bullets: pygame.draw.rect(WIN,YELLOW,(b[0],b[1],6,12))
    def move(self,keys):
        if keys[pygame.K_LEFT] and self.x>0:self.x-=self.speed
        if keys[pygame.K_RIGHT] and self.x<WIDTH-self.size:self.x+=self.speed
        if keys[pygame.K_UP] and self.y>0:self.y-=self.speed
        if keys[pygame.K_DOWN] and self.y<HEIGHT-self.size:self.y+=self.speed
    def shoot(self):
        offs=[(self.size//2,0)] if self.weapon=="single" else [(5,0),(self.size-10,0)]
        if self.weapon=="super": offs+=[(self.size//2,0)]
        for ox,oy in offs:self.bullets.append([self.x+ox,self.y])
    def update_bullets(self):
        for b in self.bullets: b[1]-=9
        self.bullets=[b for b in self.bullets if b[1]>0]

# ===================== ENEMY =====================
class Enemy:
    def __init__(self,obstacles,is_boss=False):
        self.grid=40;self.x=random.randint(0,WIDTH-30);self.y=random.randint(-150,-40)
        self.size=60 if is_boss else 30
        self.health=50 if is_boss else 10
        self.is_boss=is_boss
        self.path=[];self.obstacles=obstacles
    def draw(self): pygame.draw.rect(WIN,RED,(self.x,self.y,self.size,self.size))
    def move(self,target):
        if not self.path or random.random()<0.02:
            sx,sy=self.x//self.grid,self.y//self.grid;tx,ty=target.x//self.grid,target.y//self.grid
            self.path=astar((sx,sy),(tx,ty),self.obstacles,self.grid)
        if self.path:
            nx,ny=self.path[0];tx,ty=nx*self.grid,ny*self.grid
            if abs(self.x-tx)<3 and abs(self.y-ty)<3:self.path.pop(0)
            else:
                self.x+=(tx-self.x)*0.05;self.y+=(ty-self.y)*0.05

# ===================== MAIN LOOP =====================
def main():
    data=load_game();level=data["level"];player=Player()
    enemies=[];obstacles=[(random.randint(50,WIDTH-50),random.randint(100,HEIGHT-150),40,20) for _ in range(8)]
    spawn_timer=0

    while True:
        CLOCK.tick(60);WIN.fill(BLACK);keys=pygame.key.get_pressed()
        for e in pygame.event.get():
            if e.type==pygame.QUIT:pygame.quit();sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:player.shoot()
                if e.key==pygame.K_s:save_game({"level":level,"score":player.score,"currency":player.currency})

        if level==3:
            if hacking_game(): level+=1
        else:
            spawn_timer+=1
            if spawn_timer>max(20,60-level*4):
                boss=(level in [5,10]) and len(enemies)==0
                enemies.append(Enemy(obstacles,is_boss=boss));spawn_timer=0

            player.move(keys);player.update_bullets();player.draw()

            for en in enemies[:]:
                en.move(player);en.draw()
                for b in player.bullets:
                    if en.x<b[0]<en.x+en.size and en.y<b[1]<en.y+en.size:
                        if b in player.bullets:player.bullets.remove(b)
                        en.health-=10
                        if en.health<=0:
                            enemies.remove(en);player.score+=10;player.currency+=5
                            if len(enemies)==0 and (level<10): level+=1

        WIN.blit(FONT.render(f"Level:{level} Score:{player.score} Curr:{player.currency}",True,WHITE),(10,10))
        WIN.blit(FONT.render("Press S to Save",True,ORANGE),(10,40))
        pygame.display.update()

main()
