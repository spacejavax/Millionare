import asyncio #pygbag
import pygame #game window, buttons, text
import random #unpredictable price changes

pygame.init()

WIDTH = 900
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Millionaire")

clock = pygame.time.Clock()

title_font = pygame.font.Font(None, 54)
heading_font = pygame.font.Font(None, 30)
text_font = pygame.font.Font(None, 26)
small_font = pygame.font.Font(None, 21)

BACKGROUND = (250, 244, 248)
WHITE = (255, 255, 255)
DARK_PURPLE = (81, 60, 92)
PINK = (238, 112, 157)
LIGHT_PINK = (255, 220, 233)
PURPLE = (155, 125, 205)
GREEN = (55, 174, 112)
RED = (220, 82, 116)
GRAY = (132, 119, 137)
SHADOW = (230, 218, 226)

companies = [
    {"name": "Bigbanana:", "emoji": ":P",  "price": 50, "shares": 0, "risk": 5, "change": 0, "history": [50], "button": pygame.Rect(610, 245, 90, 42), "sell_button": pygame.Rect(715, 245, 90, 42)},
    {"name": "BubbleUnicorn:", "emoji": ":D", "price": 70, "shares": 0, "risk": 15, "change": 0, "history": [70],"button": pygame.Rect(610, 305, 90, 42), "sell_button": pygame.Rect(715, 305, 90, 42)},
    {"name": "GummyBear:",  "emoji": ":3", "price": 150, "shares": 0, "risk": 40, "change": 0, "history": [150], "button": pygame.Rect(610, 365, 90, 42), "sell_button": pygame.Rect(715, 365, 90, 42)}
]

PRICE_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(PRICE_UPDATE, 20000)

def draw_button(button, color, label):
    pygame.draw.rect(
        screen,
        color,
        button,
        border_radius=10
    )
    button_text = text_font.render(
        label,
        True,
        WHITE
    )
    text_rect = button_text.get_rect(center=button.center)
    screen.blit(button_text, text_rect)

def draw_price_graph(history, x, y, width, height):
    if len(history) < 2:
        return
    lowest_price = min(history)
    highest_price = max(history)
    price_range = highest_price - lowest_price

    if price_range == 0:
        price_range = 1
    points = []

    space_between_points = width / (len(history) -1) #space between dots on graph

    index = 0 #first graph dot at 0

    for price in history: #goes through every price in history
        point_x = x + index * space_between_points
        index += 1 #next dot moves more to the right
        point_y = (y + height -((price - lowest_price) / price_range) * height)

        points.append((point_x, point_y))

    if history[-1] >= history[0]:
        graph_color = GREEN
    else:
        graph_color = RED
    pygame.draw.lines(
        screen,
        graph_color,
        False,
        points,
        3
    )


async def main():
    cash = 1000
    day = 1
    MAX_DAYS = 10
    market_open = True
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                            
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if market_open:
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
                if market_open:
                    for company in companies:
                        price_change = random.randint(-company["risk"], company["risk"])
                        company["change"] = price_change
                        company["price"] += price_change
                        if company["price"] < 5:
                            company["price"] = 5
                        company["history"].append(company["price"])
                day += 1
                if day > MAX_DAYS:
                    day = MAX_DAYS
                    market_open = False
        portfolio_value = sum(
            company["price"] * company["shares"]
            for company in companies)  

        total_wealth = cash + portfolio_value

        screen.fill(BACKGROUND)
        title = title_font.render(
                "Millionaire",
                True,
                DARK_PURPLE
            )
        subtitle = small_font.render(
                "Build your kawai investment portfolio:)",
                True,
                GRAY
            )
        screen.blit(title, (55, 28))
        screen.blit(subtitle, (57, 75))
        day_badge = pygame.Rect(720, 35, 125, 45)
        pygame.draw.rect(
                screen,
                LIGHT_PINK,
                day_badge,
                border_radius=20
            )
        day_text = text_font.render(
                f"Day {day}/{MAX_DAYS}",
                True,
                DARK_PURPLE
            )
        day_text_rect = day_text.get_rect(center=day_badge.center)
        screen.blit(day_text, day_text_rect)

        summary_shadow = pygame.Rect(60, 116, 780, 84)
        summary_card = pygame.Rect(60, 111, 780, 84)

        pygame.draw.rect(
                screen,
                SHADOW,
                summary_shadow,
                border_radius=18
            )

        pygame.draw.rect(
                screen,
                WHITE,
                summary_card,
                border_radius=18
            )
    
        cash_label = small_font.render("AVAILABLE CASH", True, GRAY)
        cash_text = heading_font.render(f"${cash}", True, DARK_PURPLE)

        portfolio_label = small_font.render("INVESTED", True, GRAY)
        portfolio_text = small_font.render(f"${portfolio_value}", True, DARK_PURPLE)

        wealth_label = small_font.render("TOTAL WEALTH", True, GRAY)
        wealth_text = heading_font.render(f"${total_wealth}", True, GREEN)
        screen.blit(cash_label, (95, 128))
        screen.blit(cash_text, (95, 153))
        screen.blit(portfolio_label, (355, 128))
        screen.blit(portfolio_text, (355, 153))
        screen.blit(wealth_label, (610, 128))
        screen.blit(wealth_text, (610, 153))

        screen.blit(small_font.render("COMPANY", True, GRAY), (95,215))
        screen.blit(small_font.render("PRICE", True, GRAY), (330, 215))
        screen.blit(small_font.render("CHANGE", True, GRAY), (420, 215))
        screen.blit(small_font.render("OWNED", True, GRAY), (525, 215))
        screen.blit(small_font.render("TREND", True, GRAY), (575, 215))

        card_y = 235
        for company in companies:
            shadow = pygame.Rect(65, card_y + 5, 770, 90)
            card = pygame.Rect(65, card_y, 770, 90)
            pygame.draw.rect(
                screen,
                SHADOW,
                shadow,
                border_radius=17
            )

            pygame.draw.rect(
                screen,
                WHITE,
                card,
                border_radius=17
            )

            icon_center = (100, card_y + 45)

            pygame.draw.circle(
                screen,
                LIGHT_PINK,
                icon_center,
                25
            )

            company_emoji = heading_font.render(company["emoji"], True, PINK)


            emoji_rect = company_emoji.get_rect(center=icon_center)
            screen.blit(company_emoji, emoji_rect)

            name_text= text_font.render(company["name"], True, DARK_PURPLE)

            risk_text=small_font.render(f"Risk:{company['risk']}", True, GRAY)
            price_text = text_font.render(f"${company['price']}", True, DARK_PURPLE)

            if company["change"] >= 0:
                change_color = GREEN
                change_value = f"+${company['change']}"
            else:
                change_color = RED
                change_value = f"-${abs(company['change'])}"
            change_text = text_font.render(change_value, True, change_color)
            owned_text = text_font.render(str(company["shares"]), True, DARK_PURPLE)
            screen.blit(name_text, (140, card_y + 23))
            screen.blit(risk_text, (140, card_y + 53))
            screen.blit(price_text, (330, card_y + 34))
            screen.blit(change_text, (420, card_y + 34))
            screen.blit(owned_text, (540, card_y + 34))

            company["button"].update(
                    650,
                    card_y + 26,
                    75,
                    38
                    )
            
            company["sell_button"].update(
                    735,
                    card_y + 26,
                    75,
                    38
                    )
            
            draw_button(
                    company["button"],
                    PINK if market_open else GRAY,
                    "Buy"
                    )
            
            draw_button(
                    company["sell_button"],
                    PURPLE if market_open else GRAY,
                    "Sell"
                    )
            
            

            card_y +=110



        pygame.display.flip()

        clock.tick(60)


        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())