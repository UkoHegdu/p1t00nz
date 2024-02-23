import pygame
import copy

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Skein")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (138, 125, 214)
RED = (219, 138, 176)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)

# Define grid parameters
NUM_ROWS = 3
NUM_COLS = 9
GRID_WIDTH = 40
GRID_HEIGHT = 40
GRID_MARGIN = 0  # principaa tas grid margin taalaak kodaa nav vajadziigs lmao

# difficulty
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

kopija = copy.deepcopy(original_grid)


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


# Define variables to keep track of selected cells
selected_cells = []


def draw_grid(original_grid, adjacency_grid):
    # Draw grid cells
    NUM_ROWS = len(original_grid)
    # print("rindaz:", NUM_ROWS)
    # print(len(original_grid))
#    print("kasteiroutofrange",adjacency_grid)
    print("garums",len(original_grid))
    for row in range(len(original_grid)):
        #print("rindinja", row)
        for col in range(len(original_grid[row])):
         #   print("kolonna", col)
            cell_color = WHITE
            if adjacency_grid[row][col] == 0:
                cell_color = DARK_BLUE
            elif (row, col) in selected_cells:
                cell_color = LIGHT_BLUE
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


def handle_mouse_events(original_grid, adjacency_grid, buttons, button_actions):  # I think this function might handle mouse events
    global selected_cells
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
                        action() # Call button action if button is clicked
                if (col > NUM_COLS - 1 or row > len(adjacency_grid) - 1):  # handle situation if you click outside the numbers
                    print("out of boundz")
                    selected_cells = []
                    return

                if (adjacency_grid[row][col] == 0):  # check that you don't pick an already erased number
                    print("iekaapu sviestaa pirms tam")
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
                            if all(element == 0 for element in adjacency_grid):
                                print("Wow, you finished!")
                                display_dialog(window, "Congratulations!", type="ok")

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


def hint_match(adjacency_grid):
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

    def redrawbutton_action():
        print("redraw Button clicked with difficulty", difficulty_level)
        if difficulty_level == "hard":
            if hint_match(adjacency_grid) == False:
                redraw_board(original_grid, adjacency_grid)
            else:
                display_dialog(window, "More matches possible!", type="ok")
        elif difficulty_level == "easy":
            redraw_board(original_grid, adjacency_grid)

    def newbutton_action():
        print("ACHTUNG!!@! new game button has been pressed ")
        choice = display_dialog(window, "New game? Sure?", type="yes_no")
        print("choice", choice)
        if choice == True:
            global original_grid
            global adjacency_grid
            print(kopija)
            original_grid = kopija
            adjacency_grid = kopija

        elif choice == False:
            print("pressed no")

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
        # Delete rows from adjacency_grid and original_grid
        for index in reversed(rows_to_delete):
            del adjacency_grid[index]
            del original_grid[index]

    redrawbutton = Button("Redraw", (WINDOW_WIDTH - 120, 40), redrawbutton_action)
    easybutton = Button("Easy", (WINDOW_WIDTH - 120, 180), easybutton_action)
    defbutton = Button("Difficult", (WINDOW_WIDTH - 120, 220), defbutton_action)
    erasebutton = Button("Del empty", (WINDOW_WIDTH - 120, 260), erasebutton_action)
    newbutton = Button("New game", (WINDOW_WIDTH - 120, 300), newbutton_action)

    # Create font object for permanent text (difficulty level)
    font = pygame.font.Font(None, 24)  # You can change the font and size here

    # Store button-action pairs in a dictionary
    button_actions = {
        redrawbutton: redrawbutton_action,
        easybutton: easybutton_action,
        defbutton: defbutton_action,
        erasebutton: erasebutton_action,
        newbutton: newbutton_action,
    }
    buttons = [redrawbutton, easybutton, defbutton, erasebutton]
    running = True

    while running:
        # Handle events
        handle_mouse_events(grid, adjacency_grid, buttons, button_actions)

        # Draw everything
        window.fill(WHITE)
        draw_grid(grid, adjacency_grid)
        easybutton.draw(window)
        redrawbutton.draw(window)
        defbutton.draw(window)
        erasebutton.draw(window)
        newbutton.draw(window)
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
