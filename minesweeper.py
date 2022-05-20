import pygame
import math
import sys


def main():
    # Pygame setup
    pygame.init()
    screen_w, screen_h = 960, 720
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Minesweeper")
    clock = pygame.time.Clock()

    # Main loop
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        keys = pygame.key.get_pressed()
            
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()