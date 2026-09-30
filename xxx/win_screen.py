import pygame
from config import WIDTH, HEIGHT
from ui_components import draw_button
from renderer import get_victory_img

def render_win_screen(screen):
    # Заливаємо весь екран чорним фоном
    screen.fill((0, 0, 0))
    
    # 1. Верхня половина екрана для картинки перемоги
    victory_img = get_victory_img((WIDTH, int(HEIGHT * 0.45)))
    if victory_img:
        img_x = (WIDTH - victory_img.get_width()) // 2
        screen.blit(victory_img, (img_x, 30))
    
    # 2. Нижня половина екрана для кнопок
    btn_w = 280
    btn_x = (WIDTH - btn_w) // 2
    draw_button(screen, "Ще раз", btn_x, 320, btn_w, 45)
    draw_button(screen, "Новий граф", btn_x, 380, btn_w, 45)
    draw_button(screen, "Головне меню", btn_x, 440, btn_w, 45)