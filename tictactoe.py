import math
import pygame
import sys


# Classes
class Tile:
    def __init__(self, width, grid_pos):
        self.tile_state = None
        self.grid_pos = grid_pos
        self.width = width
        self.x = grid_pos[0] * self.width + 180
        self.y = grid_pos[1] * self.width + 60

    def draw(self, screen, font):
        x, y = pygame.mouse.get_pos()
        if self.tile_state is None:
            if self.x < x < (self.x + 200):
                if self.y < y < (self.y + 200):
                    pygame.draw.rect(
                        screen, "#303030", (self.x, self.y, 200, 200))
        else:
            text = font.render(str(self.tile_state), True, "white")
            textRect = text.get_rect()
            textRect.center = (self.x + 100, self.y + 100)
            screen.blit(text, textRect)


# Might add an opponent later, with different difficulties (e.g Pure
# Randomness, Some Competency etc.)
class Opponent:
    def __init__(self, difficulty):
        self.difficulty = difficulty


# Function for checking if a list is equal
def is_equal(list):
    if list[0] is not None:
        checker = list[0]
        for item in list:
            if item != checker:
                return False
        return True


# Gets the tile equivalent of the mouse position
def get_tile(grid):
    x, y = pygame.mouse.get_pos()
    x -= 180
    x /= 200
    y -= 60
    y /= 200
    x = math.floor(x)
    y = math.floor(y)
    tile = grid[y][x]
    return tile


# Grid Setup
def grid_setup():
    grid = []
    for i in range(3):
        grid.append([])
        for j in range(3):
            grid[i].append(Tile(200, (j, i)))
    return grid


# Changes the turn from X to O
def change_turn(turn):
    if turn == "X":
        turn = "O"
    else:
        turn = "X"
    return turn


# Function that checks every winning situation
def check_winner(grid):
    # Horizontal Lines
    for row in grid:
        tmplist = []
        for tile in row:
            tmplist.append(tile.tile_state)
        if is_equal(tmplist):
            return True

    # Vertical Lines
    for i in range(len(grid)):
        tmplist = []
        for j in range(len(grid)):
            tmplist.append(grid[j][i].tile_state)
        if is_equal(tmplist):
            return True

    # Diagonal
    tmplist = []
    for i in range(len(grid)):
        tmplist.append(grid[i][i].tile_state)
    if is_equal(tmplist):
        return True

    # Reverse Diagonal
    tmplist = []
    for i in range(len(grid)):
        tmplist.append(grid[i][-1 - i].tile_state)
    if is_equal(tmplist):
        return True

    return False


# Main Function
def main():
    # Pygame Setup
    pygame.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Comic Sans", 200)
    font_2 = pygame.font.SysFont("Comic Sans", 24)

    # Events for the different results
    RESET = pygame.USEREVENT
    WIN = pygame.USEREVENT + 1
    DRAW = pygame.USEREVENT + 2

    # Clears board and starts loop
    pygame.event.post(pygame.event.Event(RESET))
    running = True

    while running:
        # Main event loop
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    pygame.event.post(pygame.event.Event(RESET))

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if can_place_tiles:
                    x, y = pygame.mouse.get_pos()
                    if 180 <= x <= 780 and 60 <= y <= 660:
                        if get_tile(grid).tile_state is None:
                            get_tile(grid).tile_state = turn
                            if check_winner(grid):
                                winner = turn
                                pygame.event.post(pygame.event.Event(WIN))
                            else:
                                turn = change_turn(turn)
                                if empty_tiles > 1:
                                    empty_tiles -= 1
                                else:
                                    pygame.event.post(pygame.event.Event(DRAW))
            # Resetting the board
            if event.type == RESET:
                grid = grid_setup()
                turn = "X"
                winner = None
                empty_tiles = 9
                can_place_tiles = True
                write = False

            # Processing a draw, writing it to the screen
            if event.type == DRAW:
                can_place_tiles = False
                text = font.render(str(f"Draw!"), True, "black")
                textRect = text.get_rect()
                textRect.center = (screen_w / 2, screen_h / 2 - 25)
                write = True

            # Processing a win, writing it to the screen
            if event.type == WIN:
                can_place_tiles = False
                text = font.render(str(f"{winner} Wins!"), True, "black")
                textRect = text.get_rect()
                textRect.center = (screen_w / 2, screen_h / 2 - 25)
                write = True

        # Rendering Code
        try:
            screen.fill("#282828")
        except Exception:
            break

        for row in grid:
            for tile in row:
                tile.draw(screen, font)

        # Draws the lines that make up the board
        pygame.draw.line(screen, "black", (380, 60), (380, 660), 2)
        pygame.draw.line(screen, "black", (580, 60), (580, 660), 2)
        pygame.draw.line(screen, "black", (180, 260), (780, 260), 2)
        pygame.draw.line(screen, "black", (180, 460), (780, 460), 2)

        # Writes information to the centre of the screen
        if write:
            pygame.draw.rect(
                screen,
                "gray",
                ((screen_w / 2) - 400,
                 (screen_h / 2) - 150,
                    800,
                    300),
                border_radius=50)
            screen.blit(text, textRect)
            text_2 = font_2.render("Press Space to play again", True, "black")
            textRect_2 = text_2.get_rect()
            textRect_2.center = (screen_w / 2, screen_h / 2 + 100)
            screen.blit(text_2, textRect_2)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
    sys.exit()
