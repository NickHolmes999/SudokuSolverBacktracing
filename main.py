import pygame # Import pygame library
import copy # Import copy library to make a deep copy of the grid
import random # Import random library to generate random numbers

def generate_sudoku():
    # Starting with a solved board, you might use something like the following
    base  = 3
    side  = base*base

    # pattern for a baseline valid solution
    def pattern(r,c): return (base*(r%base)+r//base+c)%side

    # randomize rows, columns and numbers (of valid base pattern)
    def shuffle(s): return random.sample(s,len(s))
    rBase = range(base)
    rows  = [ g*base + r for g in shuffle(rBase) for r in shuffle(rBase) ]
    cols  = [ g*base + c for g in shuffle(rBase) for c in shuffle(rBase) ]
    nums  = shuffle(range(1,base*base+1))

    # produce board using randomized baseline pattern
    return [ [nums[pattern(r,c)] for c in cols] for r in rows ]

pygame.font.init() # Initialize pygame font
screen = pygame.display.set_mode((800, 800)) # Set screen size
pygame.display.set_caption('SUDOKU SOLVER(BACKTRACING)')    # Set title of screen
img = pygame.image.load('icon.png') # Load icon image
pygame.display.set_icon(img) # Set icon image
font1 = pygame.font.SysFont('comicsans', 40) # Set font for numbers
font2 = pygame.font.SysFont('comicsans', 20)    # Set font for instructions
x = 0
y = 0
dif = 500 / 9
val = 0


def create_puzzle(board, difficulty):
    puzzle = copy.deepcopy(board)
    total_cells = 81

    # Set the number of cells to empty, depending on the difficulty level
    if difficulty == 'easy':
        num_to_remove = 20
    elif difficulty == 'medium':
        num_to_remove = 30
    elif difficulty == 'hard':
        num_to_remove = 40

    for _ in range(num_to_remove):
        x = random.randint(0, 8)
        y = random.randint(0, 8)
        puzzle[x][y] = 0

    return puzzle

start_ticks = pygame.time.get_ticks()  # Define start_ticks globally
stop_ticks = 0

def display_timer():
    global start_ticks, stop_ticks
    current_time = pygame.time.get_ticks()
    elapsed_time = stop_ticks - start_ticks
    time_text = font2.render(f'Time: {elapsed_time/1000}', True, (0, 0, 0))
    screen.blit(time_text, (500, 10))



def select_difficulty():
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont('comicsans', 32)
    global start_ticks, stop_ticks # Define start_ticks globally

    text1 = font.render('Select Difficulty', 1, (0, 0, 0))
    text2 = font.render('1: Easy', 1, (0, 0, 0))
    text3 = font.render('2: Medium', 1, (0, 0, 0))
    text4 = font.render('3: Hard', 1, (0, 0, 0))

    screen.blit(text1, (200, 100))
    screen.blit(text2, (200, 200))
    screen.blit(text3, (200, 300))
    screen.blit(text4, (200, 400))

    pygame.display.update()


    selecting = True # Loop until a valid difficulty is selected
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                full_board = generate_sudoku()
                if event.key == pygame.K_1:
                    start_ticks = pygame.time.get_ticks()  # Reset start_ticks here
                    result = create_puzzle(full_board, 'easy')
                    display_timer()  # Call display_timer() here
                    return result
                elif event.key == pygame.K_2:
                    start_ticks = pygame.time.get_ticks()  # Reset start_ticks here
                    result = create_puzzle(full_board, 'medium')
                    display_timer()  # Call display_timer() here
                    return result
                elif event.key == pygame.K_3:
                    start_ticks = pygame.time.get_ticks()  # Reset start_ticks here
                    result = create_puzzle(full_board, 'hard')
                    display_timer()  # Call display_timer() here
                    return result

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()



# Replace the original grid variable with a function call
grid = select_difficulty()

# Make a deep copy of the original grid for reset functionality
original_grid = copy.deepcopy(grid)

def get_coord(pos): # Get the position of the mouse click
   x = pos[0] // dif
   y = pos[1] // dif


def draw_box(): # Draw red lines to form 9x9 grid
   for i in range(2):
       pygame.draw.line(screen, (255, 0, 0), (x * dif-3, (y + i)
                        * dif), (x * dif + dif + 3, (y + i)*dif), 7)
       pygame.draw.line(screen, (255, 0, 0), ((x + i) * dif,
                        y * dif), ((x + i) * dif, y * dif + dif), 7)


def draw(): # Draw the numbers in the grid
   for i in range(9):
       for j in range(9):
           if grid[i][j] != 0:
               pygame.draw.rect(screen, (0, 255, 0),
                                (i * dif, j * dif, dif + 1, dif + 1))
               text1 = font1.render(str(grid[i][j]), 1, (0, 0, 0))
               screen.blit(text1, (i * dif + 15, j * dif + 5))

   for i in range(10): # Draw the lines that form the 9x9 grid
       if i % 3 == 0:
           thick = 7
       else:
           thick = 1
       pygame.draw.line(screen, (0, 0, 0), (0, i * dif),
                        (500, i * dif), thick)
       pygame.draw.line(screen, (0, 0, 0), (i * dif, 0),
                        (i * dif, 500), thick)


def draw_val(val): # Draw the value entered by the user
   text1 = font1.render(str(val), 1, (0, 0, 0))
   screen.blit(text1, (x * dif + 15, y * dif + 15))


def raise_error_1(): # Raise error when wrong value entered
   text1 = font1.render('WRONG !!!', 1, (0, 0, 0))
   screen.blit(text1, (20, 570))


def raise_error_2(): # Raise error when wrong key is pressed
   text1 = font1.render('Not a valid Key', 1, (0, 0, 0))
   screen.blit(text1, (20, 570))


def valid(m, i, j, val): # Check if the value entered is valid
   for it in range(9):
       if m[i][it] == val:
           return False
       if m[it][j] == val:
           return False

   it = i // 3
   jt = j // 3

   for i in range(it * 3, it * 3 + 3):
       for j in range(jt * 3, jt * 3 + 3):
           if m[i][j] == val:
               return False
   return True


def solve(grid, i, j): # Solve the sudoku using backtracking
   while grid[i][j] != 0:
       if i < 8:
           i += 1
       elif i == 8 and j < 8:
           i = 0
           j += 1
       elif i == 8 and j == 8:
           return True

   pygame.event.pump() # Process events
   for it in range(1, 10):
       if valid(grid, i, j, it) == True:
           grid[i][j] = it
           x = i
           y = j
           screen.fill((255, 255, 255))
           draw()
           draw_box()
           pygame.display.update()
           pygame.time.delay(20)

           if solve(grid, i, j) == 1:
               return True
           else:
               grid[i][j] = 0
           screen.fill((255, 255, 255))

           draw()
           draw_box()
           pygame.display.update()
           pygame.time.delay(50)
   return False


def instruction(): # Display instruction to use the game
  text1 = font2.render(
      'PRESS D TO RESET TO DEFAULT / R TO EMPTY\n', 1, (0, 0, 0))
  text2 = font2.render(
      'ENTER VALUES AND PRESS ENTER TO VISUALIZE\n', 1, (0, 0, 0))
  screen.blit(text1, (20, 520))
  screen.blit(text2, (20, 540))


def result(): # Display the result
  global stop_ticks
  stop_ticks = pygame.time.get_ticks()  # Update stop_ticks here
  text1 = font1.render('FINISHED PRESS R or D\n', 1, (0, 0, 0))
  screen.blit(text1, (20, 570))


run = True # Run the game loop
flag_1 = 0 # Flag to check if a key is pressed
flag_2 = 0 # Flag to check if enter is pressed
rs = 0  # Flag to check if result is displayed
error = 0   # Variable to check if there is an error
while run: # Run the game loop
   screen.fill((255, 255, 255)) # Fill the screen with white color
   for event in pygame.event.get(): # Process events
       if event.type == pygame.QUIT: # If user clicks close button
           run = False
       if event.type == pygame.MOUSEBUTTONDOWN: # If user clicks mouse
           flag_1 = 1
           pos = pygame.mouse.get_pos() # Get the position of the mouse click
           get_coord(pos)
       if event.type == pygame.KEYDOWN:  # If user presses a key
           if event.key == pygame.K_LEFT:
               if x > 0:  # Check if x is not at the left edge
                   x -= 1
                   flag_1 = 1
           if event.key == pygame.K_RIGHT:
               if x < 8:  # Check if x is not at the right edge
                   x += 1
                   flag_1 = 1
           if event.key == pygame.K_UP:
               if y > 0:  # Check if y is not at the top edge
                   y -= 1
                   flag_1 = 1
           if event.key == pygame.K_DOWN:
               if y < 8:  # Check if y is not at the bottom edge
                   y += 1
                   flag_1 = 1
           if event.key == pygame.K_1:
               val = 1
           if event.key == pygame.K_2:
               val = 2
           if event.key == pygame.K_3:
               val = 3
           if event.key == pygame.K_4:
               val = 4
           if event.key == pygame.K_5:
               val = 5
           if event.key == pygame.K_6:
               val = 6
           if event.key == pygame.K_7:
               val = 7
           if event.key == pygame.K_8:
               val = 8
           if event.key == pygame.K_9:
               val = 9
           if event.key == pygame.K_RETURN:
               flag_2 = 1

           # If R pressed clear sudoku board
           if event.key == pygame.K_r:
               rs = 0
               error = 0
               flag_2 = 0
               grid = [
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0]
               ]

           # If D pressed reset board to default
           if event.key == pygame.K_d:
               rs = 0
               error = 0
               flag_2 = 0
               grid = copy.deepcopy(original_grid)
       if rs == 1:
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:
                   rs = 0
                   error = 0
                   flag_2 = 0
                   grid = select_difficulty()
               elif event.key == pygame.K_2:
                   rs = 0
                   error = 0
                   flag_2 = 0
                   grid = select_difficulty()
               elif event.key == pygame.K_3:
                   rs = 0
                   error = 0
                   flag_2 = 0
                   grid = select_difficulty()
           result()
           display_timer()

   if flag_2 == 1: # Call solve function when enter is pressed
       if solve(grid, 0, 0) == False:
           error = 1
       else:
           rs = 1
       flag_2 = 0

   if val != 0: # Draw only when val is not 0
       draw_val(val)
       if valid(grid, int(x), int(y), val) == True:
           grid[int(x)][int(y)] = val
           flag_1 = 0
       else:
           grid[int(x)][int(y)] = 0
           raise_error_2()
       val = 0

   if error == 1: # If there is an error display it
       raise_error_1()
   draw()
   if flag_1 == 1:
       draw_box()
   instruction() # Display instructions
   display_timer()

   pygame.display.update() # Update the display
