# import library
import tkinter  # Graphic Use (tk interface library)
import random  # random placing food point each time

#---Interface SetUp
ROWS = 25
COLUMNS = 25
TILE_SIZE = 25

#---25 * 25 = 625
WINDOW_WIDTH = TILE_SIZE * COLUMNS
WINDOW_HEIGHT = TILE_SIZE * ROWS

#storing (x,y) and food position (coord)
class Tile: 
    def __init__(self, x, y) -> None: #crtl + space
        self.x = x
        self.y = y

#---Game Window
window = tkinter.Tk()
window.title("Snake")
#width, height (625, 625) / no allows user to change the window size by expanding
window.resizable(False, False)  

canvas = tkinter.Canvas(
    window,
    bg="black",
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    borderwidth=0,
    highlightthickness=0,
)
canvas.pack()
window.update()

#---Setting the size center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height= window.winfo_screenheight()

#---Calculate the (x,y) position to place the window on the center
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#Set the size and position of the window: format "(w) x (h) + (x) + (y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#---Init the game (Var)
#single tile, snake's head
snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)#Pixel so need to * TILESIZE
food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
#---Velocity (the change of position everytime)
velocityX = 0
velocityY = 0
snake_body = [] #multiple snake tiles (store the body part everytime eat food)
game_over = False
score = 0

#---Game Looping
def change_direction(e): #e = event
    # print(e)
    # print(e.keysym)

    global velocityX, velocityY, game_over
    if (game_over):
        return #edit this code to reset game variables to play again

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0 # no moving to left or right
        velocityY = -1 # moving up
        
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1

    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score
    #---Game Stop
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    #---Prevent Food ON snake body
    def generate_food_position():
        global food
        while True:
            food.x = random.randint(0, COLUMNS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE
            if not any(tile.x == food.x and tile.y == food.y for tile in snake_body):
                break

    #---Collision to food
    if (snake.x == food.x and snake.y == food.y): #same coord of snake & food
        snake_body.append(Tile(food.x, food.y))
        # food.x = random.randint(0, COLUMNS-1) * TILE_SIZE #place the food in new place after eating
        # food.y = random.randint(0, ROWS-1) * TILE_SIZE
        generate_food_position()
        score += 1

    #---Update snake body (make the body move togather with head)
    #starting from last segment and move towards the head(iterate each segment)
        #range() generates a sequence of numbers from the starting index to one less than the stopping index
        #len(snake_body)-1 start from behind of the snake body by minus 1 to get the index
        #-1 stopping index for the loop ( stop at index 0)
        #-1 step of the loop (loop iterates in reverse)
            #the loop starts from the last element (len(snake_body)-1), goes down to 0, and each time decrements by 1
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0): #if head = 0
            #update its position to be the same as the current position of the snake's head
            tile.x = snake.x
            tile.y = snake.y
        else:
            #update its position to be the same as the position of the segment that comes before it 
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y
    
    snake.x += velocityX * TILE_SIZE  #if no * tile size if move, move 1 pixel over
    snake.y += velocityY * TILE_SIZE

def reset():
     global snake, food, snake_body, game_over, score, velocityX, velocityY
     snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
     food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)
     velocityX = 0
     velocityY = 0
     snake_body = [] #multiple snake tiles (store the body part everytime eat food)
     game_over = False
     score = 0

# Draw Snake
def draw():
    global snake # refer the snake var outside def
    move()

    canvas.delete("all") #clear the frame (everytime creatre new frame, clear prvious frame)

     #food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = 'red')

    #snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "white") #(TL,TR,BL,BR, Color)

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = 'lime green')

    if (game_over):
        #over msg
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Arial 20", text = f"Game Over: {score} \nPress r for Restart", fill = "white")
    else:
        #score
        canvas.create_text(30, 20, font = "Arial 10 bold", text = f"Score: {score}", fill = "white")

    window.after(100, draw) #100ms = 1/10 second, 10 frame second, every 10s draw new
    
draw()
# window.bind("<KeyRelease>", change_direction) #when you press on any key and then let go

window.bind("r", lambda event:reset())
window.bind("<Up>", change_direction)
window.bind("<Down>", change_direction)
window.bind("<Left>", change_direction)
window.bind("<Right>", change_direction)

window.mainloop()  # keep window running
