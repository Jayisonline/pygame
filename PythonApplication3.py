import pygame
import random2
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('planet.jpg')

#sound
mixer.music.load('Robot-monster-01.wav')
mixer.music.play(-1)


#sound



# Title and icon
pygame.display.set_caption("Space Fighter")
icon = pygame.image.load('blackhole.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load('tank.png')
playerX = 370
playerY = 480
playerX_change = 0



#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = [] 
enemyX_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('ghost.png'))
    enemyX.append(random2.randint(0, 736))
    enemyY.append(random2.randint(50, 150))
    enemyY_change.append(40)
    enemyX_change.append(0.3)


#ready = bullet we cant see
#fire = fires bullet
bulletImg = pygame.image.load('bullet (1).png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"


scores = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)


testX = 10
testY = 10

def show_scores(x,y):
    score = font.render("score:"+str(scores), True, (255, 255, 255))
    screen.blit(score, (x,y))


def player(x,y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16, y+10))
    
def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False

def game_over():
    over = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over, (200, 250))


running = True
while running :

    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #key movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('Flash-laser-01.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(playerX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX>= 736:
        playerX = 736
    

    #enemy movement
    for i in range(num_of_enemy):


        #game over
        if enemyY[i] > 450:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over()
            break






        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736 :
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            scores += 1
            enemyX[i] = random2.randint(0, 736)
            enemyY[i] = random2.randint(50, 150)
        
        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change


        
    
    
    player(playerX, playerY)
    show_scores(testX, testY)
    pygame.display.update()
