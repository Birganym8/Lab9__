# Imports
import pygame, sys
from pygame.locals import *
import random, time

# Initializing Pygame
pygame.init()

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  # Track collected coins

# Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load images
background = pygame.image.load("AnimatedStreet.png")
coin_image = pygame.image.load("coin.png")  # Load coin image

# Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Initial position of the player

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        # Move left
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        
        # Move right
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Move up
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        
        # Move down
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

# Coin class with random weights
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()
        # Coin randomly appears on the road
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, SCREEN_HEIGHT - 150))  
        self.weight = random.randint(1, 5)  # Random weight for the coin (1 to 5)

    def move(self):
        pass  # Coin does not move

# Setting up Sprites        
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Adding a new User event for speed increase
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Increase speed of enemies every second
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))
    
    # Display score and coins
    scores = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 100, 10))

    # Move and redraw all sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Collision check with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Collision check with coins
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += C1.weight  # Increase coins by the weight of the coin
        SCORE += C1.weight  # Add the coin's weight to score
        pygame.mixer.Sound('coin_collect.wav').play()  # Play sound on coin collection
        C1.rect.top = 0  # Reset coin to top of screen
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, SCREEN_HEIGHT - 150))  # New random position
        
        # Increase enemy speed after collecting every 10 coins
        if COINS >= 10:
            SPEED += 1  # Increase enemy speed by 1
            COINS = 0  # Reset coins after every 10 coins

    pygame.display.update()
    FramePerSec.tick(FPS)  # Control the frame rate
