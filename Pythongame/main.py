import pygame
import random
import math


# Intialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('data/background.png')

# Title and Icon
pygame.display.set_caption(("Space Invaders"))
icon = pygame.image.load('data/ufo.png')
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load('data/space-ship.png')
playerX = 370
playerY = 480
playerX_change = 0
playeRX_CHANGE = 3

# Enemy
speed = 2.8

enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyIMG.append(pygame.image.load('data/enemy1.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(speed)
    enemyY_change.append(40)

# Bullet
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletIMG = pygame.image.load('data/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 8
bullet_state = "ready"

# score

score_value = 0
font = pygame.font.Font('data/freesansbold.ttf', 32)

textX = 10
textY = 10

# Game over Text

over_font = pygame.font.Font('data/freesansbold.ttf', 80)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def isCollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if distance < 27:

        return True
    else:
        return False


def speedValue(score):
    global speed
    movement = speed
    if score >= 10:
        movement = speed * 1.25
    if score >= 20:
        movement = speed * 1.5625

    if score >= 30:
        movement = speed ** 1.5

    if score >= 40:
        movement = speed ** 1.75

    if score >= 60:
        movement = speed ** 2.25
    return movement


def enemyMove(enemyX, i):
    move = speedValue(score_value)

    if enemyX[i] <= 0:
        enemyX_change[i] = move
        enemyY[i] += enemyY_change[i]

    elif enemyX[i] >= 736:
        enemyX_change[i] = -move
        enemyY[i] += enemyY_change[i]


def playerMove(score):
    global score_value
    playermove = playeRX_CHANGE
    if score >= 15:
        playermove = playeRX_CHANGE + 1.25

    if score >= 30:
        playermove = playeRX_CHANGE + 2.5

    if score >= 60:
        playermove = playeRX_CHANGE + 3.25

    return playermove


# game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= playerMove(score_value)

            if event.key == pygame.K_RIGHT:
                playerX_change += playerMove(score_value)

            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        enemyMove(enemyX, i)

        # Collision
        collision = isCollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
