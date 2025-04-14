import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25  

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Game window setup
window = tkinter.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg='pink', width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
                       borderwidth=0, highlightthickness=0)
canvas.pack()

# Center window
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Game variables
snake = [Tile(5*TILE_SIZE, 5*TILE_SIZE)]
food = Tile(random.randint(0, COLS-1)*TILE_SIZE, random.randint(0, ROWS-1)*TILE_SIZE)
direction = 'right'
game_over = False

# Prevent direction reversal
def change_direction(new_dir):
    global direction
    if (new_dir == 'up' and direction != 'down') or \
       (new_dir == 'down' and direction != 'up') or \
       (new_dir == 'left' and direction != 'right') or \
       (new_dir == 'right' and direction != 'left'):
        direction = new_dir

# Add score tracking
score = 0

def move_snake():
    global snake, food, game_over, score
    
    if game_over:
        return
        
    head = snake[0]
    new_head = Tile(head.x, head.y)
    
    if direction == 'up':
        new_head.y -= TILE_SIZE
    elif direction == 'down':
        new_head.y += TILE_SIZE
    elif direction == 'left':
        new_head.x -= TILE_SIZE
    elif direction == 'right':
        new_head.x += TILE_SIZE
        
    # Check wall collisions
    if (new_head.x < 0 or new_head.x >= WINDOW_WIDTH or
        new_head.y < 0 or new_head.y >= WINDOW_HEIGHT):
        game_over = True
        return
        
    # Check self collisions
    for segment in snake[1:]:
        if new_head.x == segment.x and new_head.y == segment.y:
            game_over = True
            return
        
    snake.insert(0, new_head)
    
    # Check food collision
    if new_head.x == food.x and new_head.y == food.y:
        food = Tile(random.randint(0, COLS-1)*TILE_SIZE, random.randint(0, ROWS-1)*TILE_SIZE)
        score += 1
    else:
        snake.pop()

def draw():
    canvas.delete("all")
    
    # Draw score
    canvas.create_text(30, 20, text=f"Score: {score}", 
                     fill="white", font=('Arial', 12))
    
    # Draw snake
    for segment in snake:
        canvas.create_rectangle(segment.x, segment.y, 
                              segment.x + TILE_SIZE, segment.y + TILE_SIZE,
                              fill="lime green", outline="dark green")
    
    # Draw food
    canvas.create_oval(food.x, food.y, 
                     food.x + TILE_SIZE, food.y + TILE_SIZE,
                     fill="red", outline="dark red")
    
    if game_over:
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 30,
                         text="GAME OVER", fill="white", font=('Arial', 24))
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30,
                         text=f"Final Score: {score}", fill="white", font=('Arial', 20))
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 80,
                         text="Press SPACE to exit", fill="white", font=('Arial', 16))
    else:
        move_snake()
        window.after(150, draw)

def exit_game(event):
    window.destroy()

window.bind('<space>', exit_game)

window.bind('<Up>', lambda e: change_direction('up'))
window.bind('<Down>', lambda e: change_direction('down'))
window.bind('<Left>', lambda e: change_direction('left'))
window.bind('<Right>', lambda e: change_direction('right'))

draw()
window.mainloop()
