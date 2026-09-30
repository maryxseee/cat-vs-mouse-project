import pygame
import os
from pixel_font import pixel_font

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_button_image(size):
    path = os.path.join(ASSETS_DIR, "кнопка.PNG")
    if os.path.exists(path):
        img = pygame.image.load(path)
        if pygame.display.get_surface() is not None:
            img = img.convert_alpha()
        return pygame.transform.scale(img, size)
    return None

def draw_button(screen, text, x, y, w, h):
    mouse_pos = pygame.mouse.get_pos()
    is_hover = x <= mouse_pos[0] <= x + w and y <= mouse_pos[1] <= y + h
    
    current_w = w + 6 if is_hover else w
    current_h = h + 4 if is_hover else h
    current_x = x - 3 if is_hover else x
    current_y = y - 2 if is_hover else y
    
    btn_img = load_button_image((current_w, current_h))
    
    if btn_img:
        screen.blit(btn_img, (current_x, current_y))
    else:
        color = (30, 58, 138) if is_hover else (15, 23, 42)
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
    
    # Рендеримо текст твоїм піксельним шрифтом
    txt_surf = pixel_font.render(text, scale=0.015)
    
    text_x = current_x + (current_w - txt_surf.get_width()) // 2
    text_y = current_y + (current_h - txt_surf.get_height()) // 2
    
    screen.blit(txt_surf, (text_x, text_y))