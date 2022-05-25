import pygame
import math
import random
import sys


def grid_setup(dimensions, mines):
    grid = []
    for i in range(dimensions[1]):
        grid.append([])
        for j in range(dimensions[0]):
            grid[i].append(["", True, False]) # Adds a tile as a list that contains Mine/Adj. Mines, is_hidden, and is_flagged
    while mines > 0:
        x = random.randint(0, dimensions[0]-1)
        y = random.randint(0, dimensions[1]-1)
        if grid[y][x][0] != "X":
            grid[y][x][0] = "X"
            mines -= 1
    grid = get_adjacencies(grid)
    return grid


def draw_grid(screen, grid, tile_size, font, pos, sprites):
    tile_sprite = None
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            tile_sprite = None
            if not tile[1]:
                if tile[0] == "X":
                    tile_sprite = sprites[1]
                else:
                    tile_sprite = None
                    adj_text = font.render(str(tile[0]), True, "black")
                    adj_rect = adj_text.get_rect()
                    adj_rect.topleft = (j * tile_size + pos.x + 5, i * tile_size + pos.y)
                    pygame.draw.rect(screen, (200,200,200), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))
                    if tile[0] > 0:
                        screen.blit(adj_text, adj_rect)
            elif tile[2]:
                tile_sprite = sprites[4]
            else:
                pygame.draw.rect(screen, (50,50,50), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))
                tile_sprite = sprites[0]
            if tile_sprite:
                screen.blit(tile_sprite, (j * tile_size + pos.x, i * tile_size + pos.y,))


def get_adjacencies(grid):
    # Check surrounding tiles, and change it to the amount of tiles around
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile[0] != "X":
                adjacencies = 0
                upper_row = i-1
                lower_row = i+1
                # Upper row
                if upper_row >= 0:
                    for k in range(3):
                        if 0 <= j+k-1 < len(row):
                            if grid[upper_row][j+k-1][0] == "X":
                                adjacencies += 1
                # Same row
                if j - 1 >= 0:
                    if row[j-1][0] == "X":
                        adjacencies += 1
                if j + 1 < len(row):
                    if row[j+1][0] == "X":
                        adjacencies += 1
                # Lower row
                if lower_row < len(grid):
                    for k in range(3):
                        if 0 <= j+k-1 < len(row):
                            if grid[lower_row][j+k-1][0] == "X":
                                adjacencies += 1
                tile[0] = adjacencies

    return grid


def get_tile_from_mouse(grid, size, pos):
    current_tile = pygame.math.Vector2((pygame.mouse.get_pos()))
    current_tile -= pos
    current_tile //= size
    current_tile = list(current_tile)
    if current_tile[1] > len(grid)-1 or current_tile[0] > len(grid[0])-1:
        return None
    if current_tile[0] < 0 or current_tile[1] < 0:
        return None
    x = int(current_tile[0])
    y = int(current_tile[1])
    current_tile = y, x
    return current_tile


def reveal_all_tiles(grid):
    for row in grid:
        for tile in row:
            if tile[2]:
                continue
            tile[1] = False


def reveal_tile(grid, y, x):
    grid[y][x][1] = False
    if isinstance(grid[y][x][0], str):
        return True
    if grid[y][x][0] == 0:
        for nx, ny in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]: # Sjekker naboer
            if x + nx >= 0 and x + nx < len(grid[0]) and y + ny >= 0 and y+ny < len(grid):
                if grid[y+ny][x+nx][1] and not grid[y+ny][x+nx][2]:
                    reveal_tile(grid, y+ny, x+nx)
    return False

def main():
    # Pygame setup
    pygame.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    fps = 60

    tile_size = 24
    font = pygame.font.SysFont("Comic sans", tile_size * 4 // 3)
    grid_w, grid_h = 30, 16
    grid = grid_setup((grid_w, grid_h), 99)
    grid_pos = pygame.math.Vector2((100, 100))
    lmb_down = False
    rmb_down = False
    space_down = False
    is_dead = False
    has_started = False
     
    # Loading in assets and scaling them to tile size
    tile_hidden_sprite = pygame.transform.smoothscale(pygame.image.load("Assets/minesweeper/tile_hidden.png"), (tile_size, tile_size)).convert_alpha()
    mine_sprite = pygame.transform.smoothscale(pygame.image.load("Assets/minesweeper/mine.png"), (tile_size, tile_size)).convert_alpha()
    mine_clicked_sprite = pygame.transform.smoothscale(pygame.image.load("Assets/minesweeper/takethel.png"), (tile_size, tile_size)).convert_alpha()
    false_flag_sprite = pygame.transform.smoothscale(pygame.image.load("Assets/minesweeper/youdungoofed.png"), (tile_size, tile_size)).convert_alpha()
    tile_flagged_sprite = pygame.transform.smoothscale(pygame.image.load("Assets/minesweeper/tile_flagged.png"), (tile_size, tile_size)).convert_alpha()
    sprites = [tile_hidden_sprite, mine_sprite, mine_clicked_sprite, false_flag_sprite, tile_flagged_sprite]

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        keys = pygame.key.get_pressed()
        mouse_tile = get_tile_from_mouse(grid, tile_size, grid_pos)
        mouse = pygame.mouse.get_pressed()

        if is_dead:
            reveal_all_tiles(grid)
            if keys[pygame.K_SPACE]:
                if not space_down:
                    grid = grid_setup((grid_w, grid_h), 99)
                    is_dead = False
                    space_down = True
            else:
                space_down = False
            
        if not is_dead:
            if mouse[0]:
                if not lmb_down:
                    if mouse_tile and grid[mouse_tile[0]][mouse_tile[1]][1] and not grid[mouse_tile[0]][mouse_tile[1]][2]:
                                is_dead = reveal_tile(grid, mouse_tile[0], mouse_tile[1])
                    lmb_down = True
            else:
                lmb_down = False

            if mouse[2]:
                if not rmb_down:
                    if mouse_tile:
                        if grid[mouse_tile[0]][mouse_tile[1]][2]:
                            grid[mouse_tile[0]][mouse_tile[1]][2] = False
                        else:
                            grid[mouse_tile[0]][mouse_tile[1]][2] = True
                    rmb_down = True
            else:
                rmb_down = False

        if keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))
        if keys[pygame.K_u]:
            reveal_all_tiles(grid)

        draw_grid(screen, grid, tile_size, font, grid_pos, sprites)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
