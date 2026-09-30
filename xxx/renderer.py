import pygame
import os
from config import WIDTH, HEIGHT, FONT, FONT_SMALL

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

def load_image(filename, size):
    path = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(path):
        img = pygame.image.load(path)
        if pygame.display.get_surface() is not None:
            if filename.lower().endswith('.jpg'):
                img = img.convert()
            else:
                img = img.convert_alpha()
        return pygame.transform.scale(img, size)
    return None

def get_cat_img(size=(140, 140)): return load_image("кот.PNG", size)
def get_mouse_img(size=(90, 90)): return load_image("миша.PNG", size)
def get_cat_large(size=(250, 250)): return load_image("кот.PNG", size)
def get_mouse_large(size=(180, 180)): return load_image("миша.PNG", size)

def get_bg_sky(): return load_image("фон.jpg", (WIDTH, HEIGHT))
def get_title_img(size=(320, 120)): return load_image("напис.PNG", size)
def get_victory_img(size=(WIDTH, HEIGHT)): return load_image("перемога.PNG", size)
def get_defeat_img(size=(WIDTH, HEIGHT)): return load_image("програш.PNG", size)
def get_node_img(size=(46, 46)): return load_image("вершина.PNG", size)

def draw_text_with_shadow(surface, text, font, color, pos, shadow_color=(5, 8, 15), offset=2):
    x, y = pos
    shadow_txt = font.render(text, True, shadow_color)
    surface.blit(shadow_txt, (x + offset, y + offset))
    main_txt = font.render(text, True, color)
    surface.blit(main_txt, (x, y))

def render_all(screen, manager, nodes, edges, custom_cat_pos_xy=None, cat_node_idx=0, custom_mouse_pos_xy=None, mouse_node_idx=0):
    screen.fill((10, 10, 15))

    from ai_agent import get_connected_edges
    cat_edges = get_connected_edges(cat_node_idx, edges) if manager.turn == "PLAYER" and manager.state == "PLAYING" else []

    # Малювання ребер із неоновим ефектом світіння
    for edge in edges:
        u, v, color = edge
        p1 = nodes[u]
        p2 = nodes[v]
        
        line_color = color
        if manager.animating_edge == edge:
            line_color = (239, 68, 68)

        glow_color = (max(0, line_color[0]//3), max(0, line_color[1]//3), max(0, line_color[2]//3))
        pygame.draw.line(screen, glow_color, p1, p2, 7)

        if edge in cat_edges:
            pygame.draw.line(screen, (59, 130, 246), p1, p2, 9)

        pygame.draw.line(screen, line_color, p1, p2, 3)

    # Виводимо твої нові піксельні вершини замість кіл
    node_img = get_node_img((46, 46))
    for i, (x, y) in enumerate(nodes):
        if node_img:
            screen.blit(node_img, (x - 23, y - 23))
        else:
            # Запасний варіант, якщо картинка раптом не завантажиться
            pygame.draw.circle(screen, (15, 23, 42), (x, y), 20)

    # Позиція Кота
    if custom_cat_pos_xy:
        cx, cy = custom_cat_pos_xy
    else:
        cx, cy = nodes[cat_node_idx]
        
    cat_img = get_cat_img((140, 140))
    if cat_img:
        screen.blit(cat_img, (cx - 70, cy - 70))

    # Позиція Миші
    if custom_mouse_pos_xy:
        mx, my = custom_mouse_pos_xy
    else:
        mx, my = nodes[mouse_node_idx]

    mouse_img = get_mouse_img((90, 90))
    if mouse_img:
        screen.blit(mouse_img, (mx - 45, my - 45))

    # Верхня панель (HUD)
    hud_surf = pygame.Surface((WIDTH, 65), pygame.SRCALPHA)
    hud_surf.fill((15, 23, 42, 220))
    screen.blit(hud_surf, (0, 0))
    
    pygame.draw.line(screen, (59, 130, 246), (0, 65), (WIDTH, 65), 2)
    
    status_text_str = manager.turn_message
    draw_text_with_shadow(screen, status_text_str, FONT_SMALL, (241, 245, 249), (20, 22), offset=2)

    title_mini = get_title_img((160, 45))
    if title_mini:
        screen.blit(title_mini, (WIDTH // 2 - title_mini.get_width() // 2, 10))

    if manager.state == "PLAYING":
        time_left = manager.get_time_left()
        timer_color = (239, 68, 68) if time_left <= 5 else (34, 197, 94) if time_left > 10 else (234, 179, 8)
        
        timer_bg_rect = pygame.Rect(WIDTH - 130, 15, 110, 35)
        pygame.draw.rect(screen, (30, 41, 59), timer_bg_rect, border_radius=8)
        pygame.draw.rect(screen, timer_color, timer_bg_rect, width=1, border_radius=8)
        
        timer_str = f"Час: {int(time_left)}с"
        draw_text_with_shadow(screen, timer_str, FONT_SMALL, timer_color, (WIDTH - 120, 23), offset=1)

    from ui_components import draw_button
    draw_button(screen, "Меню", WIDTH - 110, HEIGHT - 50, 90, 35)

def play_win_explosion_animation(screen, nodes, cat_node, mouse_node, edges, render_func, manager):
    mx, my = nodes[mouse_node]
    cat_base_img = load_image("кот.PNG", (140, 140))
    
    for size in range(140, 600, 40):
        render_func(screen, manager, nodes, edges, cat_node_idx=cat_node, mouse_node_idx=mouse_node)
        if cat_base_img:
            scaled_cat = pygame.transform.scale(cat_base_img, (size, size))
            screen.blit(scaled_cat, (mx - size // 2, my - size // 2))
        pygame.display.flip()
        pygame.time.delay(25)

    flash_surf = pygame.Surface((WIDTH, HEIGHT))
    flash_surf.fill((128, 0, 128))
    screen.blit(flash_surf, (0, 0))
    pygame.display.flip()
    pygame.time.delay(400)