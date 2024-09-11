# ===================
# Imports
# ===================
import pygame
import random

# ===================
# Initialize Pygame
# ===================
pygame.init()

# ===================
# General Settings
# ===================
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

WHITE = (215, 104, 245)
BLACK = (15, 207, 255)

player_speed = 10
ai_speed = 2
ai_difficulty = .5
rounds = 15
player_score = 0
player2_score = 0
ai_score = 0
current_round = 1
ball = None
obstacle1 = None
obstacle2 = None
font = pygame.font.Font(None, 36)

# ===================
# Classes
# ===================
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 100)

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

player = Paddle(50, HEIGHT // 2 - 50)
ai = Paddle(WIDTH - 65, HEIGHT // 2 - 50)

class Paddle2:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 100)

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def move(self, y):
        self.rect.y += y
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 15, 15)
        self.vx = random.choice([-1, 1]) * random.randint(5, 7)
        self.vy = random.choice([-1, 1]) * random.randint(3, 5)

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

    def move(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.vy = -self.vy

class Obstacle:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-100), 10, 50)

    def draw(self):
        pygame.draw.rect(WIN, WHITE, self.rect)

def draw_scoreai():
    score_text = font.render(f"Player: {player_score} - AI: {ai_score}", True, WHITE)
    WIN.blit(score_text, (10, 10))

def draw_scoremulti():
    if player2 is not None:
        score_text = font.render(f"Player 1: {player_score} - Player 2: {player2_score}", True, WHITE)
    else:
        score_text = font.render(f"Player: {player_score} - AI: {ai_score}", True, WHITE)
    WIN.blit(score_text, (10, 10))

def ai_move():
    if ball is not None:
        if ai.rect.centery < ball.rect.centery:
            ai.move(ai_speed * ai_difficulty)
        elif ai.rect.centery > ball.rect.centery:
            ai.move(-ai_speed * ai_difficulty)

def generate_obstacles():
    global obstacle1, obstacle2
    obstacle1 = Obstacle()
    obstacle2 = Obstacle()

def main():
    global ball, player_score, ai_score, current_round, obstacle1, obstacle2, ai_speed

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        ai_speed = 2 * (current_round / 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(-player_speed)
        if keys[pygame.K_DOWN]:
            player.move(player_speed)

        if ball is None:
            ball = Ball()

        ball.move()

        if ball.rect.colliderect(player.rect) or (ball is not None and ball.rect.colliderect(ai.rect)):
            ball.vx = -ball.vx

        if ball is not None and (ball.rect.left < 0 or ball.rect.right > WIDTH):
            if ball.rect.left < 0:
                ai_score += 1
            else:
                player_score += 1

            if current_round < rounds:
                current_round += 1
                ball = None
                generate_obstacles()
            else:
                run = False

        ai_move()

        WIN.fill(BLACK)
        player.draw()
        ai.draw()
        if ball is not None:
            ball.draw()
        pygame.draw.rect(WIN, WHITE, (WIDTH // 2, 0, 2, HEIGHT))

        if obstacle1 is not None and obstacle2 is not None:
            obstacle1.draw()
            obstacle2.draw()

        if ball is not None and obstacle1 is not None and obstacle2 is not None:
            if obstacle1.rect.colliderect(ball.rect) or obstacle2.rect.colliderect(ball.rect):
                ball.vx = -ball.vx

        draw_scoreai()

        pygame.display.update()

    pygame.quit()

def modoMulti():
    global ball, player_score, player2_score, ai_score, current_round, obstacle1, obstacle2, ai_speed, player, player2

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        ai_speed = 2 * current_round

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player2.move(-player_speed)
        if keys[pygame.K_DOWN]:
            player2.move(player_speed)

        if keys[pygame.K_w]:
            player.move(-player_speed)
        if keys[pygame.K_s]:
            player.move(player_speed)

        if ball is None:
            ball = Ball()

        ball.move()

        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(player2.rect):
            ball.vx = -ball.vx

        if ball is not None and (ball.rect.left < 0 or ball.rect.right > WIDTH):
            if ball.rect.left < 0:
                player_score += 1
            else:
                player2_score += 1

            if current_round < rounds:
                current_round += 1
                ball = None
                generate_obstacles()
            else:
                run = False

        WIN.fill(BLACK)
        player.draw()
        player2.draw()
        if ball is not None:
            ball.draw()
        pygame.draw.rect(WIN, WHITE, (WIDTH // 2, 0, 2, HEIGHT))

        if obstacle1 is not None and obstacle2 is not None:
            obstacle1.draw()
            obstacle2.draw()

        if ball is not None and obstacle1 is not None and obstacle2 is not None:
            if obstacle1.rect.colliderect(ball.rect) or obstacle2.rect.colliderect(ball.rect):
                ball.vx = -ball.vx

        draw_scoremulti()

        pygame.display.update()

    pygame.quit()

def menu():
    global player, player2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        WIN.fill(BLACK)
        menu_text = font.render("1 - AI Mode, 2 - Multiplayer Mode", True, WHITE)
        WIN.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - menu_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            main()
        elif keys[pygame.K_2]:
            player = Paddle(50, HEIGHT // 2 - 50)
            player2 = Paddle2(WIDTH - 65, HEIGHT // 2 - 50)
            modoMulti()

        pygame.display.update()

if __name__ == "__main__":
    generate_obstacles()
    menu()
