import asyncio
import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Millionaire")

clock = pygame.time.Clock()

title_font = pygame.font.Font(None, 64)
text_font = pygame.font.Font(None, 34)

companies = [
    {"name": "Bigbanana:", "price": 50, "shares": 0, "button": pygame.Rect(610, 245, 90, 42), "sell_button": pygame.Rect(715, 245, 90, 42)},
    {"name": "BubbleUnicorn:", "price": 70, "shares": 0, "button": pygame.Rect(610, 305, 90, 42), "sell_button": pygame.Rect(715, 305, 90, 42)},
    {"name": "GummyBear:", "price": 150, "shares": 0, "button": pygame.Rect(610, 365, 90, 42), "sell_button": pygame.Rect(715, 365, 90, 42)}
]

PRICE_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(PRICE_UPDATE, 3000)
async def main():
    cash = 1000
    day = 1
    MAX_DAYS = 30
    market_open = True
    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                            
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    for company in companies:
                        if company["button"].collidepoint(event.pos):
                            if cash >= company["price"]:
                                cash -= company["price"]
                                company["shares"] += 1
                        elif company["sell_button"].collidepoint(event.pos):
                            if company["shares"] > 0:
                                cash += company["price"]
                                company["shares"] -= 1
            elif event.type == PRICE_UPDATE:
                for company in companies:
                    price_change = random.randint(-15, 15)
                    company["price"] += price_change
                    if company["price"] < 5:
                        company["price"] = 5
                day += 1
                if day > MAX_DAYS:
                    day = MAX_DAYS
                    market_open = False  

    
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
        day_text = text_font.render(
            f"Day: {day}/{MAX_DAYS}",
            True,
            (125, 85, 145)
        )
        screen.blit(day_text, (60, 180))
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
            sell_button = company["sell_button"]
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

            buy_text_rect = buy_text.get_rect(center=buy_button.center)
            screen.blit(buy_text, buy_text_rect)

          
            pygame.draw.rect(
                screen,
                (180, 150, 220),
                sell_button,
                border_radius=12
            )

            sell_text = text_font.render(
                "sell",
                True,
                (255, 255, 255)
            )

            sell_text_rect = sell_text.get_rect(center=sell_button.center)
            screen.blit(sell_text, sell_text_rect)

            y_position += 60
        

        pygame.display.flip()

        clock.tick(60)


        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())