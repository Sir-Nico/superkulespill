import pygame
import math
import random
import sys


def grid_setup(dimensions, mines):
    grid = []
    for i in range(dimensions[1]):
        grid.append([])
        for j in range(dimensions[0]):
            grid[i].append(["", True, False]) # Adds a tile as a list that contains Mine/no Mine, is_hidden, and is_flagged
    while mines > 0:
        x = random.randint(0, dimensions[0]-1)
        y = random.randint(0, dimensions[1]-1)
        if grid[y][x][0] != "X":
            grid[y][x][0] = "X"
            mines -= 1
    return grid


def draw_grid(screen, grid, tile_size):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            if not tile[1]:
                if tile[0] == "X":
                    pygame.draw.rect(screen, (200,50,50), ((j * tile_size, i * tile_size, tile_size-1, tile_size-1)))
                else:
                    pygame.draw.rect(screen, (200,200,200), ((j * tile_size, i * tile_size, tile_size-1, tile_size-1)))
            elif tile[2]:
                pygame.draw.rect(screen, (50,200,50), ((j * tile_size, i * tile_size, tile_size-1, tile_size-1)))
            else:
                pygame.draw.rect(screen, (50,50,50), ((j * tile_size, i * tile_size, tile_size-1, tile_size-1)))


def get_tile_from_mouse(grid, size):
    current_tile = pygame.math.Vector2((pygame.mouse.get_pos()))
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

    grid = grid_setup((20, 10), 50)
    tile_size = 24
    lmb_down = False
    rmb_down = False
    space_down = False

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        
        mouse_tile = get_tile_from_mouse(grid, tile_size)
        mouse = pygame.mouse.get_pressed()
        if mouse[0]:
            if not lmb_down:
                if grid[mouse_tile[0]][mouse_tile[1]][1] == False and grid[mouse_tile[0]][mouse_tile[1]][2] == False:
                    grid[mouse_tile[0]][mouse_tile[1]][1] = False
                lmb_down = True
        else:
            lmb_down = False
        # if mouse[2]:
        #     if not rmb_down:
        #         if grid[mouse_tile[0]][mouse_tile[1]][2]:
        #             grid[mouse_tile[0]][mouse_tile[1]][2] = False
        #             rmb_down = True
        #         else:
        #             grid[mouse_tile[0]][mouse_tile[1]][2] = True
        #             rmb_down = True
        # else:
        #     rmb_down = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            break
        if keys[pygame.K_SPACE]:
            if not space_down:
                grid = grid_setup((30, 16), 99)
                space_down = True
        else:
            space_down = False

        draw_grid(screen, grid, tile_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()