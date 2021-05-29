import pygame
import random
import math
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True

player_icon = pygame.image.load("spaceship.png")

clock = pygame.time.Clock()

background_image = pygame.image.load("background.png")


def player_function(x_position, y_position):
    screen.blit(player_icon, (x_position, y_position))


# Background music
pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

# fruit = ["mango", "banana"]
enemy_image = []
enemy_x_position = []
enemy_y_position = []
enemy_x_position_change = []
enemy_y_position_change = []
no_of_enemies = 6

for i in range(no_of_enemies):
    enemy_image.append(pygame.image.load("pixelated-alien.png"))
    enemy_x_position.append(random.randint(0, 740))
    enemy_y_position.append(random.randint(50, 150))
    enemy_x_position_change.append(2)
    enemy_y_position_change.append(150)

enemy_icon = pygame.image.load("pixelated-alien.png")


def enemy_function(x_position, y_position, k):
    screen.blit(enemy_image[k], (x_position, y_position))


initial_enemy_x_position = random.randint(0, 740)
initial_enemy_y_position = random.randint(50, 150)

initial_x_position = 370
initial_y_position = 480

x_rightmost_edge = 730
x_leftmost_edge = 0
position_change = 0
enemy_position_change = 2

bullet_image = pygame.image.load("bullet.png")
bullet_x_position = initial_x_position
bullet_y_position = 480

# bullet_state -> ready / fire
bullet_state = "ready"
bullet_y_position_change = 0

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

game_over_font = pygame.font.Font("freesansbold.ttf", 60)

def show_score(font_x, font_y):
    score = font.render("Score: " + str(score_value), True, (0, 0, 0))
    screen.blit(score, (font_x, font_y))


def bullet_show(bullet_x_position, bullet_y_position):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (bullet_x_position + 16, bullet_y_position + 10))


# int = 3, 4, 5, 10, decimal = 1.3, 2,2, string = "Nikhil", "hello"

# Control + alt + L - to format our code - so that code looks beautiful
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


game_over = 0


def check_if_game_over(enemy_x_position, enemy_y_position):
    global game_over
    if enemy_y_position > 450:
        game_over = 1


def display_game_over_screen():
    text_rotate_degrees = 0

    t_end = time.time() + 10
    while time.time() < t_end:
        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))
        font = pygame.font.SysFont('Calibri', 100, True, False)
        over = font.render("Game Over", True, (0, 0, 0))
        over = pygame.transform.rotate(over, text_rotate_degrees)
        text_rotate_degrees += 2
        screen.blit(over, [200, 150])
        pygame.display.flip()
        clock.tick(60)

    exit(1)


while running:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            position_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                position_change = -2
            if event.key == pygame.K_RIGHT:
                position_change = 2

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x_position = initial_x_position
                    bullet_show(bullet_x_position, bullet_y_position)

    initial_x_position = initial_x_position + position_change

    if initial_x_position > x_rightmost_edge:
        initial_x_position = x_rightmost_edge

    if initial_x_position < x_leftmost_edge:
        initial_x_position = x_leftmost_edge

    for i in range(no_of_enemies):
        if enemy_x_position[i] > x_rightmost_edge:
            enemy_x_position_change[i] = -2
            enemy_y_position[i] = enemy_y_position[i] + enemy_y_position_change[i]

        if enemy_x_position[i] < x_leftmost_edge:
            enemy_x_position_change[i] = 2
            enemy_y_position[i] = enemy_y_position[i] + enemy_y_position_change[i]

        enemy_x_position[i] = enemy_x_position[i] + enemy_x_position_change[i]

        collision = is_collision(enemy_x_position[i], enemy_y_position[i], bullet_x_position, bullet_y_position)

        if collision is True:
            explosion_sound = pygame.mixer.Sound("explosion.wav")
            explosion_sound.play()
            enemy_x_position[i] = random.randint(0, 740)
            enemy_y_position[i] = random.randint(50, 150)
            bullet_state = "ready"
            bullet_y_position = 480
            score_value = score_value + 1

        check_if_game_over(enemy_x_position[i], enemy_y_position[i])

        if game_over == 1:
            display_game_over_screen()

        enemy_function(enemy_x_position[i], enemy_y_position[i], i)

    player_function(initial_x_position, initial_y_position)

    if bullet_y_position <= 0:
        bullet_state = "ready"
        bullet_y_position = 480

    if bullet_state == "fire":
        bullet_y_position = bullet_y_position - 6
        bullet_show(bullet_x_position, bullet_y_position)

    show_score(10, 10)
    pygame.display.update()
