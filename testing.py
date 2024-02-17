import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Button:
    def __init__(self, text, position, action):
        self.text = text
        self.position = position
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(self.position[0], self.position[1], 200, 50)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

def main():
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pygame Button Example")

    clock = pygame.time.Clock()

    # Define button action
    def button_action():
        print("Button clicked!")

    # Create button
    button = Button("Click me", (screen_width - 250, 50), button_action)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            button.handle_event(event)

        screen.fill(WHITE)
        button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
