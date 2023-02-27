import pygame

# Init the game
pygame.init()

# Screen
screen = pygame.display.set_mode((744, 682))

# Map
map = pygame.image.load('../data/map.png')

# Title and icon
pygame.display.set_caption("Pacman")
icon = pygame.image.load('../data/pacman.png')
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load("../data/pacman.png")
playerX = 0
playerY = 0
playerX_change = 1
playerY_change = 1

# functions

def player(x, y):
    screen.blit(playerIMG, (x, y))



# game loop

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(map, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.K_RIGHT:
            


    player(playerX, playerY)
    pygame.display.update()
