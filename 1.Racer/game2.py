# Импорты
import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Создание цветов
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Другие переменные, используемые в программе
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  # Подсчет собранных монет

# Настройка шрифтов
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Загрузка изображений
background = pygame.image.load("AnimatedStreet.png")
coin_image = pygame.image.load("coin.png")  # Загрузка изображения монеты

# Создание белого экрана
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Класс врага
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

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)  # Начальная позиция игрока

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        # Движение влево
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        
        # Движение вправо
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Движение вверх
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        
        # Движение вниз
        if self.rect.bottom < SCREEN_HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

# Класс монеты со случайным весом
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()
        # Монета случайно появляется на дороге
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, SCREEN_HEIGHT - 150))  
        self.weight = random.randint(1, 5)  # Случайный вес монеты (от 1 до 5)

    def move(self):
        pass  # Монета не двигается

# Настройка спрайтов        
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Создание групп спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Добавление нового пользовательского события для увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5  # Увеличивать скорость врагов каждую секунду
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))
    
    # Отображение очков и монет
    scores = font_small.render(f"Очки: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Монеты: {COINS}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_display, (SCREEN_WIDTH - 100, 10))

    # Движение и отрисовка всех спрайтов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверка столкновения с врагами
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

    # Проверка столкновения с монетами
    if pygame.sprite.spritecollideany(P1, coins):
        COINS += C1.weight  # Увеличить количество монет на вес монеты
        SCORE += C1.weight  # Добавить вес монеты к очкам
        pygame.mixer.Sound('coin_collect.wav').play()  # Проиграть звук при сборе монеты
        C1.rect.top = 0  # Сбросить монету наверх экрана
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(50, SCREEN_HEIGHT - 150))  # Новая случайная позиция
        
        # Увеличить скорость врагов после сбора каждых 10 монет
        if COINS >= 10:
            SPEED += 1  # Увеличить скорость врагов на 1
            COINS = 0  # Обнулить счетчик монет после каждых 10

    pygame.display.update()
    FramePerSec.tick(FPS)  # Контроль частоты кадров
