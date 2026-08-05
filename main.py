import asyncio
import pygame

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Millionaire")

clock = pygame.time.Clock()

title_font = pygame.font.Font(None, 64)
text_font = pygame.font.Font(None, 34)


async def main():
    running = True

    while running:

        for event in pygame.event.get():

           
            if event.type == pygame.QUIT:
                running = False

    
        screen.fill((255, 232, 240))

        title = title_font.render(
            "MILLIONAIRE",
            True,
            (215, 75, 125)
        )

        balance = text_font.render(
            "Cash: $1,000",
            True,
            (125, 85, 145)
        )

        screen.blit(title, (275, 80))
        screen.blit(balance, (350, 180))

        pygame.display.flip()

        clock.tick(60)


        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())