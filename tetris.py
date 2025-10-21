import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 10, 20
CELL = 30
W, H = WIDTH * CELL, HEIGHT * CELL
FPS = 60

# 색상
COLORS = [
    (0, 0, 0),
    (0, 240, 240),  # I
    (0, 0, 240),    # J
    (240, 160, 0),  # L
    (240, 240, 0),  # O
    (0, 240, 0),    # S
    (160, 0, 240),  # T
    (240, 0, 0),    # Z
]

# 테트리스 블록 형태(회전 포함)
SHAPES = [
    # I
    [[(0,1),(1,1),(2,1),(3,1)], [(2,0),(2,1),(2,2),(2,3)]],
    # J
    [[(0,0),(0,1),(1,1),(2,1)], [(1,0),(2,0),(1,1),(1,2)], [(0,1),(1,1),(2,1),(2,2)], [(1,0),(1,1),(0,2),(1,2)]],
    # L
    [[(2,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(1,2),(2,2)], [(0,1),(1,1),(2,1),(0,2)], [(0,0),(1,0),(1,1),(1,2)]],
    # O
    [[(1,0),(2,0),(1,1),(2,1)]],
    # S
    [[(1,0),(2,0),(0,1),(1,1)], [(1,0),(1,1),(2,1),(2,2)]],
    # T
    [[(1,0),(0,1),(1,1),(2,1)], [(1,0),(1,1),(2,1),(1,2)], [(0,1),(1,1),(2,1),(1,2)], [(1,0),(0,1),(1,1),(1,2)]],
    # Z
    [[(0,0),(1,0),(1,1),(2,1)], [(2,0),(1,1),(2,1),(1,2)]],
]

class Piece:
    def __init__(self, x, y, shape_id):
        self.x = x
        self.y = y
        self.shape_id = shape_id
        self.rot = 0
        self.shape = SHAPES[shape_id]

    def cells(self):
        coords = []
        layout = self.shape[self.rot % len(self.shape)]
        for px, py in layout:
            coords.append((self.x + px, self.y + py))
        return coords

    def rotate(self):
        self.rot = (self.rot + 1) % len(self.shape)

    def rotate_back(self):
        self.rot = (self.rot - 1) % len(self.shape)

def create_grid(locked):
    grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    for (x, y), val in locked.items():
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            grid[y][x] = val
    return grid

def valid_space(piece, grid):
    for x, y in piece.cells():
        if x < 0 or x >= WIDTH or y >= HEIGHT:
            return False
        if y >= 0 and grid[y][x] != 0:
            return False
    return True

def clear_lines(grid, locked):
    removed = 0
    for y in range(HEIGHT-1, -1, -1):
        if 0 not in grid[y]:
            removed += 1
            # remove line from locked
            for x in range(WIDTH):
                if (x, y) in locked:
                    del locked[(x, y)]
            # move everything above down
            for key in sorted(list(locked.keys()), key=lambda k:k[1])[::-1]:
                xk, yk = key
                if yk < y:
                    locked[(xk, yk+1)] = locked.pop((xk, yk))
    return removed

def get_new_piece():
    idx = random.randrange(len(SHAPES))
    return Piece(WIDTH//2 - 2, -2, idx)

def draw_window(surface, grid, score):
    surface.fill((10,10,10))
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = COLORS[grid[y][x]]
            pygame.draw.rect(surface, color, (x*CELL, y*CELL, CELL, CELL), 0)
            pygame.draw.rect(surface, (30,30,30), (x*CELL, y*CELL, CELL, CELL), 1)
    # score
    font = pygame.font.SysFont('arial', 18)
    text = font.render(f"Score: {score}", True, (255,255,255))
    surface.blit(text, (5, 5))

def draw_piece(surface, piece):
    for x, y in piece.cells():
        if y >= 0:
            pygame.draw.rect(surface, COLORS[piece.shape_id+1], (x*CELL, y*CELL, CELL, CELL))
            pygame.draw.rect(surface, (30,30,30), (x*CELL, y*CELL, CELL, CELL), 1)

def main():
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    locked = {}
    grid = create_grid(locked)
    change_piece = False
    run = True
    current_piece = get_new_piece()
    next_piece = get_new_piece()
    fall_time = 0
    fall_speed = 0.5
    level_time = 0
    score = 0

    while run:
        dt = clock.tick(FPS) / 1000.0
        fall_time += dt
        level_time += dt

        if level_time > 10:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.02

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    break
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        current_piece.rotate_back()
                if event.key == pygame.K_SPACE:
                    # hard drop
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    change_piece = True

        if fall_time > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                change_piece = True

        grid = create_grid(locked)
        # place current piece temporarily
        for x, y in current_piece.cells():
            if 0 <= y < HEIGHT and 0 <= x < WIDTH:
                grid[y][x] = current_piece.shape_id + 1

        if change_piece:
            for x, y in current_piece.cells():
                if y < 0:
                    # game over
                    run = False
                    break
                locked[(x, y)] = current_piece.shape_id + 1
            removed = clear_lines(grid, locked)
            if removed > 0:
                score += {1:100, 2:300, 3:700, 4:1500}.get(removed, removed*100)
            current_piece = next_piece
            next_piece = get_new_piece()
            change_piece = False

        draw_window(screen, grid, score)
        draw_piece(screen, current_piece)
        pygame.display.update()

    # 게임 종료 화면
    screen.fill((0,0,0))
    font = pygame.font.SysFont('arial', 36)
    text = font.render("Game Over", True, (255,255,255))
    screen.blit(text, (W//2 - text.get_width()//2, H//2 - text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()