import pygame
import os
from config import WIDTH, HEIGHT
from renderer import get_bg_sky, get_title_img
from ui_components import draw_button

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def get_pause_bg(size=(440, 440)):
    path = os.path.join(ASSETS_DIR, "пауза.PNG")
    if os.path.exists(path):
        img = pygame.image.load(path)
        if pygame.display.get_surface() is not None:
            img = img.convert_alpha()
        return pygame.transform.scale(img, size)
    return None

def render_main_menu(screen):
    bg_sky = get_bg_sky()
    if bg_sky:
        screen.blit(bg_sky, (0, 0))
    else:
        screen.fill((30, 144, 255))
    
    title_img = get_title_img((480, 180))
    if title_img:
        screen.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, 40))
    
    # Зробили кнопки ширшими (340 пікселів замість 300) та відцентрували
    btn_w, btn_h = 340, 48
    btn_x = (WIDTH - btn_w) // 2
    
    draw_button(screen, "Маленький", btn_x, 300, btn_w, btn_h)
    draw_button(screen, "Середній", btn_x, 362, btn_w, btn_h)
    draw_button(screen, "Великий", btn_x, 424, btn_w, btn_h)

def render_mode_select_menu(screen):
    bg_sky = get_bg_sky()
    if bg_sky:
        screen.blit(bg_sky, (0, 0))
    else:
        screen.fill((30, 144, 255))

    title_img = get_title_img((420, 160))
    if title_img:
        screen.blit(title_img, (WIDTH // 2 - title_img.get_width() // 2, 60))

    btn_w, btn_h = 340, 48
    btn_x = (WIDTH - btn_w) // 2

    draw_button(screen, "Жеребкування", btn_x, 280, btn_w, btn_h)
    draw_button(screen, "Першим", btn_x, 342, btn_w, btn_h)
    draw_button(screen, "Назад", btn_x, 404, btn_w, btn_h)

def render_pause_menu(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    pause_size = 460
    px = (WIDTH - pause_size) // 2
    py = (HEIGHT - pause_size) // 2 - 10
    
    pause_bg = get_pause_bg((pause_size, pause_size))
    if pause_bg:
        screen.blit(pause_bg, (px, py))

    btn_w, btn_h = 300, 40
    btn_x = WIDTH // 2 - btn_w // 2
    start_y = HEIGHT // 2 - 95
    
    draw_button(screen, "Продовжити", btn_x, start_y, btn_w, btn_h)
    draw_button(screen, "Спочатку", btn_x, start_y + 48, btn_w, btn_h)
    draw_button(screen, "Новий граф", btn_x, start_y + 96, btn_w, btn_h)
    draw_button(screen, "Меню", btn_x, start_y + 144, btn_w, btn_h)

def handle_menu_click(pos, manager):
    mx, my = pos
    if manager.state == "MENU":
        # Змінили координати під нову ширину кнопок (340) та розташування від центру
        btn_w = 340
        btn_x = (WIDTH - btn_w) // 2
        if btn_x <= mx <= btn_x + btn_w:
            if 300 <= my <= 348:
                manager.start_scale_selection("small")
                return True
            elif 362 <= my <= 410:
                manager.start_scale_selection("medium")
                return True
            elif 424 <= my <= 472:
                manager.start_scale_selection("large")
                return True
    elif manager.state == "MODE_SELECT":
        btn_w = 340
        btn_x = (WIDTH - btn_w) // 2
        if btn_x <= mx <= btn_x + btn_w:
            if 280 <= my <= 328:
                return "random"
            elif 342 <= my <= 390:
                return "player"
            elif 404 <= my <= 452:
                manager.state = "MENU"
                return True
    return None