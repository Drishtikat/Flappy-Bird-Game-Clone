import pygame
import random

# Initialize pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, 300
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
GROUND_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load images
bird_img = pygame.image.load("bird.png")  # Make sure to have a 'bird.png' file
bird_img = pygame.transform.scale(bird_img, (40, 30))

# Bird properties
bird_y = BIRD_Y
bird_velocity = 0

# Pipe properties
pipes = []
def create_pipe():
    height = random.randint(100, 400)
    pipes.append({"x": WIDTH, "top": height, "bottom": height + PIPE_GAP, "scored": False})

# Score
score = 0
font = pygame.font.Font(None, 36)

# Game Loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_velocity = JUMP_STRENGTH

    # Bird movement
    bird_velocity += GRAVITY
    bird_y += bird_velocity

    # Draw bird
    screen.blit(bird_img, (BIRD_X, bird_y))

    # Pipe Movement
    for pipe in pipes:
        pipe["x"] -= PIPE_SPEED
        pygame.draw.rect(screen, GREEN, (pipe["x"], 0, PIPE_WIDTH, pipe["top"]))
        pygame.draw.rect(screen, GREEN, (pipe["x"], pipe["bottom"], PIPE_WIDTH, HEIGHT - pipe["bottom"]))

        # Collision detection
        if BIRD_X < pipe["x"] + PIPE_WIDTH and BIRD_X + 40 > pipe["x"]:
            if bird_y < pipe["top"] or bird_y + 30 > pipe["bottom"]:
                running = False  # Game over

        # Increase score when bird completely passes the pipe
        if pipe["x"] + PIPE_WIDTH < BIRD_X and not pipe["scored"]:
            score += 1
            pipe["scored"] = True  # Mark this pipe as scored

    # Generate new pipes
    if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
        create_pipe()

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]

    # Draw ground
    pygame.draw.rect(screen, BLUE, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

    # Check if bird hits the ground
    if bird_y + 30 > HEIGHT - GROUND_HEIGHT:
        running = False  # Game over

    # Display score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
print(f"Game Over! Score: {score}")