from collections import deque

def setup():
    global coin, player
    size(800, 800)
    frameRate(30)
    coin = loadImage('Score.png')
    player = loadImage('Player.png')
# ----------------------------------------------------------------------- Basic Variable Setting
dimension = 16
l = 800 // 16

sq_array = [[[True] for _ in range(dimension)] for _ in range(dimension)]

col = -1
row = -1
colCir = -1
rowCir = -1
remain = False
x = 0
y = 0
Score = 0
moving = False
path = []
coin = None
# -----------------------------------------------------------------------

def find_path(start, goal, sq_array): # Use BFS / start : Now (x, y) & goal : Score (x, y)
    visited = [[False] * dimension for _ in range(dimension)]
    parent = [[None] * dimension for _ in range(dimension)]
    # parent[y][x] = previous location
    queue = deque() # for use popleft
    
    sx, sy = start
    gx, gy = goal

    # return = [(a1, b1), (a2, b2), (a3, b3), (a4, b4), ..., (gx, gy)]
    # repeat popleft(return) and move to return[0] -> move to (gx, gy)

    queue.append((sx, sy))
    visited[sy][sx] = True # start location
    
    dx = [1, -1, 0, 0] # 0 : right | 1 : left | 2 : stop | 3 : stop
    dy = [0, 0, 1, -1] # 0 : stop  | 1 : stop | 2 : down | 3 : up
    # dx[n], dy[n]
    # n = 0 -> right | n = 1 -> left | n = 2 -> down | n = 3 -> up
    
    while queue:
        x, y = queue.popleft()
        
        if (x, y) == (gx, gy): # complete
            break
        
        for i in range(4): # 4 direction move
            nx = x + dx[i]
            ny = y + dy[i] # (nx, ny) = moved (x, y)
            if 0 <= nx < dimension and 0 <= ny < dimension: # move is valid
                if not visited[ny][nx] and sq_array[ny][nx]: # not visited & can move
                    visited[ny][nx] = True
                    parent[ny][nx] = (x, y) # record previous location
                    queue.append((nx, ny))
    # move every possible path and save best path
    # after while
    # parent = best move list
    # while test like spreading : spreading ink in water ( 4 direction move )
            
    path = []
    cur = (gx, gy)
    while cur != (sx, sy):
        path.append(cur)
        cur = parent[cur[1]][cur[0]] # inversion calculate
        if cur is None:
            return [] # path doesn't exist
    path.reverse() # reverse again to restore
    return path


def mouseClicked(): # Score & Barrier Place
    global l, col, row, remain, sq_array, colCir, rowCir
    if mouseButton == LEFT:
        colCir = mouseX // l
        rowCir = mouseY // l
        remain = True

    elif mouseButton == RIGHT:
        col = mouseX // l
        row = mouseY // l
        sq_array[row][col] = not sq_array[row][col]

def keyPressed(): # Space Detection -> find path
    global moving, path
    if key == ' ' and colCir != -1 and rowCir != -1:
        path = find_path((x, y), (colCir, rowCir), sq_array)
        if path:
            moving = True


def draw():
    global dimension, l, sq_array, col, row, remain, x, y, colCir, rowCir, Score, moving, path, coin, player
    background(255)

    if mousePressed and mouseButton == RIGHT and keyPressed and key == 'q': # press q & Right -> Place Barrier
        col_drag = mouseX // l
        row_drag = mouseY // l
        if 0 <= col_drag < dimension and 0 <= row_drag < dimension:
            sq_array[row_drag][col_drag] = False
    
    if mousePressed and mouseButton == RIGHT and keyPressed and key == 'w': # press w & Right -> Remove Barrier
        col_drag = mouseX // l
        row_drag = mouseY // l
        if 0 <= col_drag < dimension and 0 <= row_drag < dimension:
            sq_array[row_drag][col_drag] = True
    
# ----------------------------------------------------------------------- Square Coloring
    for i in range(dimension):
        for j in range(dimension):
            if (i + j) % 2 == 0:
                noStroke()
                fill(235, 236, 210)
                if not sq_array[i][j]:
                    fill(236, 125, 106)
            else:
                noStroke()
                fill(115, 149, 87)
                if not sq_array[i][j]:
                    fill(212, 108, 81)
            rectMode(CORNERS)
            rect(l * j, l * i, l * (j + 1), l * (i + 1))
# ----------------------------------------------------------------------- Placing Score
    if remain and colCir != -1 and rowCir != -1:
        imageMode(CENTER)
        image(coin, colCir * l + l / 2, rowCir * l + l / 2, l - 10, l - 10)
# ----------------------------------------------------------------------- 

    imageMode(CENTER)
    image(player, l * x + l/2, l * y + l/2, l - 10, l -10)
                
    if moving and path: # Space Pressed & path exsist
        next_pos = path.pop(0)
        x, y = next_pos
        if (x, y) == (colCir, rowCir):
            moving = False
            remain = False
            Score += 1
        
    fill(0)
    textSize(20)
    text("Score : " + str(Score), 10, height - 10)
