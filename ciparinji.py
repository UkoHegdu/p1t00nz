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
GRID_MARGIN = 0
NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Define variables to keep track of selected cells
selected_cells = []

def draw_grid(grid):
    # Draw grid cells
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            cell_color = LIGHT_BLUE if (row, col) in selected_cells else WHITE #detect cell colour
            pygame.draw.rect(window, cell_color, [
                GRID_MARGIN + col * (GRID_WIDTH + GRID_MARGIN),
                GRID_MARGIN + row * (GRID_HEIGHT + GRID_MARGIN),
                GRID_WIDTH + GRID_MARGIN, GRID_HEIGHT + GRID_MARGIN])
            font = pygame.font.Font(None, 40)
            text = font.render(str(grid[row][col]), True, BLACK)
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
    pygame.draw.rect(window, RED, [WINDOW_HEIGHT + 75, 0, GRID_MARGIN, WINDOW_HEIGHT])  # notebook red line

def handle_mouse_events(grid):
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
                if 0 <= row < NUM_ROWS and 0 <= col < NUM_COLS:
                    cell_pos = (row, col)
                    if len(selected_cells) < 2:
                        if cell_pos in selected_cells:
                            selected_cells.remove(cell_pos)
                        else:
                            selected_cells.append(cell_pos)
                    if len(selected_cells) == 2:
                        # Compare numbers in the selected cells
                        row1, col1 = selected_cells[0]
                        row2, col2 = selected_cells[1]
                        num1 = grid[row1][col1]
                        num2 = grid[row2][col2]
                        if num1 == num2:
                            print("Numbers match!")
                            # Add your code here to handle when numbers match
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
    grid = [[random.choice(NUMBERS) for _ in range(NUM_COLS)] for _ in range(NUM_ROWS)]
    running = True
    while running:
        # Handle events
        handle_mouse_events(grid)

        # Draw everything
        window.fill(WHITE)
        draw_grid(grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
