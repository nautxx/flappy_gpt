import pygame
import random
import sys
import os

# Constants
WIDTH = 400
HEIGHT = 600
BACKGROUND_COLOR = (135, 206, 250)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = 0.25
FLAP_POWER = -6.5
MIN_PIPE_DISTANCE = 200

# Class for the Bird
class Bird:
    def __init__(self):
        self.y = HEIGHT // 2
        self.x = 50
        self.velocity = 0
        self.gravity = GRAVITY

    def flap(self):
        self.velocity = FLAP_POWER

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), 20)

# Class for the Pipe
class Pipe:
    def __init__(self):
        self.gap = 200
        self.x = WIDTH
        self.width = 50
        self.top = random.randint(0, HEIGHT - self.gap)
        self.bottom = self.top + self.gap

    def update(self):
        self.x -= 3

    def off_screen(self):
        return self.x < -self.width

    def hits(self, bird):
        if bird.y - 20 < self.top or bird.y + 20 > self.bottom:
            if bird.x + 20 > self.x and bird.x - 20 < self.x + self.width:
                return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, PIPE_COLOR, (self.x, self.bottom, self.width, HEIGHT))

# Class for Clouds
class Cloud:
    def __init__(self):
        self.x = random.randint(-100, WIDTH)
        self.y = random.randint(0, HEIGHT // 2)
        self.speed = random.uniform(0.1, 0.5)

    def update(self):
        self.x += self.speed
        if self.x > WIDTH:
            self.x = -100
            self.y = random.randint(0, HEIGHT // 2)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 20)

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
bird = Bird()
pipes = []
clouds = [Cloud() for _ in range(5)]  # Create 5 cloud instances
score = 0
top_score = 0
start_screen = True

# File to store top score
top_score_file = "top_score.txt"

# Load top score from file if it exists
if os.path.exists(top_score_file):
    with open(top_score_file, "r") as file:
        top_score = int(file.read())

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save top score to file before quitting
            with open(top_score_file, "w") as file:
                file.write(str(top_score))
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_screen:
                    start_screen = False
                else:
                    bird.flap()

    screen.fill(BACKGROUND_COLOR)

    # Update and draw clouds
    for cloud in clouds:
        cloud.update()
        cloud.draw(screen)

    if start_screen:
        # Display start screen
        font = pygame.font.Font(None, 36)
        text = font.render("Press SPACE to start", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
    else:
        # Add new pipe only if last pipe is far enough from screen edge
        if len(pipes) == 0 or WIDTH - pipes[-1].x > MIN_PIPE_DISTANCE:
            pipes.append(Pipe())

        bird.update()
        bird.draw(screen)

        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            if pipe.hits(bird):
                if score > top_score:
                    top_score = score
                score = 0
                pipes = []
                start_screen = True
            if pipe.off_screen():
                pipes.remove(pipe)
                score += 1

        if score > top_score:
            top_score = score

        # Render top score
        font = pygame.font.Font(None, 24)
        top_score_text = font.render("Top Score: " + str(top_score), True, (255, 255, 255))
        top_score_rect = top_score_text.get_rect(center=(WIDTH // 2, 10))
        screen.blit(top_score_text, top_score_rect)

        pygame.display.set_caption("Flappy Bird | Score: " + str(score))

    pygame.display.update()
    clock.tick(60)
