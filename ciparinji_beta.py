import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Number Matching Game")

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
GRID_MARGIN = 0 #principaa tas grid margin taalaak kodaa nav vajadziigs lmao

# Define the initial grid
original_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 1, 1, 2, 1, 3, 1, 4, 1],
    [5, 1, 6, 1, 7, 1, 8, 1, 9]
]

adjacency_grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 1, 1, 2, 1, 3, 1, 4, 1],
    [5, 1, 6, 1, 7, 1, 8, 1, 9]
]

# Define variables to keep track of selected cells
selected_cells = []

def draw_grid(original_grid, adjacency_grid):
    # Draw grid cells
    for row in range(len(original_grid)):
        for col in range(len(original_grid[row])):
            cell_color = WHITE
            if adjacency_grid[row][col] == 0:
                cell_color = DARK_BLUE
            elif (row, col) in selected_cells:
                cell_color = LIGHT_BLUE
            pygame.draw.rect(window, cell_color, [
                GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN),
                GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN),
                GRID_WIDTH + GRID_MARGIN, GRID_HEIGHT + GRID_MARGIN])
            ''' # Draw squiggly lines for the crossed-out effect
            if adjacency_grid[row][col] == 0:
                # Calculate the position of the squiggly lines
                x = GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN)
                y = GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)
                width = GRID_WIDTH
                height = GRID_HEIGHT
                
                # Draw squiggly lines using pygame's drawing functions
                for i in range(0, width, 5):
                    pygame.draw.line(window, WHITE, (x + i, y), (x + i + 5, y + height), 2)
                    pygame.draw.line(window, WHITE, (x + i + 2, y), (x + i + 5, y + height), 2)
                    pygame.draw.line(window, WHITE, (x + i + 4, y), (x + i + 5, y + height), 2)'''
            font = pygame.font.Font(None, 40)
            text = font.render(str(original_grid[row][col]), True, BLACK)
            text_rect = text.get_rect(center=(
                GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN) + (GRID_WIDTH + GRID_MARGIN) / 2,
                GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN) + (GRID_HEIGHT + GRID_MARGIN) / 2)) # Adjusted to center
            window.blit(text, text_rect)
    
    # Draw horizontal lines
    for row in range(WINDOW_HEIGHT // GRID_HEIGHT):
        pygame.draw.line(window, BLUE, (GRID_MARGIN, GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)),
                         (WINDOW_WIDTH - GRID_MARGIN, GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN)), 2)
    
    # Draw vertical lines
    for col in range(WINDOW_WIDTH // GRID_WIDTH):
        pygame.draw.line(window, BLUE, (GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN), GRID_MARGIN),
                         (GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN), WINDOW_HEIGHT - GRID_MARGIN), 2)
        
    # Draw the red line that notebooks have
    pygame.draw.rect(window, RED, [WINDOW_WIDTH - 150, 0, 2, WINDOW_HEIGHT])  # notebook red line

def handle_mouse_events(original_grid, adjacency_grid):
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
                if adjacency_grid[row][col] == 0: # check that you don't pick an already erased number
                    display_dialog(window, "Number already removed!")
                    selected_cells = []

                elif 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
                    cell_pos = (row, col)
                    print("cell_pos", cell_pos)
                    if len(selected_cells) < 2:
                        if cell_pos in selected_cells:
                            selected_cells.remove(cell_pos)
                        else:
                            selected_cells.append(cell_pos)
                    if len(selected_cells) == 2:
                        # Compare numbers in the selected cells
                        row1, col1 = selected_cells[0]
                        row2, col2 = selected_cells[1]
                        num1 = original_grid[row1][col1]
                        num2 = original_grid[row2][col2]
                        if num1 == num2:
                            print("Numbers match!")
                            # Change the color of matched cells to DARK_BLUE
                            adjacency_grid[row1][col1] = 0
                            adjacency_grid[row2][col2] = 0
                            selected_cells = []
                        else:
                            print("Numbers do not match!")
                            display_dialog(window, "Numbers do not match!")
                            # Deselect the cells
                            selected_cells = []



def display_dialog(window, message): # koda klucis logam
    # Create a window surface
    dialog_surface = pygame.Surface((400, 200))
    dialog_surface.fill(LIGHT_BLUE)  # Fill the window surface with a color

    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect(center=(200, 80))

    button_surface = pygame.Surface((200, 50))
    button_surface.fill(BLUE)
    button_rect = button_surface.get_rect(center=(200, 150))

    # Render text on the button
    button_text = font.render("OK", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)

    dialog_surface.blit(text, text_rect)
    dialog_surface.blit(button_surface, button_rect)
    dialog_surface.blit(button_text, button_text_rect)  # Blit text onto the button

    # Get the rect for the dialog surface and center it on the game window
    dialog_rect = dialog_surface.get_rect(center=window.get_rect().center)

    window.blit(dialog_surface, dialog_rect)

    pygame.display.flip()

    # Wait for user input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if dialog_rect.collidepoint(x, y):
                    waiting = False





def main():
    # Create initial grid
    grid = original_grid
    running = True
    while running:
        # Handle events
        handle_mouse_events(grid, adjacency_grid)

        # Draw everything
        window.fill(WHITE)
        draw_grid(grid, adjacency_grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
