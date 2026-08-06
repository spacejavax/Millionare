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

companies = [
    {"name": "Bigbanana:", "price": 50, "shares": 0, "button": pygame.Rect(650, 245, 100, 40)},
    {"name": "BubbleUnicorn:", "price": 70, "shares": 0, "button": pygame.Rect(650, 305, 100, 40)},
    {"name": "GummyBear:", "price": 150, "shares": 0, "button": pygame.Rect(650, 365, 100, 40)}
]


async def main():
    cash = 1000
    running = True

    while running:

        for event in pygame.event.get():

           
            if event.type == pygame.QUIT:
                if event.type == pygame.MOUSEBUTTON:
                    for company in companies:
                        if company["button"].collidepoint(event.pos):
                            if cash >= company["price"]:
                                cash -= company["price"]
                                company["shares"] +=1
                running = False

    
        screen.fill((255, 232, 240))

        title = title_font.render(
            "MILLIONAIRE",
            True,
            (215, 75, 125)
        )

        balance = text_font.render(
            f"Cash: ${cash}",
            True,
            (125, 85, 145)
        )

        screen.blit(title, (275, 80))
        screen.blit(balance, (350, 180))

        y_position = 250
        for company in companies:
            company_text = text_font.render(
                f"{company['name']} ${company['price']}",
                True,
                (125, 85, 145)
                )
            shares_text = text_font.render(
                f"Owned: {company['shares']}",
                True,
                (125, 85, 145)
            )
            screen.blit(shares_text, (470, y_position))
            screen.blit(company_text, (180, y_position))
            buy_button = company["button"]
            pygame.draw.rect(
                screen,
                (255, 145, 180),
                buy_button,
                border_radius=12
            )
            buy_text = text_font.render(
                "Buy",
                True,
                (255, 255, 255)
            )

            screen.blit(buy_text, (677, y_position + 2))

            y_position += 60
        

        pygame.display.flip()

        clock.tick(60)


        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())