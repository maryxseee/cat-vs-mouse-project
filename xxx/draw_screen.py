import pygame
from config import WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, FONT
from ui_components import draw_button

def render_draw_screen(screen):
    screen.fill(BG_COLOR)
    title = FONT.render("НІЧИЧІЯ! Дороги розійшлися.", True, (234, 179, 8))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
    
    draw_button(screen, "Спробувати ще раз", WIDTH // 2 - 100, 280, 200, 40)
    draw_button(screen, "Новий граф", WIDTH // 2 - 100, 340, 200, 40)
    draw_button(screen, "Головне меню", WIDTH // 2 - 100, 400, 200, 40)