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


def draw_grid(screen, grid, tile_size, font, pos):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if not tile[1]:
                if tile[0] == "X":
                    pygame.draw.rect(screen, (200,50,50), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))
                else:
                    adj_text = font.render(str(tile[0]), True, "black")
                    adj_rect = adj_text.get_rect()
                    adj_rect.topleft = (j * tile_size + pos.x + 5, i * tile_size + pos.y)
                    pygame.draw.rect(screen, (200,200,200), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))
                    if tile[0] > 0:
                        screen.blit(adj_text, adj_rect)
            elif tile[2]:
                pygame.draw.rect(screen, (50,200,50), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))
            else:
                pygame.draw.rect(screen, (50,50,50), (j * tile_size + pos.x, i * tile_size + pos.y, tile_size-1, tile_size-1))


def get_adjacencies(grid):
    # Check surrounding tiles, and change it to the amount of tiles around
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if tile[0] != "X":
                adjacencies = 0
                # Upper row
                if i - 1 >= 0:
                    if 0 < j+k-1 < len(row):
                        for k in range(3):
                            if grid[i-1][j+k-1][0] == "X":
                                adjacencies += 1
                # Same row
                if j - 1 >= 0:
                    if row[j-1][0] == "X":
                        adjacencies += 1
                if j + 1 < len(row):
                    if row[j+1][0] == "X":
                        adjacencies += 1
                # Lower row
                if i + 1 < len(grid):
                    for k in range(3):
                        if 0 < j+k-1 < len(row):
                            if grid[i+1][j+k-1][0] == "X":
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
    x = int(current_tile[0])
    y = int(current_tile[1])
    current_tile = y, x
    return current_tile

def main():
    # Pygame setup
    pygame.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()
    fps = 60

    tile_size = 24
    font = pygame.font.SysFont("Comic sans", tile_size * 2 // 3)
    grid_w, grid_h = 30, 16
    grid = grid_setup((grid_w, grid_h), 50)
    grid_pos = pygame.math.Vector2((100, 100))
    lmb_down = False
    rmb_down = False
    space_down = False

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        mouse_tile = get_tile_from_mouse(grid, tile_size, grid_pos)
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if not lmb_down:
                if mouse_tile:
                    print(mouse_tile)
                    if grid[mouse_tile[0]][mouse_tile[1]][1]:
                        if grid[mouse_tile[0]][mouse_tile[1]][2] == False:
                            grid[mouse_tile[0]][mouse_tile[1]][1] = False
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

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_SPACE]:
            if not space_down:
                grid = grid_setup((grid_w, grid_h), 99)
                space_down = True
        else:
            space_down = False
        if keys[pygame.K_u]:
            for row in grid:
                for tile in row:
                    tile[1] = False

        draw_grid(screen, grid, tile_size, font, grid_pos)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
