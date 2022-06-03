import pygame
import random
import sys


def grid_setup(dimensions, mines):
    grid = []
    for i in range(dimensions[1]):
        grid.append([])
        for j in range(dimensions[0]):
            # Adds a tile as a list that contains Mine/Adj. Mines, is_hidden, and is_flagged
            # And an optional parameter which only exists if it is a clicked mine
            grid[i].append(["", True, False])
    while mines > 0:
        x = random.randint(0, dimensions[0]-1)
        y = random.randint(0, dimensions[1]-1)
        if grid[y][x][0] != "X":
            grid[y][x][0] = "X"
            mines -= 1
    grid = get_adjacencies(grid)
    return grid


def draw_grid(screen, grid, tile_size, font, colours, pos, sprites, is_dead, sondre):
    for i, row in enumerate(grid):
        for j, tile in enumerate(row):
            adj_text = None
            if not tile[1]:
                if tile[0] == "X":
                    tile_sprite = sprites[2]
                else:
                    tile_sprite = sprites[0]
                    if tile[0] > 0:
                        adj_text = font.render(
                            str(tile[0]), True, colours[tile[0]-1])
                        adj_rect = adj_text.get_rect()
                        adj_rect.center = (
                            j * tile_size + pos.x + (tile_size // 2), i * tile_size + pos.y + (tile_size // 2) + 1)
                    if tile[0] == 0 and len(tile) > 3:
                        tile_sprite = sondre
            elif tile[2]:
                tile_sprite = sprites[5]
                if tile[0] != "X" and is_dead:
                    tile_sprite = sprites[4]
            else:
                tile_sprite = sprites[1]

            if len(tile) > 3 and is_dead and tile[3] != "Sondre":
                tile_sprite = sprites[3]

            if tile_sprite:
                if tile_sprite == sprites[2] or tile_sprite == sprites[4]:
                    screen.blit(sprites[0], (j * tile_size +
                                pos.x, i * tile_size + pos.y,))
                screen.blit(tile_sprite, (j * tile_size +
                            pos.x, i * tile_size + pos.y,))
            if adj_text:
                if tile[0] > 0:
                    screen.blit(adj_text, adj_rect)


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


def reveal_all_mines(grid):
    for row in grid:
        for tile in row:
            if tile[2] or isinstance(tile[0], int):
                continue
            tile[1] = False


def hide_all_mines(grid):
    for row in grid:
        for tile in row:
            if tile[2] or isinstance(tile[0], int):
                continue
            tile[1] = True


def reveal_tile(grid, y, x):
    grid[y][x][1] = False
    if isinstance(grid[y][x][0], str):
        grid[y][x].append(True)
        return True, grid
    if grid[y][x][0] == 0:
        for nx, ny in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:  # Sjekker naboer
            if x + nx >= 0 and x + nx < len(grid[0]) and y + ny >= 0 and y+ny < len(grid):
                if grid[y+ny][x+nx][1] and not grid[y+ny][x+nx][2]:
                    reveal_tile(grid, y+ny, x+nx)
    return False, grid


def draw_face(screen, face_sprites, is_clicked, is_dead, has_won):
    face_pos = (442, 80)
    face_image = face_sprites[0]
    if is_clicked:
        face_image = face_sprites[1]
    elif is_dead:
        face_image = face_sprites[3]
    elif has_won:
        face_image = face_sprites[2]

    screen.blit(face_image, face_pos)


def check_board(grid):
    remaining_tiles = 0
    for row in grid:
        for tile in row:
            if tile[1]:
                remaining_tiles += 1
    return remaining_tiles


def hide_sondre(grid):
    is_hidden = False
    for row in grid:
        for tile in row:
            if isinstance(tile[0], int) and tile[0] == 0 and not is_hidden:
                if random.randint(1, 50) == 1:
                    tile.append("Sondre")
                    is_hidden = True
    return grid


def main():
    # Pygame setup
    pygame.init()
    pygame.mixer.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(pygame.image.load("Assets/minesweeper/mine.png"))
    clock = pygame.time.Clock()
    fps = 60

    tile_size = 24
    font = pygame.font.SysFont(None, tile_size * 4 // 3)
    grid_w, grid_h = 30, 16
    mines = 99
    flag_mine_difference = 99
    grid = grid_setup((grid_w, grid_h), mines)
    grid = hide_sondre(grid)
    grid_pos = pygame.math.Vector2((120, 200))
    lmb_down = False
    rmb_down = False
    b_down = False
    bosnian_mode = False
    is_dead = False
    face_is_clicked = False
    has_won = False

    # Number colours
    colours = [(0, 0, 255), (0, 100, 0), (255, 0, 0), (100, 0, 100),
               (64, 64, 0), (100, 100, 100), (31, 31, 31), (110, 110, 110)]

    # Loading in background image
    background = pygame.image.load("Assets/minesweeper/background.png")

    # Loading in assets and scaling tile assets to tile size
    tile_revealed_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/tile_revealed.png"), (tile_size, tile_size)).convert_alpha()
    tile_hidden_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/tile_hidden.png"), (tile_size, tile_size)).convert_alpha()
    mine_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/mine.png"), (tile_size, tile_size)).convert_alpha()
    mine_clicked_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/takethel.png"), (tile_size, tile_size)).convert_alpha()
    false_flag_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/youdungoofed.png"), (tile_size, tile_size)).convert_alpha()
    tile_flagged_sprite = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/tile_flagged.png"), (tile_size, tile_size)).convert_alpha()
    tile_sprites = [tile_revealed_sprite, tile_hidden_sprite, mine_sprite,
                    mine_clicked_sprite, false_flag_sprite, tile_flagged_sprite]

    face_sprite = pygame.image.load("Assets/minesweeper/face_normal.png")
    face_clicked_sprite = pygame.image.load(
        "Assets/minesweeper/face_clicked.png")
    face_won_sprite = pygame.image.load("Assets/minesweeper/face_won.png")
    face_dead_sprite = pygame.image.load("Assets/minesweeper/face_dead.png")
    face_sprites = [face_sprite, face_clicked_sprite,
                    face_won_sprite, face_dead_sprite]

    sondre = pygame.transform.smoothscale(pygame.image.load(
        "Assets/minesweeper/nowaysondray.png"), (tile_size, tile_size)).convert_alpha()


    # Main loop
    pygame.mixer.music.load("Assets/minesweeper/minesweep.mp3")
    pygame.mixer.music.play(-1)
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        try:
            remaining_tiles = check_board(grid)
            keys = pygame.key.get_pressed()
            mouse_tile = get_tile_from_mouse(grid, tile_size, grid_pos)
            mouse = pygame.mouse.get_pressed()
            mousepos = pygame.math.Vector2(pygame.mouse.get_pos())
        except pygame.error:
            pygame.quit()
            break

        # WIN
        if remaining_tiles == mines and not is_dead:
            has_won = True

        if is_dead:
            reveal_all_mines(grid)
            if mouse[0] and 442 <= mousepos.x <= 505 and 80 <= mousepos.y <= 143:
                face_is_clicked = True
                grid = grid_setup((grid_w, grid_h), mines)
                grid = hide_sondre(grid)
                flag_mine_difference = mines
                is_dead = False
                has_won = False

        if not is_dead:
            if mouse[0]:
                if not lmb_down:
                    if mouse_tile and grid[mouse_tile[0]][mouse_tile[1]][1] and not grid[mouse_tile[0]][mouse_tile[1]][2]:
                        is_dead, grid = reveal_tile(
                            grid, mouse_tile[0], mouse_tile[1])
                    if mouse_tile and not grid[mouse_tile[0]][mouse_tile[1]][1] and not grid[mouse_tile[0]][mouse_tile[1]][2]:
                        adj_flags = 0
                        for nx, ny in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                            if mouse_tile[1] + nx >= 0 and mouse_tile[1] + nx < len(grid[0]) and mouse_tile[0] + ny >= 0 and mouse_tile[0]+ny < len(grid):
                                if grid[mouse_tile[0]+ny][mouse_tile[1]+nx][2]:
                                    adj_flags += 1
                        if isinstance(grid[mouse_tile[0]][mouse_tile[1]][0], int) and adj_flags == grid[mouse_tile[0]][mouse_tile[1]][0]:
                            for nx, ny in [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]:
                                if mouse_tile[1] + nx >= 0 and mouse_tile[1] + nx < len(grid[0]) and mouse_tile[0] + ny >= 0 and mouse_tile[0]+ny < len(grid):
                                    if not grid[mouse_tile[0]+ny][mouse_tile[1]+nx][2] and grid[mouse_tile[0]+ny][mouse_tile[1]+nx][1]:
                                        if not is_dead:
                                            is_dead, grid = reveal_tile(
                                                grid, mouse_tile[0]+ny, mouse_tile[1]+nx)

                    if 442 <= mousepos.x <= 505 and 80 <= mousepos.y <= 143:
                        face_is_clicked = True
                        grid = grid_setup((grid_w, grid_h), mines)
                        grid = hide_sondre(grid)
                        flag_mine_difference = mines
                        is_dead = False
                        has_won = False
                    else:
                        face_is_clicked = False
                    lmb_down = True
            else:
                face_is_clicked = False
                lmb_down = False

            if mouse[2]:
                if not rmb_down:
                    if mouse_tile:
                        if not grid[mouse_tile[0]][mouse_tile[1]][2] and grid[mouse_tile[0]][mouse_tile[1]][1]:
                            flag_mine_difference -= 1
                            print(flag_mine_difference)
                            grid[mouse_tile[0]][mouse_tile[1]][2] = True
                        elif grid[mouse_tile[0]][mouse_tile[1]][2] and grid[mouse_tile[0]][mouse_tile[1]][1]:
                            flag_mine_difference += 1
                            print(flag_mine_difference)
                            grid[mouse_tile[0]][mouse_tile[1]][2] = False
                    rmb_down = True
            else:
                rmb_down = False

        if keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        if keys[pygame.K_b]:
            if not b_down and not bosnian_mode:
                b_down = True
                bosnian_mode = True
                background = pygame.image.load("Assets/minesweeper/bosnia_bg.png")
                pygame.display.set_caption(
                    "Bosnia 1994 Simulator")  # If you know you know
                pygame.display.set_icon(pygame.image.load(
                    "Assets/minesweeper/takethel.png"))
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/minesweeper/bosnian.mp3")
                pygame.mixer.music.play(-1)
            elif not b_down and bosnian_mode:
                b_down = True
                bosnian_mode = False
                background = pygame.image.load("Assets/minesweeper/background.png")
                pygame.display.set_caption("Minesweeper")
                pygame.display.set_icon(pygame.image.load(
                    "Assets/minesweeper/mine.png"))
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/minesweeper/minesweep.mp3")
                pygame.mixer.music.play(-1)
        else:
            b_down = False

        if keys[pygame.K_r]:
            reveal_all_mines(grid)

        if keys[pygame.K_h]:
            hide_all_mines(grid)

        screen.blit(background, (0, 0))
        draw_grid(screen, grid, tile_size, font, colours,
                  grid_pos, tile_sprites, is_dead, sondre)
        draw_face(screen, face_sprites, face_is_clicked, is_dead, has_won)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
