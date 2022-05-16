import math
import pygame
import sys

# Class Setup
class Tile:
    def __init__(self, width, grid_pos):
        self.tile_state = None
        self.grid_pos = grid_pos
        self.width = width
        self.x = grid_pos[0]*self.width + 180
        self.y = grid_pos[1]*self.width + 60


    def draw(self, screen, font):
        x, y = pygame.mouse.get_pos()
        if self.tile_state == None:
            if self.x < x < (self.x + 200):
                if self.y < y < (self.y + 200):
                    pygame.draw.rect(screen, "#303030", (self.x, self.y, 200, 200))
        else:
            text = font.render(str(self.tile_state), True, "white")
            textRect = text.get_rect()
            textRect.center = (self.x + 100, self.y + 100)
            screen.blit(text, textRect)


# Functions
def is_equal(list):
    if list[0] != None:
        checker = list[0]
        for item in list:
            if item != checker:
                return False
        return True


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
    

def change_turn(turn):
    if turn == "X":
        turn = "O"
    else:
        turn = "X"
    return turn


def check_winner(grid):
    # Horisontale linjer
    for row in grid:
        tmplist = []
        for tile in row:
            tmplist.append(tile.tile_state)
        if is_equal(tmplist):
            return True

    for i in range(len(grid)):
        tmplist = []
        for j in range(len(grid)):
            tmplist.append(grid[j][i].tile_state)
        if is_equal(tmplist):
            return True
    
    tmplist = []
    for i in range(len(grid)):
        tmplist.append(grid[i][i].tile_state)
    if is_equal(tmplist):
            return True
    
    tmplist = []
    for i in range(len(grid)):
        tmplist.append(grid[i][-1-i].tile_state)
    if is_equal(tmplist):
            return True

    return False

def main():
    # Pygame setup
    pygame.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Tic Tac Toe")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Comic Sans", 200)

    RESET = pygame.USEREVENT
    WIN = pygame.USEREVENT + 1
    DRAW = pygame.USEREVENT + 2

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
                        if get_tile(grid).tile_state == None:
                            get_tile(grid).tile_state = turn
                            if check_winner(grid):
                                winner = turn
                                pygame.event.post(pygame.event.Event(WIN))
                            else:
                                turn = change_turn(turn)
                                if empty_tiles > 1:
                                    empty_tiles -= 1
                                    print(empty_tiles)
                                else:
                                    pygame.event.post(pygame.event.Event(DRAW))
            
            if event.type == RESET:
                grid = grid_setup()
                turn = "X"
                winner = None
                empty_tiles = 9
                can_place_tiles = True
                write = False
            
            if event.type == DRAW:
                can_place_tiles = False
                text = font.render(str(f"Draw!"), True, "white")
                textRect = text.get_rect()
                textRect.center = (screen_w / 2, screen_h / 2)
                write = True
                print("draw!")
            
            if event.type == WIN:
                can_place_tiles = False
                text = font.render(str(f"{winner} Wins!"), True, "white")
                textRect = text.get_rect()
                textRect.center = (screen_w / 2, screen_h / 2)
                write = True
                print(winner, "won!")

        # Eventual logic code goes here

        # Rendering Code
        screen.fill("#282828")

        for row in grid:
                    for tile in row:
                        tile.draw(screen, font)

        pygame.draw.line(screen, "black", (380, 60), (380, 660), 2)
        pygame.draw.line(screen, "black", (580, 60), (580, 660), 2)
        pygame.draw.line(screen, "black", (180, 260), (780, 260), 2)
        pygame.draw.line(screen, "black", (180, 460), (780, 460), 2)

        if write:
            pygame.draw.rect(screen, "gray", ((screen_w / 2) - 300, (screen_h / 2) - 150, 600, 300), border_radius=50)
            screen.blit(text, textRect)
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
