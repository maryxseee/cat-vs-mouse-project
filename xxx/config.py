import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT_LARGE = pygame.font.SysFont(None, 48)

# Кольорова палітра у стилістиці «Кіт і Миша» (темний естетичний фон)
BG_COLOR = (15, 23, 42)          # Глибокий темно-синій
TEXT_COLOR = (241, 245, 249)     # Світло-сірий текст
BUTTON_BG = (51, 65, 85)         # Колір кнопок
BUTTON_HOVER = (71, 85, 105)     # Колір кнопок при наведенні

EDGE_YELLOW = (234, 179, 8)      # Жовтий місток
EDGE_ORANGE = (249, 115, 22)     # Оранжевий місток

NODE_CAT = (59, 130, 246)        # Синій (Кіт)
NODE_MOUSE = (239, 68, 68)       # Червоний (Миша)
NODE_WIN = (34, 197, 94)         # Зелений (Перемога)

WIDTH, HEIGHT = 800, 600
BG_COLOR = (15, 23, 42)      # Темний стиль кіберпанку
TEXT_COLOR = (248, 250, 252)  # Світлий текст
NODE_CAT = (59, 130, 246)     # Синій (Кіт)
NODE_MOUSE = (239, 68, 68)    # Червоний (Миша)
NODE_WIN = (168, 85, 247)     # Яскраво-фіолетовий для перемоги

import pygame
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 18)

# Шрифти
FONT = pygame.font.SysFont("Arial", 28, bold=True)
FONT_SMALL = pygame.font.SysFont("Arial", 18)
