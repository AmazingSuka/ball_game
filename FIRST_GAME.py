import tkinter as tk
import random as rnd

#Constants
WIDTH = 1200
HEIGHT = 600
BAD_COLOR = "black"
COLORS = ['aqua', 'blue', 'pink', 'yellow', 'gold', BAD_COLOR]
BACK_COLOR = "white"
ZERO = 0
BALL_RADIUS = 30
BALL_COLOR = 'red'
BALLS_COUNT = 10
INIT_DX = 2
INIT_DY = 2
DELAY = 10

#balls class
class Balls():
    def __init__(self, x, y, r, color, dx=0, dy=0):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.dx = dx
        self.dy = dy
        
    def draw(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r , self.y + self.r,
                           fill=self.color, outline= self.color)
                           
    def hide(self):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r , self.y + self.r,
                           fill=BACK_COLOR, outline= BACK_COLOR)
                           
    def is_colision(self, small_ball):
        a = abs(self.x + self.dx - small_ball.x)
        b = abs(self.y + self.dy - small_ball.y)
        return (a**2 + b**2)**0.5 <= self.r + small_ball.r
        
    def move(self): 
        # Collading
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= ZERO):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dx <= ZERO):
            self.dy = -self.dy
        #colliding with balls
        for small_ball in small_balls:
            if self.is_colision(small_ball):
                if small_ball.color != BAD_COLOR: # good ball
                    small_ball.hide()
                    small_balls.remove(small_ball)
                    self.dx = -self.dx
                    self.dy = -self.dy
                else:
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()
    


#mouse events 
def mouse_click(event):
    global ball
    if event.num == 1:
        if 'ball' not in globals():
            ball = Balls(event.x, event.y, BALL_RADIUS, BALL_COLOR, INIT_DX , INIT_DY)
            ball.draw()
        else:
            if ball.dx * ball.dy > 0:
                ball.dy = -ball.dy
            else:
                ball.dx = -ball.dx
    elif event.num == 3:
        if ball.dx * ball.dy > 0:
            ball.dx = -ball.dx
        else:
            ball.dy = -ball.dy 
        
#create random balls on the map
def create_small_balls(number):
    lst = []
    while len(lst) < number:
            small_ball = Balls(rnd.choice(range(0,WIDTH)),
                               rnd.choice(range(0,HEIGHT)),
                               rnd.choice(range(15,35)),
                               rnd.choice(COLORS))
            lst.append(small_ball)
            small_ball.draw()
    return lst

#bad balls count
def count_bad_balls(list_balls):
    result = 0
    for ball in list_balls:
        if ball.color == BAD_COLOR:
            result+= 1
    return result
         
#main
def main():
    if 'ball' in globals():
        ball.move()
        if len(small_balls) - num_bad_balls == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="YOU WIN!", font='Arial 20', fill= BALL_COLOR)
            ball.dx = ball.dy = 0
        elif ball.dx == 0:
            canvas.create_text(WIDTH / 2, HEIGHT / 2, text="YOU LOSE!", font='Arial 20', fill= BAD_COLOR)
    root.after(DELAY, main)


root = tk.Tk()
root.title("First Game For Practic")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BACK_COLOR)
canvas.pack()
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-3>', mouse_click)
if 'ball' in globals():
    del ball
small_balls = create_small_balls(BALLS_COUNT)
num_bad_balls = count_bad_balls(small_balls)
main()
root.mainloop()
