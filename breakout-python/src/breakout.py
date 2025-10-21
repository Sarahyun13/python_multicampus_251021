import pygame
import sys
import random

WIDTH, HEIGHT = 800, 600
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 24
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 16
BALL_RADIUS = 8

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (28, 28, 30)
BRICK_COLORS = [
    (255, 99, 71),
    (255, 165, 0),
    (255, 215, 0),
    (144, 238, 144),
    (135, 206, 235),
]

class Brick:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.alive = True

    def draw(self, surf):
        if self.alive:
            pygame.draw.rect(surf, self.color, self.rect)
            pygame.draw.rect(surf, BLACK, self.rect, 2)

class Paddle:
    def __init__(self):
        self.rect = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 8

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def update_with_mouse(self, mouse_x):
        self.rect.centerx = mouse_x
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self, surf):
        pygame.draw.rect(surf, (200, 200, 200), self.rect)
        pygame.draw.rect(surf, BLACK, self.rect, 2)

class Ball:
    def __init__(self):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        angle = random.uniform(-0.6, 0.6)
        speed = 5
        self.vel = pygame.Vector2(speed * (1 if random.random() < 0.5 else -1), -speed).rotate_rad(angle)
        self.radius = BALL_RADIUS

    def update(self):
        self.pos += self.vel

    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (int(self.pos.x), int(self.pos.y)), self.radius)
        pygame.draw.circle(surf, BLACK, (int(self.pos.x), int(self.pos.y)), self.radius, 2)

    def rect(self):
        return pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius*2, self.radius*2)

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.reset_level()
        self.lives = 3
        self.score = 0
        self.running = True
        self.mouse_control = True

    def reset_level(self):
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * BRICK_WIDTH
                y = 40 + row * (BRICK_HEIGHT + 4)
                rect = pygame.Rect(x + 2, y + 2, BRICK_WIDTH - 4, BRICK_HEIGHT)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                self.bricks.append(Brick(rect, color))
        self.paddle = Paddle()
        self.ball = Ball()
        self.ball.pos = pygame.Vector2(WIDTH // 2, HEIGHT - 80)
        self.ball.vel = pygame.Vector2(random.choice([-5, 5]), -5)

    def handle_collisions(self):
        # walls
        if self.ball.pos.x - self.ball.radius <= 0:
            self.ball.pos.x = self.ball.radius
            self.ball.vel.x *= -1
        if self.ball.pos.x + self.ball.radius >= WIDTH:
            self.ball.pos.x = WIDTH - self.ball.radius
            self.ball.vel.x *= -1
        if self.ball.pos.y - self.ball.radius <= 0:
            self.ball.pos.y = self.ball.radius
            self.ball.vel.y *= -1

        # paddle
        if self.ball.rect().colliderect(self.paddle.rect):
            overlap_y = (self.paddle.rect.top - (self.ball.pos.y + self.ball.radius))
            if self.ball.vel.y > 0:
                self.ball.pos.y = self.paddle.rect.top - self.ball.radius
                self.ball.vel.y *= -1
                offset = (self.ball.pos.x - self.paddle.rect.centerx) / (self.paddle.rect.width / 2)
                self.ball.vel.x += offset * 3
                # limit speed
                if self.ball.vel.length() > 10:
                    self.ball.vel.scale_to_length(10)

        # bricks
        for brick in self.bricks:
            if not brick.alive:
                continue
            if self.ball.rect().colliderect(brick.rect):
                # simple response: invert y velocity and mark brick dead
                brick.alive = False
                self.score += 10
                # determine collision side
                overlap = self.ball.rect().clip(brick.rect)
                if overlap.width < overlap.height:
                    self.ball.vel.x *= -1
                else:
                    self.ball.vel.y *= -1
                break

    def update(self, dt):
        self.ball.update()
        self.handle_collisions()

        # ball falls
        if self.ball.pos.y - self.ball.radius > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.running = False
            else:
                self.ball = Ball()
                self.ball.pos = pygame.Vector2(WIDTH // 2, HEIGHT - 80)
                self.ball.vel = pygame.Vector2(random.choice([-5, 5]), -5)

        # check win
        if all(not b.alive for b in self.bricks):
            self.reset_level()

    def draw_hud(self):
        txt = self.font.render(f"Score: {self.score}   Lives: {self.lives}", True, WHITE)
        self.screen.blit(txt, (8, 8))

    def draw(self):
        self.screen.fill(BG_COLOR)
        for brick in self.bricks:
            brick.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_hud()

    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_m:
                        self.mouse_control = not self.mouse_control
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # click to launch if ball is stuck (simple)
                    if event.button == 1:
                        if abs(self.ball.vel.y) < 1:
                            self.ball.vel = pygame.Vector2(random.choice([-5, 5]), -5)

            keys = pygame.key.get_pressed()
            if not self.mouse_control:
                dx = 0
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    dx -= self.paddle.speed
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    dx += self.paddle.speed
                self.paddle.move(dx)
            else:
                mx, _ = pygame.mouse.get_pos()
                self.paddle.update_with_mouse(mx)

            if not self.running:
                # simple game over screen
                self.screen.fill(BG_COLOR)
                go = self.font.render("GAME OVER - R to restart, ESC to quit", True, WHITE)
                score = self.font.render(f"Final Score: {self.score}", True, WHITE)
                self.screen.blit(go, (WIDTH//2 - go.get_width()//2, HEIGHT//2 - 20))
                self.screen.blit(score, (WIDTH//2 - score.get_width()//2, HEIGHT//2 + 10))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.lives = 3
                            self.score = 0
                            self.running = True
                            self.reset_level()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                continue

            self.update(dt)
            self.draw()
            pygame.display.flip()

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Breakout - Single File")
    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()