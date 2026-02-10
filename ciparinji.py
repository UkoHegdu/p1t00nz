import math
import copy
import pygame
import time
import json
import os

# I have not finished this but for now I will leave it as it is
# it is a game I played in my notebooks while in university, here it is without redrawing and with the option to check for hints (to play it properly - in the hard mode)
# The help menu explains, but you need to erase all the numbers to finish and the numbers need to be matching AND adjacent. Depending on what you decide to erase
# you will come across different scenarios. If you think the code is shit it's because this is my first piece of code in Python and... first piece of code in Github.
# The last time I coded anything was in c++ around 20 years ago. Anyway, who cares :D enjoy the game. Btw minimum number of turns I've got for the difficult difficulty is 4.
# I was about to implement the moves functionality, but I lost interest in this, so it is not written anywhere, just printed in console. You can copy it if you manage to finish the game in 4 turns or less.

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 1010
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ruutinju klade")

# Set window icon
icon = pygame.image.load('skein_icon.png')
pygame.display.set_icon(icon)
help_image = pygame.image.load("heelp.png") #load the help image that will be shown when "Heeelp" is pressed



# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (138, 125, 214)
RED = (219, 138, 176)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_GREEN = (144, 238, 144)

#Inverted colours for dark mode
inverted_BLUE = (117, 130, 41)
inverted_LIGHT_BLUE = (82, 39, 25)
inverted_DARK_BLUE = (255, 255, 116)
inverted_LIGHT_GREEN = (111, 17, 111)
inverted_RED = (36, 117, 79)
DARK_GREY = (31, 31, 31)

is_dark_mode = False

# Define grid parameters
NUM_ROWS = 3
NUM_COLS = 9
GRID_WIDTH = 40
GRID_HEIGHT = 40
GRID_MARGIN = 0  # principaa tas grid margin taalaak kodaa nav vajadziigs lmao

# difficulty and time
start_time = time.time()
difficulty_level = "easy"

# Define the initial grid
original_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 1, 1, 2, 1, 3, 1, 4, 1],
    [5, 1, 6, 1, 7, 1, 8, 1, 9],
]

adjacency_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 1, 1, 2, 1, 3, 1, 4, 1],
    [5, 1, 6, 1, 7, 1, 8, 1, 9],
]

class Button:
    def __init__(
        self,
        text,
        position,
        action,
        color=(0, 128, 255),
        size=(90, 30),
    ):
        self.text = text
        self.position = position
        self.action = action
        self.font = pygame.font.Font(None, 24)
        self.rect = pygame.Rect(self.position[0], self.position[1], 100, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK if is_dark_mode else LIGHT_BLUE, self.rect)
        pygame.draw.rect(screen, inverted_BLUE if is_dark_mode else BLUE, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE if is_dark_mode else BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        button_surface = pygame.Surface((100, 30))
        button_surface.fill(inverted_BLUE if is_dark_mode else BLUE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                 print("esmu eventhandlerii button klasē") 
                 self.action()


# Define variables to keep track of selected & hint cells & what moves have been made
selected_cells = []
hint_cells=[]
moves=[]
history=[]


def _hand_drawn_horizontal_line(left, top, width, height, line_index, num_lines):
    """One continuous horizontal wavy line (hand-drawn, mostly straight)."""
    t0 = (line_index + 1) / (num_lines + 2)
    y_base = top + height * t0
    points = []
    n = 14
    for i in range(n + 1):
        x = left + width * (i / n)
        wobble = height * 0.02 * math.sin(line_index * 1.5 + i * 0.7) + height * 0.01 * math.sin(i * 1.9 + line_index)
        y = y_base + wobble
        points.append((x, y))
    return points


def draw_erased_scribbles(surface, left, top, width, height, color, line_width=2):
    """Hand-drawn horizontal scribbles: continuous wavy lines, not too dense."""
    num_lines = 9
    for i in range(num_lines):
        pts = _hand_drawn_horizontal_line(left, top, width, height, i, num_lines)
        pygame.draw.lines(surface, color, False, pts, line_width)


def draw_grid(original_grid, adjacency_grid, elapsed_time): #ze draewing funcshen
    # Draw grid cells (use min row length so playback with variable-length rows is safe)
    for row in range(len(original_grid)):
        if row >= len(adjacency_grid):
            break
        num_cols = min(len(original_grid[row]), len(adjacency_grid[row]))
        for col in range(num_cols):
            cell_color = DARK_GREY if is_dark_mode else WHITE
            is_erased = adjacency_grid[row][col] == 0
            if is_erased:
                cell_color = WHITE if not is_dark_mode else DARK_GREY
            elif (row, col) in selected_cells:
                cell_color = inverted_LIGHT_BLUE if is_dark_mode else LIGHT_BLUE
            elif (row, col) in hint_cells and elapsed_time < 3:
                cell_color = inverted_LIGHT_GREEN if is_dark_mode else LIGHT_GREEN
            cell_left = col * GRID_WIDTH + GRID_WIDTH
            cell_top = row * GRID_HEIGHT + GRID_HEIGHT
            pygame.draw.rect(
                window,
                cell_color,
                [cell_left, cell_top, GRID_WIDTH, GRID_HEIGHT],
            )
            font = pygame.font.Font(None, 40)
            text = font.render(str(original_grid[row][col]), True, WHITE if is_dark_mode else BLACK)
            text_rect = text.get_rect(
                center=(cell_left + GRID_WIDTH / 2, cell_top + GRID_HEIGHT / 2))
            window.blit(text, text_rect)
            if is_erased:
                scribble_color = (80, 70, 90) if not is_dark_mode else (180, 175, 165)
                draw_erased_scribbles(window, cell_left, cell_top, GRID_WIDTH, GRID_HEIGHT, scribble_color, 2)

    # Draw horizontal lines
    for row in range(WINDOW_HEIGHT // GRID_HEIGHT + 1):
        pygame.draw.line(
            window,
            inverted_BLUE if is_dark_mode else BLUE,
            (GRID_MARGIN, GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)),            (
                WINDOW_WIDTH - GRID_MARGIN,
                GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)),
            2,
        )

    # Draw vertical lines
    
    for col in range(WINDOW_WIDTH // GRID_WIDTH):
        pygame.draw.line(
            window,
            inverted_BLUE if is_dark_mode else BLUE,
            (GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN), GRID_MARGIN),
            (
                GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN),
                WINDOW_HEIGHT - GRID_MARGIN,
            ),
            2,
        )
    
    # Draw the red line that notebooks have
    pygame.draw.rect(
        window, inverted_RED if is_dark_mode else RED, [WINDOW_WIDTH - 150, 0, 2, WINDOW_HEIGHT]
    )  # notebook red line


def handle_mouse_events(original_grid, adjacency_grid, button_actions):  # I think this function might handle mouse events
    global selected_cells
    global turns
    global moves
    global history
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                x=x - GRID_WIDTH #these adjustments are because of *1* reference
                y=y -GRID_HEIGHT
                col = x // GRID_WIDTH 
                print("Clicked column:", col)  # Print clicked column to console
                row = y // GRID_HEIGHT
                print("Clicked row:", row)  # Print clicked row to console
                # print ("num rows", NUM_ROWS, " un num cols", NUM_COLS)
                for button, action in button_actions.items():
                    if button.rect.collidepoint(event.pos):  # Check if mouse click is inside the button
                        print("Button clicked!", button.text)
                        action()
                if (row < 0 or row >= len(adjacency_grid) or col < 0 or col >= len(adjacency_grid[row])):
                    print("out of boundz")
                    selected_cells = []
                    return

                if (adjacency_grid[row][col] == 0):  # check that you don't pick an already erased number
                    display_dialog(window, "Number already removed!", type="ok")
                    selected_cells = []

                elif 0 <= row < len(original_grid) and 0 <= col < len(adjacency_grid[row]):
                    cell_pos = (row, col)
                    print("cell_pos", cell_pos)
                    if len(selected_cells) < 2:
                        if cell_pos in selected_cells:
                            selected_cells.remove(cell_pos)
                        else:
                            selected_cells.append(cell_pos)
                            print(selected_cells)
                    if len(selected_cells) == 2:
                        # Save state before applying a matching move so we can undo
                        history.append(copy.deepcopy((original_grid, adjacency_grid, moves, turns)))
                        # Compare numbers in the selected cells
                        row1, col1 = selected_cells[0]
                        row2, col2 = selected_cells[1]
                        num1 = original_grid[row1][col1]
                        num2 = original_grid[row2][col2]
                        if matching(adjacency_grid, selected_cells) == True:
                            print("Numbers match!")
                            moves.append([[row1, col1], [row2, col2]])
                            # Change the color of matched cells to DARK_BLUE and update adjacency grid to 0s
                            adjacency_grid[row1][col1] = 0
                            adjacency_grid[row2][col2] = 0
                            selected_cells = []
                            print("adjacency grid", adjacency_grid)
                            print("original grid", original_grid)
                            print("moves, ", moves)
                        else:
                            selected_cells = []


def matching(adjacency_grid, selected_cells):  # laiks sapārot ciparus
    row1, col1 = selected_cells[0]
    row2, col2 = selected_cells[1]
    num1 = adjacency_grid[row1][col1]
    num2 = adjacency_grid[row2][col2]
    if num1 == num2 or (num1 + num2 == 10):
        if (
            is_adjacent(adjacency_grid, row1, col1, row2, col2) == True
        ):  # ja ir summaa 10, vai blakām vienādi, viss ok
            return True
        else:
            print("Numbers are not adjacent!")
            display_dialog(window, "Numbers are not adjacent!", type="ok")
            selected_cells = []

    else:
        print("Numbers do not match!")
        display_dialog(window, "Numbers do not match!", type="ok")
        selected_cells = []


def is_adjacent(adjacency_grid, row1, col1, row2, col2):  # mēģinām izpīpēt vai cipari atrodas blakām
    print(adjacency_grid)
    print("veertiibas", row1, col1, row2, col2)
    if row1 == row2:
        # Check if there are only zeros between num1 and num2 in the same row
        start_col, end_col = min(col1, col2), max(col1, col2)
        return all(
            adjacency_grid[row1][col] == 0 for col in range(start_col + 1, end_col)
        )  # ja ir tikai nulles, true, ja nav, false
    elif col1 == col2:
        # Check if there are only zeros between num1 and num2 in the same column
        start_row, end_row = min(row1, row2), max(row1, row2)
        return all(
            adjacency_grid[row][col1] == 0 for row in range(start_row + 1, end_row)
        )  # same
    else:  # if neither rows nor columns are equal we need to check if there are only 0s between 2 elements
        start_row = 0
        end_row = len(adjacency_grid)
        start_col = 0
        end_col = 8
        small_row = min(row2, row1)
        big_row = max(row1, row2)
        if small_row == row2:
            small_col = col2
            big_col = col1
        else:
            small_col = col1
            big_col = col2
            print("small row", small_row, "smallcol", small_col)
        if (
            all(
                adjacency_grid[small_row][small_col + 1] == 0
                for col in range(small_col + 1, end_col)
            )
            == True
            or small_col == end_col
        ):
            # if all the numbers in the current starting row after the picked number are 0s, we can start checking if
            # the numbers in subsequent rows until we reach the row with number 2 are also filled with 0s. If not, False.
            # OR - maybe its the last element in the row, no need to check for 0s before moving on
            print("esmu iekshaa")
            for cur_row in range(
                small_row + 1, big_row + 1
            ):  # +1 because we already checked small row just now
                if cur_row == big_row and (
                    all(
                        adjacency_grid[cur_row][start_col] == 0
                        for col in range(start_col, big_col)
                    )
                    == True
                    or big_col == 0
                ):
                    print("cur row", cur_row, "big_row", big_row, "big_col", big_col)
                    return True  # if you have reached the last row, check if either it is the first element, or it only has 0s leading up to it

                elif (
                    all(
                        adjacency_grid[cur_row][start_col] == 0
                        for col in range(start_col, end_col)
                    )
                    == True
                ):  # if its not the last row, check if it only
                    cur_row = (
                        cur_row + 1
                    )  # if it contains only 0s, move to the next row                           #contains zeros
                else:
                    return False
        else:
            return False


def redraw_board(original_grid, adjacency_grid):  # collect non-zeros, place starting after last cell (extend current row or append new rows)
    global turns
    global moves
    global history
    history.append(copy.deepcopy((original_grid, adjacency_grid, moves, turns)))
    moves.append({"action": "redraw"})
    turns = turns + 1
    print("turn No. ", turns)
    append_list = []
    for row in adjacency_grid:
        for element in row:
            if element != 0:
                append_list.append(element)
    # Start after the last cell in the grid so we extend the current row if it has < 9 elements
    i = len(adjacency_grid) - 1
    j = len(adjacency_grid[-1]) - 1
    for element in append_list:
        j = j + 1
        if j >= 9:
            j = 0
            i = i + 1
            if i >= WINDOW_HEIGHT / GRID_HEIGHT:
                display_dialog(window, "Game over!", type="ok")
                new_game_board(original_grid, adjacency_grid, choice=True)
                return False
            original_grid.append([])
            adjacency_grid.append([])
        adjacency_grid[i].append(element)
        original_grid[i].append(element)

def new_game_board(original_grid, adjacency_grid, choice): #restart the game
     global turns
     global hint_cells
     global moves
     global history
     hint_cells=[]
     if choice == False:
        choice = display_dialog(window, "New game? Sure?", type="yes_no")
        #print("choice", choice)
     if choice == True:
            original_grid.clear()
            adjacency_grid.clear()
            rows = [[1, 2, 3, 4, 5, 6, 7, 8, 9],[1, 1, 1, 2, 1, 3, 1, 4, 1],[5, 1, 6, 1, 7, 1, 8, 1, 9],]
            for row in rows:
                original_grid.append(row.copy())  # Make a copy of the row otherwise modifications in adjacency grid will affect original grid as well because why the fuck not
                adjacency_grid.append(row.copy())
            print (len(original_grid), "garums original grid")
            print (len(adjacency_grid), "garums adjacency grid")
            turns=0
            moves=[]
            history=[]
            #draw_grid(grid, adjacency_grid)
            

     elif choice == False:
            print("pressed no")

def hint_find(adjacency_grid): #what happens when you press the hint button 
    global hint_cells
    hint_cells=[]
    hint_found=False
        
    for i, row in enumerate(adjacency_grid):
         for j, element in enumerate(row):
             print("i j element",i, j, element, "row len", len(row))
             if adjacency_grid[i][j] != 0:
                 if find_matches(adjacency_grid, i, j, hint_cells) != False: #if a match was found, we're done
                     hint_found=True
                     break
         if hint_found:
            break
    if hint_found==False:
       return False
    else:
       print("hint cells",hint_cells)
       return True

def find_matches(adjacency_grid, i, j, hint_cells): #looking for adjacent cells and verifying if they match, if yes, adding to hint_cells[]
    search_done=False
    found_match=False        
    #look for an element to the left
    x=i
    y=j
    while search_done==False:
        if i==0 and j==0: #we stop at the very first element when going to the left, that's as far as you can go
            search_done=True
        else:
           if j == 0:  #if we are not at the first element, there is something to the left. First, we check if we are at the first element of a row
               j=len(adjacency_grid[i-1])-1  #if we are, move to a row above and to the end of it
               i=i-1
           else: #if we are anywhere else, move to the left
               j=j-1 
           if adjacency_grid[i][j] != 0: #check if the element is valid
             if adjacency_grid[i][j] == adjacency_grid[x][y] or adjacency_grid[i][j] + adjacency_grid[x][y] == 10:
                  print("left match found", i, j)
                  cell_pos = (i, j)
                  hint_cells.append(cell_pos)
                  cell_pos = (x, y)
                  hint_cells.append(cell_pos)
                  found_match=True
             search_done=True  #regardless of whether it matches, the search for a valid neighbour is done, search has to stop
                
    if found_match==False: #if there is no match found, we need to check 2 remaining directions
        search_done=False #neighbour might've been found, but it wasn't a match
        i=x
        j=y
    else:
        return hint_cells    
    #look for an element to the right
    while search_done==False:
        if i==len(adjacency_grid)-1 and j==len(adjacency_grid[i])-1: #last element of the last row
            search_done=True
        else: #if it is anything else, we can look for adjacent cells to the right
            if j == len(adjacency_grid[i])-1 and i<len(adjacency_grid)-1:  #last element of a row, move to the next row
               j=0 
               i=i+1
            else:
               j=j+1 #move to the right
            if adjacency_grid[i][j] != 0: #check if the element is valid
                if adjacency_grid[i][j] == adjacency_grid[x][y] or adjacency_grid[i][j] + adjacency_grid[x][y] == 10:
                   print("right match found", i, j)
                   cell_pos = (i, j)
                   hint_cells.append(cell_pos)
                   cell_pos = (x, y)
                   hint_cells.append(cell_pos)
                   found_match=True
                search_done=True
                   
    if found_match==False: #if there is no match found, we need to check 2 remaining directions
        search_done=False
        i=x
        j=y
    else:
        return hint_cells    
    
    #look for an element below
    while search_done==False:
        if i==len(adjacency_grid)-1: #last row
            search_done=True
        else:
            if i==len(adjacency_grid)-2: #if second last row we need to check if there is an element below
               if j < len(adjacency_grid[i+1]): #last row can have less than 9 elements
                 i=i+1
               else:
                 search_done=True
                 break
            else:
                i=i+1 #move a row below for every other row above last 2
                
            if adjacency_grid[i][j] != 0: #check if the element is valid
                if adjacency_grid[i][j] == adjacency_grid[x][y] or adjacency_grid[i][j] + adjacency_grid[x][y] == 10: #matching
                   print("below match found", i, j)
                   cell_pos = (i, j)
                   hint_cells.append(cell_pos)
                   cell_pos = (x, y)
                   hint_cells.append(cell_pos)
                   found_match=True
                search_done=True
    if found_match==False: #if there is no match found, we need to check last remaining direction
        return False
    else:
        return hint_cells    
    
    #look for an element above (not actually necessary right now so commented out, might be necessary later if you want to check an arbitrary number for matches)
    '''
    while search_done==False:
        if i==0: #first row
            search_done=True
        else:
             i=i-1 #move a row below for every other row above last   
             if adjacency_grid[i][j] != 0: #check if the element is valid
                if adjacency_grid[i][j] == adjacency_grid[x][y] or adjacency_grid[i][j] + adjacency_grid[x][y] == 10: #matching
                   print("above match found", i, j)
                   cell_pos = (i, j)
                   hint_cells.append(cell_pos)
                   cell_pos = (x, y)
                   hint_cells.append(cell_pos)
                   found_match=True
                search_done=True
    '''
       
                 
def display_dialog(window, message, type="ok"):  # the informative display dialogues (and the yes/no one as well)

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE if is_dark_mode else BLACK)
    text_rect = text.get_rect()
    min_w = max(400, text_rect.width + 80)
    min_h = max(200, text_rect.height + 100)
    dialog_rect = pygame.Rect(100, 100, min_w, min_h)

    text_x, text_y = dialog_rect.center
    text_rect = text.get_rect(center=(text_x, text_y - 25))
    button_center_x = dialog_rect.centerx
    button_y = dialog_rect.centery + 50

    if type == "ok":

        pygame.draw.rect(window, inverted_LIGHT_BLUE if is_dark_mode else LIGHT_BLUE, dialog_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, dialog_rect, 2)

        button_rect = pygame.Rect(0, 0, 120, 50)
        button_rect.center = (button_center_x, button_y)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, button_rect)
        pygame.draw.rect(window, BLACK if is_dark_mode else WHITE, button_rect, 2)

        # Render and draw button text
        button_text = font.render("OK", True, BLACK if is_dark_mode else WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        window.blit(button_text, button_text_rect)
    elif type == "yes_no":
        pygame.draw.rect(window, BLACK if is_dark_mode else WHITE, dialog_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, dialog_rect, 2)

        # Render "Yes" button
        yes_button = Button("Yes",(150, 150),action=lambda: print("Yes button clicked"))
        yes_button.rect.center = (button_center_x - 75, button_y)
        # print("yes button", yes_button(button_type))
        no_button = Button("No",(250, 150),action=lambda: print("No button clicked"))
        no_button.rect.center = (button_center_x + 75, button_y)

        yes_button.draw(window)
        no_button.draw(window)

    window.blit(text, text_rect)

    pygame.display.update()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if type == "ok" and button_rect.collidepoint(x, y):
                  print("OK button clicked")
                  waiting = False  # Exit the loop only if the OK button is clicked
                  return False
                elif type == "yes_no":
                  if yes_button.rect.collidepoint(x, y):
                    print("Yes button clicked")
                    waiting = False  # Exit the loop if the Yes button is clicked
                    return True
                  elif no_button.rect.collidepoint(x, y):
                    print("No button clicked")
                    waiting = False  # Exit the loop if the No button is clicked
                    return False

def _normalize_scores(scores):
    """Convert legacy list-of-ints to list of {turns, moves, initials}."""
    out = []
    for s in scores:
        if isinstance(s, int):
            out.append({"turns": s, "moves": [], "initials": "---"})
        else:
            out.append({
                "turns": s.get("turns", 0),
                "moves": s.get("moves", []),
                "initials": s.get("initials", "---")[:3].upper() or "---",
            })
    return out


def _count_moves_and_redraws(moves_list):
    """One move = one pair removal or one redraw. Returns (move_count, redraw_count)."""
    if not moves_list:
        return 0, 0
    moves_count = 0
    redraws_count = 0
    for m in moves_list:
        if isinstance(m, dict) and m.get("action") == "redraw":
            moves_count += 1
            redraws_count += 1
        elif isinstance(m, list) and len(m) == 2 and isinstance(m[0], (list, tuple)) and len(m[0]) == 2:
            moves_count += 1
    return moves_count, redraws_count


def _get_move_count(entry):
    """For ordering: use move count from moves list; entries with no moves (old BOT-like) get 200."""
    moves = entry.get("moves", [])
    if not moves:
        return 200
    return _count_moves_and_redraws(moves)[0]


def save_score(turns, moves_list, initials=""):  # saves top 10 by move count
    initials = (initials or "---")[:3].upper() or "---"
    try:
        with open('scores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []
    scores = _normalize_scores(scores)
    scores.append({"turns": turns, "moves": moves_list, "initials": initials})
    scores.sort(key=_get_move_count)
    scores = scores[:10]
    with open('scores.json', 'w') as f:
        json.dump(scores, f, indent=2)


def save_moves_record(turns, moves_list, initials, difficulty_level):
    """Append full move history for a finished game into moves.json."""
    record = {
        "turns": turns,
        "initials": (initials or "---")[:3].upper() or "---",
        "difficulty": difficulty_level,
        "moves": moves_list,
    }
    try:
        with open('moves.json', 'r') as f:
            all_records = json.load(f)
    except FileNotFoundError:
        all_records = []
    if not isinstance(all_records, list):
        all_records = []
    all_records.append(record)
    # Keep only the 10 best (lowest move count) replays
    all_records.sort(key=lambda r: _count_moves_and_redraws(r.get("moves", []))[0] if r.get("moves") else r.get("turns", 999999))
    all_records = all_records[:10]
    with open('moves.json', 'w') as f:
        json.dump(all_records, f, indent=2)

def load_scores():  # returns list of {"turns": n, "moves": [...]}
    try:
        with open('scores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []
    return _normalize_scores(scores)


def display_initials_prompt(window):
    """Prompt for 3-letter initials; returns string of up to 3 chars (uppercase)."""
    buf = []
    font = pygame.font.Font(None, 36)
    dialog_rect = pygame.Rect(150, 280, 340, 140)
    ok_rect = pygame.Rect(dialog_rect.centerx - 45, dialog_rect.bottom - 50, 90, 36)
    text_color = WHITE if is_dark_mode else BLACK

    def draw():
        pygame.draw.rect(window, inverted_LIGHT_BLUE if is_dark_mode else LIGHT_BLUE, dialog_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, dialog_rect, 2)
        prompt = font.render("Enter initials (3 letters):", True, text_color)
        window.blit(prompt, (dialog_rect.x + 20, dialog_rect.y + 18))
        display_str = "".join(buf).ljust(3, "_")
        cur_text = font.render(display_str, True, text_color)
        window.blit(cur_text, (dialog_rect.x + 20, dialog_rect.y + 52))
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, ok_rect)
        pygame.draw.rect(window, BLACK if is_dark_mode else WHITE, ok_rect, 2)
        ok_label = font.render("OK", True, text_color)
        window.blit(ok_label, ok_label.get_rect(center=ok_rect.center))
        pygame.display.update()

    draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return "".join(buf)[:3].upper() or "---"
                if event.key == pygame.K_BACKSPACE:
                    if buf:
                        buf.pop()
                        draw()
                elif event.unicode and len(buf) < 3 and event.unicode.isalpha():
                    buf.append(event.unicode.upper())
                    draw()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ok_rect.collidepoint(event.pos):
                    return "".join(buf)[:3].upper() or "---"


def display_scores(window):
    scores = load_scores()
    scores.sort(key=_get_move_count)
    first_ten = scores[:10]
    while len(first_ten) < 10:
        first_ten.append({"turns": 200, "moves": [], "initials": "BOT"})
    num_scores = len(first_ten)
    row_h = 32
    header_h = 52
    margin_left = 14
    notebook_margin = 8
    box_w = 380
    box_h = header_h + num_scores * row_h + 50
    box_x = 60
    box_y = 70
    text_color = WHITE if is_dark_mode else BLACK
    paper = (252, 248, 240) if not is_dark_mode else (45, 42, 38)
    line_color = (200, 190, 180) if not is_dark_mode else (70, 68, 65)
    red_line = (200, 60, 60) if not is_dark_mode else (180, 80, 80)

    pygame.draw.rect(window, paper, (box_x, box_y, box_w, box_h))
    pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, (box_x, box_y, box_w, box_h), 2)
    pygame.draw.rect(window, red_line, (box_x + notebook_margin, box_y, 3, box_h))
    for r in range(1, num_scores + 1):
        y = box_y + header_h + r * row_h
        pygame.draw.line(window, line_color, (box_x + margin_left, y), (box_x + box_w - 10, y), 1)

    font = pygame.font.Font(None, 24)
    font_header = pygame.font.Font(None, 26)
    header = font_header.render("Scoreboard", True, text_color)
    window.blit(header, (box_x + margin_left + 18, box_y + 6))
    col_place = box_x + margin_left + 18
    col_initials = box_x + margin_left + 58
    col_moves = box_x + margin_left + 130
    col_redraws = box_x + margin_left + 200
    font_small = pygame.font.Font(None, 20)
    window.blit(font_small.render("#", True, text_color), (col_place, box_y + 30))
    window.blit(font_small.render("Initials", True, text_color), (col_initials, box_y + 30))
    window.blit(font_small.render("Moves", True, text_color), (col_moves, box_y + 30))
    window.blit(font_small.render("Redraws", True, text_color), (col_redraws, box_y + 30))
    for i, entry in enumerate(first_ten):
        y = box_y + header_h + i * row_h + 6
        place_text = font.render(f"#{i + 1}", True, text_color)
        initials = entry.get("initials", "---")
        if initials == "---" or not initials:
            initials = "BOT"
        initials_text = font.render(initials, True, text_color)
        moves_list = entry.get("moves", [])
        # Placeholder / legacy entries with no moves: show 200/200 so they sit below real scores
        if not moves_list:
            move_count, redraw_count = 200, 200
        else:
            move_count, redraw_count = _count_moves_and_redraws(moves_list)
        moves_text = font.render(str(move_count), True, text_color)
        redraws_text = font.render(str(redraw_count), True, text_color)
        window.blit(place_text, (col_place, y))
        window.blit(initials_text, (col_initials, y))
        window.blit(moves_text, (col_moves, y))
        window.blit(redraws_text, (col_redraws, y))
    close_rect = pygame.Rect(box_x + box_w - 90, box_y + box_h - 38, 80, 28)
    pygame.draw.rect(window, BLACK if is_dark_mode else LIGHT_BLUE, close_rect)
    pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, close_rect, 2)
    close_label = font.render("Close", True, WHITE if is_dark_mode else BLACK)
    window.blit(close_label, close_label.get_rect(center=close_rect.center))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_rect.collidepoint(event.pos):
                    waiting = False


def display_playback_menu(window, records):
    """Let the user pick a replay from moves.json."""
    if not records:
        display_dialog(window, "No replays available!", type="ok")
        return None
    # Sort by best move count first
    records = sorted(records, key=lambda r: _count_moves_and_redraws(r.get("moves", []))[0] if r.get("moves") else r.get("turns", 999999))
    num = len(records)
    row_h = 32
    header_h = 44
    margin_left = 14
    box_w = 420
    box_h = header_h + num * row_h + 60
    box_x = 40
    box_y = 120
    text_color = WHITE if is_dark_mode else BLACK
    paper = (252, 248, 240) if not is_dark_mode else (45, 42, 38)

    font = pygame.font.Font(None, 22)
    font_header = pygame.font.Font(None, 24)

    def draw_menu():
        # Draw overlay panel
        pygame.draw.rect(window, paper, (box_x, box_y, box_w, box_h))
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, (box_x, box_y, box_w, box_h), 2)
        header = font_header.render("Playback – click a game to replay", True, text_color)
        window.blit(header, (box_x + margin_left, box_y + 8))
        col_hash = box_x + margin_left
        col_init = box_x + margin_left + 40
        col_mode = box_x + margin_left + 120
        col_turns = box_x + margin_left + 220
        head_y = box_y + header_h - 18
        window.blit(font.render("#", True, text_color), (col_hash, head_y))
        window.blit(font.render("Initials", True, text_color), (col_init, head_y))
        window.blit(font.render("Mode", True, text_color), (col_mode, head_y))
        window.blit(font.render("Turns", True, text_color), (col_turns, head_y))
        row_rects = []
        for i, rec in enumerate(records):
            y = box_y + header_h + i * row_h + 4
            window.blit(font.render(f"{i+1}", True, text_color), (col_hash, y))
            window.blit(font.render(rec.get("initials", "---"), True, text_color), (col_init, y))
            window.blit(font.render(rec.get("difficulty", "?"), True, text_color), (col_mode, y))
            window.blit(font.render(str(rec.get("turns", "?")), True, text_color), (col_turns, y))
            row_rects.append(pygame.Rect(box_x, box_y + header_h + i * row_h, box_w, row_h))
        close_rect = pygame.Rect(box_x + box_w - 90, box_y + box_h - 38, 80, 28)
        pygame.draw.rect(window, BLACK if is_dark_mode else LIGHT_BLUE, close_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, close_rect, 2)
        close_label = font.render("Close", True, WHITE if is_dark_mode else BLACK)
        window.blit(close_label, close_label.get_rect(center=close_rect.center))
        pygame.display.update()
        return row_rects, close_rect

    row_rects, close_rect = draw_menu()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_rect.collidepoint(event.pos):
                    return None
                for idx, rect in enumerate(row_rects):
                    if rect.collidepoint(event.pos):
                        return records[idx]


def display_help(window):
    window.blit(help_image, (100,100))
    print("Image dimensions:", help_image.get_width(), "x", help_image.get_height())
    pygame.display.update()
    waiting = True 
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False 
def undo_last_action(original_grid, adjacency_grid):
    """Revert the last move/redraw/delete-empty if possible."""
    global moves, turns, history
    if not history:
        display_dialog(window, "Nothing to undo!", type="ok")
        return
    prev_original, prev_adjacency, prev_moves, prev_turns = history.pop()
    # Deepcopy to avoid aliasing issues across undos
    original_grid.clear()
    adjacency_grid.clear()
    for row in prev_original:
        original_grid.append(list(row))
    for row in prev_adjacency:
        adjacency_grid.append(list(row))
    moves = prev_moves
    turns = prev_turns


def playback_record(window, record):
    """Replay a single game record from moves.json."""
    # Fresh playback grids (do not touch live game state)
    rows = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 1, 1, 2, 1, 3, 1, 4, 1],
        [5, 1, 6, 1, 7, 1, 8, 1, 9],
    ]
    pb_original = [row.copy() for row in rows]
    pb_adjacency = [row.copy() for row in rows]

    def playback_redraw(adj_grid, orig_grid):
        """Match game: collect non-zeros, place after last cell (extend current row or append new rows). Zero cells unchanged."""
        append_list = []
        for row in adj_grid:
            for element in row:
                if element != 0:
                    append_list.append(element)
        new_adj = [list(row) for row in adj_grid]
        new_orig = [list(row) for row in orig_grid]
        i = len(new_adj) - 1
        j = len(new_adj[-1]) - 1
        for val in append_list:
            j = j + 1
            if j >= 9:
                j = 0
                i = i + 1
                new_adj.append([])
                new_orig.append([])  # new list so pair-removal does not zero pb_original
            new_adj[i].append(val)
            new_orig[i].append(val)
        return new_adj, new_orig

    def playback_delete_empty(adj_grid, orig_grid):
        # Remove fully empty rows from both grids
        new_adj = []
        new_orig = []
        for a_row, o_row in zip(adj_grid, orig_grid):
            if all(col == 0 for col in a_row):
                continue
            new_adj.append(a_row)
            new_orig.append(o_row)
        return new_adj, new_orig

    paused = False
    clock = pygame.time.Clock()
    pause_rect = pygame.Rect(WINDOW_WIDTH - 125, 50, 100, 30)
    exit_rect = pygame.Rect(WINDOW_WIDTH - 125, 90, 100, 30)
    font_btn = pygame.font.Font(None, 24)
    text_color = WHITE if is_dark_mode else BLACK

    def draw_playback_frame():
        window.fill(DARK_GREY if is_dark_mode else WHITE)
        draw_grid(pb_original, pb_adjacency, 0)
        label = "Resume" if paused else "Pause"
        pygame.draw.rect(window, BLACK if is_dark_mode else LIGHT_BLUE, pause_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, pause_rect, 2)
        window.blit(font_btn.render(label, True, WHITE if is_dark_mode else BLACK), font_btn.render(label, True, WHITE if is_dark_mode else BLACK).get_rect(center=pause_rect.center))
        pygame.draw.rect(window, BLACK if is_dark_mode else LIGHT_BLUE, exit_rect)
        pygame.draw.rect(window, inverted_BLUE if is_dark_mode else BLUE, exit_rect, 2)
        window.blit(font_btn.render("Exit", True, WHITE if is_dark_mode else BLACK), font_btn.render("Exit", True, WHITE if is_dark_mode else BLACK).get_rect(center=exit_rect.center))
        pygame.display.flip()

    for move in record.get("moves", []):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and exit_rect.collidepoint(event.pos):
                return
        if isinstance(move, dict) and "action" in move:
            action = move["action"]
            if action == "redraw":
                pb_adjacency, pb_original = playback_redraw(pb_adjacency, pb_original)
            elif action == "delete_empty_row":
                pb_adjacency, pb_original = playback_delete_empty(pb_adjacency, pb_original)
        else:
            try:
                (r1, c1), (r2, c2) = move
                # Only zero adjacency (like the game); keep original so erased cells still show number + scribbles
                if 0 <= r1 < len(pb_adjacency) and 0 <= c1 < len(pb_adjacency[r1]):
                    pb_adjacency[r1][c1] = 0
                if 0 <= r2 < len(pb_adjacency) and 0 <= c2 < len(pb_adjacency[r2]):
                    pb_adjacency[r2][c2] = 0
            except Exception:
                pass

        draw_playback_frame()
        elapsed = 0
        while elapsed < 1000:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_rect.collidepoint(event.pos):
                        return
                    if pause_rect.collidepoint(event.pos):
                        paused = not paused
            if paused:
                draw_playback_frame()
                continue
            elapsed += dt
            draw_playback_frame()


def endgame_check(adjacency_grid, difficulty_level, turns, button_actions): #has the game ended?
    global moves
    if sum(element for row in adjacency_grid for element in row) == 0:
      print("Wow, he finished!")
      moves_copy = list(moves)
      moves = []
      message = f"Congratulations, you finished in {turns} turns"
      # First show the fully erased board (including last crossed-out pair)
      window.fill(DARK_GREY if is_dark_mode else WHITE)
      draw_grid(original_grid, adjacency_grid, 0)
      for button in button_actions:  # redraw buttons
            button.draw(window)
      pygame.display.flip()
      display_dialog(window, message, type="ok")
      pygame.display.update()
      initials = display_initials_prompt(window)
      save_score(turns, moves_copy, initials)
      save_moves_record(turns, moves_copy, initials, difficulty_level)
      display_scores(window)
      if difficulty_level == "easy" and turns==1:
        display_dialog(window, "Congratulations, you beat easy mode!", type="ok")
        pygame.display.update()
        display_dialog(window, "Try hard mode now!", type="ok")

      window.fill(DARK_GREY if is_dark_mode else WHITE)
      draw_grid(original_grid, adjacency_grid, 0)
      for button in button_actions: #draw ZE BUTTONZ
            button.draw(window)
      pygame.display.flip()
      turns=0
      new_game_board(original_grid, adjacency_grid, choice=True)
      


def main():
    # Create initial grid
    grid = original_grid
    clock = pygame.time.Clock()
    global start_time
    global turns
    turns=0
            
    def redrawbutton_action():
        #print("redraw Button clicked with difficulty", difficulty_level)
        if difficulty_level == "hard":
            if hint_find(adjacency_grid) == False:
                redraw_board(original_grid, adjacency_grid)
            else:
                display_dialog(window, "More matches possible!", type="ok")
        elif difficulty_level == "easy":
            redraw_board(original_grid, adjacency_grid)
                            
    def hintbutton_action():
        global start_time
        if hint_find(adjacency_grid) == False:
            display_dialog(window, "No matches remaining!", type="ok")
        start_time = time.time()

    def newbutton_action():
        new_game_board(original_grid, adjacency_grid, choice=False)
        print("aarpusfunkcijas original grid garums", len(original_grid))
        print(original_grid)
       

    def modebutton_action():
        print("Mode Button clicked!")
        global difficulty_level
        # Don't allow changing mode mid-game
        if hint_cells != [] or adjacency_grid != original_grid:
            display_dialog(window, "Game already started", type="ok")
        else:
            difficulty_level = "hard" if difficulty_level == "easy" else "easy"
    
    def dark_mode_action():
        print("darkmode Button clicked!")
        global is_dark_mode
        is_dark_mode = not is_dark_mode
    
    def scorebutton_action():
        display_scores(window)
        
    def helpbutton_action():
        display_help(window)
                
    def playbackbutton_action():
        try:
            with open('moves.json', 'r') as f:
                records = json.load(f)
        except FileNotFoundError:
            records = []
        if not isinstance(records, list) or not records:
            display_dialog(window, "No replays available!", type="ok")
            return
        choice = display_playback_menu(window, records)
        if choice is not None:
            playback_record(window, choice)
            # After playback, redraw current game state
            window.fill(DARK_GREY if is_dark_mode else WHITE)
            draw_grid(original_grid, adjacency_grid, 0)
            for button in button_actions:
                button.draw(window)
            pygame.display.flip()
    def erasebutton_action():
        global turns
        global moves
        global history
        print("erase Button clicked!")
        turns = turns + 1
        rows_to_delete = []  # Store the indices of rows to delete
        for index, row in enumerate(adjacency_grid):
            if all(col == 0 for col in row):
                rows_to_delete.append(index)
        if rows_to_delete == []:
           display_dialog(window, "There are no empty rows!", type="ok")
        else:
          history.append(copy.deepcopy((original_grid, adjacency_grid, moves, turns)))
          moves.append({"action": "delete_empty_row"})
          # Delete rows from adjacency_grid and original_grid
          for index in reversed(rows_to_delete):
              del adjacency_grid[index]
              del original_grid[index]

    redrawbutton = Button("Redraw", (WINDOW_WIDTH - 125, 40), redrawbutton_action)
    erasebutton = Button("Del empty", (WINDOW_WIDTH - 125, 80), erasebutton_action)
    hintbutton = Button("Hint!", (WINDOW_WIDTH - 125, 120), hintbutton_action)
    undobutton = Button("Undo", (WINDOW_WIDTH - 125, 160), lambda: undo_last_action(original_grid, adjacency_grid))
    
    helpbutton = Button("Heeelp!", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 320), helpbutton_action) 
    newbutton = Button("New game", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 280), newbutton_action)
    modebutton = Button("Mode", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 200), modebutton_action)
    playbackbutton = Button("Playback", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 160), playbackbutton_action)
    scorebutton = Button("Scoreboard", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 120), scorebutton_action)
    dark_modebutton = Button("Dark mode", (WINDOW_WIDTH - 125, WINDOW_HEIGHT - 80), dark_mode_action)
    
    

    # Create font object for permanent text (difficulty level)
    font = pygame.font.Font(None, 24)  # You can change the font and size here

    # Store button-action pairs in a dictionary
    button_actions = {
        redrawbutton: redrawbutton_action,
        modebutton: modebutton_action,
        erasebutton: erasebutton_action,
        newbutton: newbutton_action,
        hintbutton: hintbutton_action,
        undobutton: lambda: undo_last_action(original_grid, adjacency_grid),
        dark_modebutton: dark_mode_action,
        scorebutton: scorebutton_action,
        playbackbutton: playbackbutton_action,
        helpbutton: helpbutton_action
    }
    running = True

    while running:
        elapsed_time = time.time() - start_time
        # Handle events
        
        handle_mouse_events(grid, adjacency_grid, button_actions)
        endgame_check(adjacency_grid, difficulty_level,turns, button_actions)
        
        # Draw everything
        window.fill(DARK_GREY if is_dark_mode else WHITE)
        draw_grid(grid, adjacency_grid, elapsed_time)
        for button in button_actions: #draw ZE BUTTONZ
            button.draw(window)
            
            
        # Render permanent text
        text_content = f"Mode: {difficulty_level}"
        difficulty_text = font.render(text_content, True, WHITE if is_dark_mode else BLACK)  # Render text
        window.blit(
            difficulty_text, (WINDOW_WIDTH - 123, WINDOW_HEIGHT - 235)
        )  # Blit text onto the screen

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
