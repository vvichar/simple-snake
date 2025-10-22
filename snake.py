import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Snake Game")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont("Arial", 24)

def draw_grid():
    """Draw grid lines on the screen."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def draw_snake(snake):
    """Draw the snake on the screen."""
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_food(food):
    """Draw the food on the screen."""
    pygame.draw.rect(screen, RED, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def generate_food(snake):
    """Generate food at a random position not occupied by the snake."""
    while True:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food

def check_collision(snake):
    """Check if the snake has collided with itself or the walls."""
    head = snake[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
        return True
    if head in snake[1:]:
        return True
    return False

def main():
    """Main game loop."""
    # Initialize snake in the middle of the screen
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)  # Moving right initially
    food = generate_food(snake)
    score = 0
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        main()  # Restart game
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                else:
                    # Change direction (prevent 180-degree turns)
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)

        if not game_over:
            # Move snake
            head = snake[0]
            new_head = (head[0] + direction[0], head[1] + direction[1])
            snake.insert(0, new_head)

            # Check if food is eaten
            if new_head == food:
                score += 1
                food = generate_food(snake)
            else:
                snake.pop()

            # Check for collisions
            if check_collision(snake):
                game_over = True

        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw game over message
        if game_over:
            game_over_text = font.render("GAME OVER! Press R to Restart or Q to Quit", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
