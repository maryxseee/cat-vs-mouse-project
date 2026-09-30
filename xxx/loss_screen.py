import pygame
from config import WIDTH, HEIGHT
from ui_components import draw_button
from renderer import get_defeat_img

def render_loss_screen(screen):
    # Заливаємо весь екран чорним фоном
    screen.fill((0, 0, 0))
    
    # 1. Верхня половина екрана для картинки поразки
    defeat_img = get_defeat_img((WIDTH, int(HEIGHT * 0.45)))
    if defeat_img:
        img_x = (WIDTH - defeat_img.get_width()) // 2
        screen.blit(defeat_img, (img_x, 30))
        
    # 2. Нижня половина екрана для кнопок
    btn_w = 280
    btn_x = (WIDTH - btn_w) // 2
    draw_button(screen, "Ще раз", btn_x, 320, btn_w, 45)
    draw_button(screen, "Новий граф", btn_x, 380, btn_w, 45)
    draw_button(screen, "Головне меню", btn_x, 440, btn_w, 45)

def handle_loss_click(event, manager):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos
        btn_w = 280
        btn_x = (WIDTH - btn_w) // 2
        if btn_x <= mx <= btn_x + btn_w:
            if 320 <= my <= 365:
                manager.start_game()
                return "restart"
            elif 380 <= my <= 425:
                manager.start_scale_selection(manager.current_scale_type)
                return "new_graph"
            elif 440 <= my <= 485:
                manager.state = "MENU"
                return "menu"
    return None
