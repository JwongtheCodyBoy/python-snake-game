import pygame as pg
import sys
import random

pg.init()

SW, SH = 800, 800

BLOCK_SIZE = 50;
FONT = pg.font.Font("Satoshi-Variable.ttf", BLOCK_SIZE*2)

screen = pg.display.set_mode((SW,SH))
pg.display.set_caption("Snake")
clock = pg.time.Clock()

class Snake: 
    def __init__(self):
        self.x, self.y = int((SW/4)/BLOCK_SIZE) * BLOCK_SIZE, int((SH/2)/BLOCK_SIZE) * BLOCK_SIZE       # divide by BLOCK_SIZE to get a relative point, int() to floor the float, multiply BLOCK_SIZE to get back floored position           
        self.xdir = 1   # -1 Left   0 no move   1 Right
        self.ydir = 0   # 1 Down   0 no move   -1 Up        Because pygame screen grid (0,0) is at top left (Like openCV)
        self.head = pg.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        self.body = [pg.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
        self.dead = False
    
    def update(self):
        self.checkDeath()
        global apple

        if self.dead:
            menu()

        self.body.append(self.head)
        for i in range(len(self.body)-1):
            self.body[i].x = self.body[i+1].x
            self.body[i].y = self.body[i+1].y

        self.head.x += self.xdir * BLOCK_SIZE
        self.head.y += self.ydir * BLOCK_SIZE

        self.body.remove(self.head)

    def checkDeath(self):
        for square in self.body:
            if self.head.x == square.x and self.head.y == square.y:
                self.dead = True
            if self.head.x not in range(0, SW) or self.head.y not in range(0, SH):      # Demorgans law >:)
                self.dead = True

class Apple:
    def __init__(self):
        self.x = int(random.randint(0, SW)/BLOCK_SIZE) * BLOCK_SIZE
        self.y = int(random.randint(0, SH)/BLOCK_SIZE) * BLOCK_SIZE
        self.rect = pg.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

    def update(self):
        pg.draw.rect(screen, "red", self.rect)      

def drawGrid():                                        # Nested for loop that draws grid (optional)
    for x in range(0, SW, BLOCK_SIZE):
        for y in range(0, SH, BLOCK_SIZE):
            rect = pg.Rect(x,y,BLOCK_SIZE, BLOCK_SIZE)
            pg.draw.rect(screen, "#3c3c3b", rect, 1)

# ChatGPT menu
button_width, button_height = int(SW *0.3), int(SH *0.18)
play_button_rect = pg.Rect(SW // 4 - button_width // 2, SH // 2 - button_height // 2, button_width, button_height)
exit_button_rect = pg.Rect(3 * SW // 4 - button_width // 2, SH // 2 - button_height // 2, button_width, button_height)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

def draw_buttons():
    pg.draw.rect(screen, GRAY, play_button_rect)
    pg.draw.rect(screen, GRAY, exit_button_rect)
    play_text = FONT.render("Play", True, WHITE)
    exit_text = FONT.render("Exit", True, WHITE)
    screen.blit(play_text, (play_button_rect.x + (button_width - play_text.get_width()) // 2, play_button_rect.y + (button_height - play_text.get_height()) // 2))
    screen.blit(exit_text, (exit_button_rect.x + (button_width - exit_text.get_width()) // 2, exit_button_rect.y + (button_height - exit_text.get_height()) // 2))

def menu():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    print("Play button clicked!")
                    PlayGame()
                elif exit_button_rect.collidepoint(event.pos):
                    pg.quit()
                    sys.exit()

        # screen.fill(BLACK)
        draw_buttons()
        pg.display.flip()
    
def PlayGame():
    score = FONT.render("0", True, "white")
    score_rect = score.get_rect(center=(SW/2, SH/16))

    drawGrid()

    snake = Snake()

    apple = Apple()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN and snake.ydir != -1:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pg.K_UP and snake.ydir != 1:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pg.K_RIGHT and snake.xdir != -1:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pg.K_LEFT and snake.xdir != 1:
                    snake.ydir = 0
                    snake.xdir = -1

        snake.update()
        screen.fill('black')
        drawGrid()

        apple.update()

        score = FONT.render(f"{len(snake.body)-1}", True, "white")      # Update score

        pg.draw.rect(screen, "green", snake.head)

        for square in snake.body:
            pg.draw.rect(screen, "green", square)

        screen.blit(score,score_rect)       # Display Score
                
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pg.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))      # square exists here because Python is built different (so square == the last piece of body from previous frame)
            apple = Apple()

        pg.display.update()
        clock.tick(10)      # delay in ms

menu()