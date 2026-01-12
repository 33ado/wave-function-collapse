import pygame

pygame.init()

# global variables
width = 600
height = 600
display = pygame.display.set_mode((width, height))


def main():
    # game loop
    loop = True
    while loop:
        display.fill((0, 0, 0))
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    hover_toggle = not hover_toggle

                if event.key == pygame.K_q:
                    loop = False
                    exit()

        # update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
