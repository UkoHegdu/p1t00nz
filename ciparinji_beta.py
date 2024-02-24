import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Skein")

# Set window icon
icon = pygame.image.load('skein_icon.png')
pygame.display.set_icon(icon)


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (138, 125, 214)
RED = (219, 138, 176)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
LIGHT_GREEN = (144, 238, 144)

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
        self.rect = pygame.Rect(self.position[0], self.position[1], 90, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        button_surface = pygame.Surface((90, 30))
        button_surface.fill(BLUE)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                 print("esmu eventhandlerii button klasē") 
                 self.action()


# Define variables to keep track of selected & hint cells
selected_cells = []
hint_cells=[]


def draw_grid(original_grid, adjacency_grid, elapsed_time):
    # Draw grid cells
    NUM_ROWS = len(original_grid)
    #print("hintcells drawgridaa", hint_cells)
    #print("selected cells", selected_cells)
    #print(elapsed_time)
    for row in range(len(original_grid)):
       # print("rindinja", row, len(original_grid))
        for col in range(len(original_grid[row])):
        #    print("kolonna", col)
            cell_color = WHITE
            if adjacency_grid[row][col] == 0:
                cell_color = DARK_BLUE
            elif (row, col) in selected_cells:
                cell_color = LIGHT_BLUE
            elif (row, col) in hint_cells and elapsed_time < 3:
                cell_color = LIGHT_GREEN   
            pygame.draw.rect(
                window,
                cell_color,
                [
                    GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN),
                    GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN),
                    GRID_WIDTH + GRID_MARGIN,
                    GRID_HEIGHT + GRID_MARGIN,
                ],
            )
            font = pygame.font.Font(None, 40)
            text = font.render(str(original_grid[row][col]), True, BLACK)
            text_rect = text.get_rect(
                center=(
                    GRID_MARGIN
                    + col * (GRID_WIDTH + GRID_MARGIN)
                    + (GRID_WIDTH + GRID_MARGIN) / 2,
                    GRID_MARGIN
                    + row * (GRID_HEIGHT + GRID_MARGIN)
                    + (GRID_HEIGHT + GRID_MARGIN) / 2,
                )
            )  # Adjusted to center
            window.blit(text, text_rect)

    # Draw horizontal lines
    for row in range(WINDOW_HEIGHT // GRID_HEIGHT):
        pygame.draw.line(
            window,
            BLUE,
            (GRID_MARGIN, GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)),
            (
                WINDOW_WIDTH - GRID_MARGIN,
                GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN),
            ),
            2,
        )

    # Draw vertical lines
    for col in range(WINDOW_WIDTH // GRID_WIDTH):
        pygame.draw.line(
            window,
            BLUE,
            (GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN), GRID_MARGIN),
            (
                GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN),
                WINDOW_HEIGHT - GRID_MARGIN,
            ),
            2,
        )

    # Draw the red line that notebooks have
    pygame.draw.rect(
        window, RED, [WINDOW_WIDTH - 150, 0, 2, WINDOW_HEIGHT]
    )  # notebook red line


def handle_mouse_events(original_grid, adjacency_grid, button_actions):  # I think this function might handle mouse events
    global selected_cells
    global turns
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                x, y = event.pos
                col = (x - GRID_MARGIN) // (GRID_WIDTH + GRID_MARGIN)
                print("Clicked column:", col)  # Print clicked column to console
                row = (y - GRID_MARGIN) // (GRID_HEIGHT + GRID_MARGIN)
                print("Clicked row:", row)  # Print clicked row to console
                # print ("num rows", NUM_ROWS, " un num cols", NUM_COLS)
                for button, action in button_actions.items():
                    if button.rect.collidepoint(event.pos):  # Check if mouse click is inside the button
                        print("Button clicked!", button.text)
                        action()
                if (col > NUM_COLS - 1 or row > len(adjacency_grid) - 1):  # handle situation if you click outside the numbers
                    print("out of boundz")
                    selected_cells = []
                    return

                if (adjacency_grid[row][col] == 0):  # check that you don't pick an already erased number
                    display_dialog(window, "Number already removed!", type="ok")
                    selected_cells = []

                elif 0 <= row < len(original_grid) and 0 <= col < NUM_COLS:
                    # print("iekaapu sviestaa")
                    cell_pos = (row, col)
                    print("cell_pos", cell_pos)
                    if len(selected_cells) < 2:
                        if cell_pos in selected_cells:
                            selected_cells.remove(cell_pos)
                        else:
                            selected_cells.append(cell_pos)
                            print(selected_cells)
                    if len(selected_cells) == 2:
                        # Compare numbers in the selected cells
                        row1, col1 = selected_cells[0]
                        row2, col2 = selected_cells[1]
                        num1 = original_grid[row1][col1]
                        num2 = original_grid[row2][col2]
                        if matching(adjacency_grid, selected_cells) == True:
                            print("Numbers match!")
                            # Change the color of matched cells to DARK_BLUE and update adjacency grid to 0s
                            adjacency_grid[row1][col1] = 0
                            adjacency_grid[row2][col2] = 0
                            selected_cells = []
                            print("adjacency grid", adjacency_grid)
                            print("original grid", original_grid)
                            if sum(element for row in adjacency_grid for element in row) == 0:
                                print("Wow, you finished!")
                                display_dialog(window, "Congratulations! You finished in ", turns, " turns", type="ok")
                                turns=0
                                #new_game_board(original_grid, adjacency_grid)


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


def redraw_board(original_grid, adjacency_grid):  # add the numbers that are not 0s
    global turns
    append_list = []
    for i, row in enumerate(adjacency_grid):
        for j, element in enumerate(row):
            if element != 0:
                append_list.append(
                    element
                )  # create a list of all the elements we need to add. i and j should point towards the last element
    print(append_list)
    # print (i, j)
    # print ("garums",len(adjacency_grid[i])-1)
    for element in append_list:
        if (
            j == 8
        ):  # if we are looking at the last element of a row, jump to the next one
            # print("esmu ifaa")
            j = -1
            i = i + 1
            original_grid.append(
                []
            )  # need to add new rows otherwise the poor soul is out of range
            adjacency_grid.append([])
        # print(i, j, " ifaa")
        #  print(i, j)
        adjacency_grid[i].append(element)
        original_grid[i].append(element)
        j = j + 1

def new_game_board(original_grid, adjacency_grid):
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
            #draw_grid(grid, adjacency_grid)
            

     elif choice == False:
            print("pressed no")

def hint_find(adjacency_grid):
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
        search_done=False
        i=x
        j=y
    else:
        return hint_cells    
    
    #look for an element above
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
    if found_match==False: #if there is no match found return false
       return False
                 
def display_dialog(window, message, type="ok"):  # koda klucis logam

    # Render text
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    
    # Create rectangle for dialog area
    dialog_rect = pygame.Rect(100, 100, 400, 200)
    
    # Calculate center position for text and buttons
    text_rect = text.get_rect(center=dialog_rect.center)
    button_center_x = dialog_rect.centerx
    button_y = dialog_rect.centery + 50  # Adjust for button height

    if type == "ok":

        pygame.draw.rect(window, LIGHT_BLUE, dialog_rect)
        # Draw button rectangle
        button_rect = pygame.Rect(150, 100, 200, 50)
        button_rect.center = (button_center_x, button_y)
        pygame.draw.rect(window, BLUE, button_rect)
        # Render and draw button text
        button_text = font.render("OK", True, WHITE)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        window.blit(button_text, button_text_rect)
    elif type == "yes_no":
        pygame.draw.rect(window, BLUE, dialog_rect)
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
                  waiting = False  # Exit the loop only if the OK button is clicked
                elif type == "yes_no":
                  if yes_button.rect.collidepoint(x, y):
                    print("Yes button clicked")
                    waiting = False  # Exit the loop if the Yes button is clicked
                    return True
                  elif no_button.rect.collidepoint(x, y):
                    print("No button clicked")
                    waiting = False  # Exit the loop if the No button is clicked
                    return False


def main():
    # Create initial grid
    grid = original_grid
    clock = pygame.time.Clock()
    global start_time
    global turns
    turns=0
            
    def redrawbutton_action():
        global turns
        #print("redraw Button clicked with difficulty", difficulty_level)
        if difficulty_level == "hard":
            if hint_find(adjacency_grid) == False:
                redraw_board(original_grid, adjacency_grid)
                turns=turns+1
                print("turn no. ", turns)
            else:
                display_dialog(window, "More matches possible!", type="ok")
        elif difficulty_level == "easy":
            redraw_board(original_grid, adjacency_grid)
            turns=turns+1
            print("turn no. ", turns)
    
    def hintbutton_action():
        global start_time
        if hint_find(adjacency_grid) == False:
            display_dialog(window, "No matches remaining!", type="ok")
        start_time = time.time()

    def newbutton_action():
        new_game_board(original_grid, adjacency_grid)
        print("aarpusfunkcijas original grid garums", len(original_grid))
        print(original_grid)
       

    def easybutton_action():
        print("easy Button clicked!")
        global difficulty_level
        difficulty_level = "easy"

    def defbutton_action():
        print("defButton clicked!")
        global difficulty_level
        difficulty_level = "hard"

    def erasebutton_action():
        print("erase Button clicked!")
        rows_to_delete = []  # Store the indices of rows to delete
        for index, row in enumerate(adjacency_grid):
            if all(col == 0 for col in row):
                rows_to_delete.append(index)
        if rows_to_delete == []:
           display_dialog(window, "There are no empty rows!", type="ok")
        else:
          # Delete rows from adjacency_grid and original_grid
          for index in reversed(rows_to_delete):
              del adjacency_grid[index]
              del original_grid[index]

    redrawbutton = Button("Redraw", (WINDOW_WIDTH - 120, 40), redrawbutton_action)
    easybutton = Button("Easy", (WINDOW_WIDTH - 120, 180), easybutton_action)
    defbutton = Button("Difficult", (WINDOW_WIDTH - 120, 220), defbutton_action)
    erasebutton = Button("Del empty", (WINDOW_WIDTH - 120, 260), erasebutton_action)
    hintbutton = Button("Hint!", (WINDOW_WIDTH - 120, 300), hintbutton_action)
    newbutton = Button("New game", (WINDOW_WIDTH - 120, 340), newbutton_action)

    # Create font object for permanent text (difficulty level)
    font = pygame.font.Font(None, 24)  # You can change the font and size here

    # Store button-action pairs in a dictionary
    button_actions = {
        redrawbutton: redrawbutton_action,
        easybutton: easybutton_action,
        defbutton: defbutton_action,
        erasebutton: erasebutton_action,
        newbutton: newbutton_action,
        hintbutton: hintbutton_action
    }
    running = True

    while running:
        elapsed_time = time.time() - start_time
        # Handle events
        
        handle_mouse_events(grid, adjacency_grid, button_actions)
        # Draw everything
        window.fill(WHITE)
        draw_grid(grid, adjacency_grid, elapsed_time)
        easybutton.draw(window)
        redrawbutton.draw(window)
        defbutton.draw(window)
        erasebutton.draw(window)
        newbutton.draw(window)
        hintbutton.draw(window)
        # Render permanent text
        text_content = f"Diff: {difficulty_level}"
        difficulty_text = font.render(text_content, True, (0, 0, 0))  # Render text
        window.blit(
            difficulty_text, (WINDOW_WIDTH - 120, 120)
        )  # Blit text onto the screen

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
