import pygame
import random

pygame.init()

width, height = 600, 400

bg_color = (255, 255, 255)
snake_color = (0, 102, 0)
food_color = (255, 0, 0)
grid_color = (180, 210, 235)
text_color = (0, 51, 102)
button_color = (50, 153, 213)
button_hover_color = (30, 130, 180)

snake_block = 20
initial_speed = 5
max_speed = 20
speed_increment = 0.5

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Snake Game with Dynamic Speed")

clock = pygame.time.Clock()

font_style = pygame.font.SysFont("comicsansms", 25, bold=True)
score_font = pygame.font.SysFont("comicsansms", 20, bold=True)

highest_score = 0

def show_score(score):
    value = score_font.render(f"Score: {score}  |  High Score: {highest_score}", True, text_color)
    window.blit(value, [10, 10])

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(window, snake_color, [block[0], block[1], snake_block, snake_block], border_radius=8)

def draw_food(x, y):
    pygame.draw.circle(window, food_color, (x + snake_block // 2, y + snake_block // 2), snake_block // 2)

def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(window, button_hover_color, (x, y, width, height), border_radius=8)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(window, button_color, (x, y, width, height), border_radius=8)

    text_surface = font_style.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    window.blit(text_surface, text_rect)

background_image = pygame.image.load(r'C:\Users\Rohan MK\OneDrive\Desktop\8th sem Internship\background.jpg')
background_image = pygame.transform.scale(background_image, (width, height))

def game_over_screen(score):
    global highest_score
    if score > highest_score:
        highest_score = score

    game_over = True
    while game_over:
        window.blit(background_image, (0, 0))
        text = font_style.render("Game Over!", True, text_color)
        window.blit(text, (width // 2 - 80, height // 3))
        show_score(score)

        button_width = 150
        button_height = 50
        button_spacing = 30
        total_width = 2 * button_width + button_spacing

        start_x = (width - total_width) // 2

        draw_button("Try Again", start_x, height // 2, button_width, button_height, game_loop)
        draw_button("Quit", start_x + button_width + button_spacing, height // 2, button_width, button_height, pygame.quit)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

def game_loop():
    global width, height

    game_over = False
    current_speed = initial_speed

    x, y = width // 2, height // 2
    x_change, y_change = 0, 0

    snake_list = []
    length_of_snake = 1

    food_x = random.randint(0, (width // snake_block) - 1) * snake_block
    food_y = random.randint(0, (height // snake_block) - 1) * snake_block

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -snake_block
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = snake_block
                    x_change = 0

        if x >= width or x < 0 or y >= height or y < 0:
            game_over_screen(length_of_snake - 1)
            return

        x += x_change
        y += y_change
        window.blit(background_image, (0, 0))

        draw_food(food_x, food_y)

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_over_screen(length_of_snake - 1)
                return

        draw_snake(snake_list)
        show_score(length_of_snake - 1)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = random.randint(0, (width // snake_block) - 1) * snake_block
            food_y = random.randint(0, (height // snake_block) - 1) * snake_block
            length_of_snake += 1

            if current_speed < max_speed:
                current_speed += speed_increment

        clock.tick(current_speed)

    pygame.quit()
    quit()

game_loop()
 