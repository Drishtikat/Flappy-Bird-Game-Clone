import pygame
import random
import time  # For precise delays

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize sound mixer

# Load sounds
flap_sound = pygame.mixer.Sound("flap_sound.mp3")
point_sound = pygame.mixer.Sound("point_sound.mp3")
hit_sound = pygame.mixer.Sound("hit_sound.mp3")
gameover_sound = pygame.mixer.Sound("gameover_sound.mp3")

# Load and play background music
pygame.mixer.music.load("background_music.mp3")  
pygame.mixer.music.set_volume(0.3)  # 🔉 Lower background music volume (30%)
pygame.mixer.music.play(-1)  # Loop forever

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
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load images
bird_img = pygame.image.load("bird.png")  
bird_img = pygame.transform.scale(bird_img, (40, 30))

# Font
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 48)

# Function to show Game Over screen
def show_game_over(score):
    screen.fill(WHITE)
    
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)

    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 40))
    screen.blit(final_score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 10))

    pygame.display.update()
    time.sleep(2)  # ⏳ Wait before exiting
    pygame.quit()
    exit()

# Main Game Loop
def main():
    global bird_y, bird_velocity

    bird_y = BIRD_Y
    bird_velocity = 0
    pipes = []
    score = 0
    clock = pygame.time.Clock()

    while True:
        screen.fill(WHITE)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = JUMP_STRENGTH
                flap_sound.play()

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
                    hit_sound.play()
                    pygame.mixer.music.stop()
                    gameover_sound.play()
                    time.sleep(1)  # ⏳ Short delay
                    show_game_over(score)  

            # Increase score when bird completely passes the pipe
            if pipe["x"] + PIPE_WIDTH < BIRD_X and not pipe["scored"]:
                score += 1
                pipe["scored"] = True  
                point_sound.play()

        # Generate new pipes
        if len(pipes) == 0 or pipes[-1]["x"] < WIDTH - 200:
            height = random.randint(100, 400)
            pipes.append({"x": WIDTH, "top": height, "bottom": height + PIPE_GAP, "scored": False})

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe["x"] > -PIPE_WIDTH]

        # Draw ground
        pygame.draw.rect(screen, BLUE, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # Check if bird hits the ground
        if bird_y + 30 > HEIGHT - GROUND_HEIGHT:
            hit_sound.play()
            pygame.mixer.music.stop()
            gameover_sound.play()
            time.sleep(1)
            show_game_over(score)  

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(30)

# Run the game
main()
