import pygame
import math

# Настройки окна
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Инициализация
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape Drawing")
clock = pygame.time.Clock()

# Переменные
start_pos = None
drawing = False
shape_type = "square"  # default
shapes = []  # список нарисованных фигур
erase_mode = False  # режим стерки

def draw_square(surface, start, end, color):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    rect = pygame.Rect(x1, y1, side, side)
    rect.normalize()
    pygame.draw.rect(surface, color, rect, 2)

def draw_right_triangle(surface, start, end, color):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x1, y2), (x2, y2)]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, start, end, color):
    x1, y1 = start
    x2, y2 = end
    base = math.hypot(x2 - x1, y2 - y1)
    height = (math.sqrt(3)/2) * base
    mid_x = (x1 + x2) / 2
    top = (mid_x, y1 - height)
    pygame.draw.polygon(surface, color, [(x1, y1), (x2, y1), top], 2)

def draw_rhombus(surface, start, end, color):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    points = [
        (mid_x, y1),
        (x2, mid_y),
        (mid_x, y2),
        (x1, mid_y)
    ]
    pygame.draw.polygon(surface, color, points, 2)

# Главный цикл
run = True
while run:
    clock.tick(FPS)
    win.fill(WHITE)

    # Отрисовка сохранённых фигур
    for shape in shapes:
        typ, start, end = shape
        if typ == "square":
            draw_square(win, start, end, BLACK)
        elif typ == "right_triangle":
            draw_right_triangle(win, start, end, BLACK)
        elif typ == "equilateral_triangle":
            draw_equilateral_triangle(win, start, end, BLACK)
        elif typ == "rhombus":
            draw_rhombus(win, start, end, BLACK)

    # Отрисовка текущей фигуры при удержании мыши
    if drawing and start_pos:
        current_pos = pygame.mouse.get_pos()
        if shape_type == "square":
            draw_square(win, start_pos, current_pos, BLUE)
        elif shape_type == "right_triangle":
            draw_right_triangle(win, start_pos, current_pos, BLUE)
        elif shape_type == "equilateral_triangle":
            draw_equilateral_triangle(win, start_pos, current_pos, BLUE)
        elif shape_type == "rhombus":
            draw_rhombus(win, start_pos, current_pos, BLUE)

    # Если режим стерки, рисуем белым
    if erase_mode and drawing and start_pos:
        current_pos = pygame.mouse.get_pos()
        draw_square(win, start_pos, current_pos, WHITE)  # Пример с квадратом для стирания

    pygame.display.update()

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Нажатие мыши — начинаем рисовать
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_pos = event.pos
            drawing = True

        # Отпускание мыши — сохраняем фигуру
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            end_pos = event.pos
            if start_pos and end_pos:
                if erase_mode:
                    shapes = [shape for shape in shapes if not pygame.Rect(shape[1], (abs(shape[2][0]-shape[1][0]), abs(shape[2][1]-shape[1][1]))).colliderect(pygame.Rect(start_pos, (abs(end_pos[0]-start_pos[0]), abs(end_pos[1]-start_pos[1]))))]
                else:
                    shapes.append((shape_type, start_pos, end_pos))
            drawing = False
            start_pos = None

        # Нажатие клавиш — выбор фигуры и включение стерки
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                shape_type = "square"
            elif event.key == pygame.K_r:
                shape_type = "right_triangle"
            elif event.key == pygame.K_e:
                shape_type = "equilateral_triangle"
            elif event.key == pygame.K_h:
                shape_type = "rhombus"
            elif event.key == pygame.K_ESCAPE:  # Выход из режима стерки
                erase_mode = not erase_mode

pygame.quit()
