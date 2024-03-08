import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
CELL_SIZE = 30
GRID_WIDTH = 9
GRID_HEIGHT = 9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Grid with Numbers")

# 2D Array
grid = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [2, 2, 3, 4, 5, 6, 7, 8, 9]
]


# Function to draw the grid
def draw_grid():
    print("GRID_HEIGHT:", GRID_HEIGHT)
    print("len(grid):", len(grid))
    for y in range(min(GRID_HEIGHT, len(grid)+1)):
        print("y:", y)
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)
            if y >= 1:  # Fill squares from the 2nd row
                font = pygame.font.SysFont(None, 24)
                if x < len(grid[y]):  # Check if x is within the bounds of the row
                    number_text = font.render(str(grid[y-1][x]), True, BLACK)
                    screen.blit(number_text, rect.topleft)
                    #screen.blit(number_text, (rect.topleft[0] + 10, rect.topleft[1]))  # Adjust x-coordinate for number rendering
                else:
                    print("x out of range:", x)
        print()  # Add a newline for clarity

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    draw_grid()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()