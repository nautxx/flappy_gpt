import pygame
import random
import sys
import os

# Constants
WIDTH = 400
HEIGHT = 600
GROUND_HEIGHT = 100
BACKGROUND_COLOR = (135, 206, 250)
GROUND_COLOR = (210, 180, 140)  # Tan color
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = 0.25
FLAP_POWER = -6.5
MIN_PIPE_DISTANCE = 175  # Increased distance between pipes
BUTTON_COLOR = (255, 0, 0)
BUTTON_WIDTH = 30
BUTTON_HEIGHT = 30

class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.y = random.randint(HEIGHT // 4, HEIGHT - 4 * GROUND_HEIGHT)
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

    def hits_ground(self):
        return self.y + 20 > HEIGHT - GROUND_HEIGHT

class Pipe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.gap = 150  # Gap between pipes
        self.x = WIDTH
        self.width = 50
        self.top = random.randint(0, HEIGHT - self.gap - GROUND_HEIGHT)
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

class Button:
    def __init__(self, rect):
        self.rect = rect

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def save_top_score(score, top_score_file):
    if score > get_top_score(top_score_file):
        with open(top_score_file, "w") as file:
            file.write(str(score))

def get_top_score(top_score_file):
    if os.path.exists(top_score_file):
        with open(top_score_file, "r") as file:
            return int(file.read())
    return 0

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    clouds = [Cloud() for _ in range(5)]
    score = 0
    top_score_file = "top_score.txt"
    start_screen = True
    pause_button = Button(pygame.Rect(10, 10, BUTTON_WIDTH, BUTTON_HEIGHT))

    def reset_game():
        nonlocal bird, pipes, score
        bird.reset()
        pipes = []
        score = 0

    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_top_score(score, top_score_file)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_clicked(event.pos):
                    if start_screen:
                        reset_game()
                        start_screen = False
                    else:
                        start_screen = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if start_screen:
                    reset_game()
                    start_screen = False
                else:
                    bird.flap()

        screen.fill(BACKGROUND_COLOR)
        for cloud in clouds:
            cloud.update()
            cloud.draw(screen)

        if start_screen:
            draw_text(screen, "Press SPACE to start", 36, (255, 255, 255), WIDTH // 2, HEIGHT // 2)
        else:
            pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

            if len(pipes) == 0 or WIDTH - pipes[-1].x > MIN_PIPE_DISTANCE:
                pipes.append(Pipe())

            bird.update()
            bird.draw(screen)

            for pipe in pipes:
                pipe.update()
                pipe.draw(screen)
                if pipe.hits(bird) or bird.hits_ground():
                    save_top_score(score, top_score_file)
                    start_screen = True

                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1

            top_score = get_top_score(top_score_file)
            draw_text(screen, f"Top Score: {top_score}", 24, (255, 255, 255), WIDTH // 2, 10)
            pygame.display.set_caption(f"Flappy Bird | Score: {score}")

        pause_button.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
