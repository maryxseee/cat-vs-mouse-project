import math
import pygame
from graph_gen import generate_graph
from ai_agent import get_connected_edges
from menu_screen import handle_menu_click

def check_edge_click(mouse_pos, nodes, edges):
    mx, my = mouse_pos
    for edge in edges:
        u, v, color = edge
        p1, p2 = nodes[u], nodes[v]
        x1, y1 = p1
        x2, y2 = p2
        line_len = math.hypot(x2 - x1, y2 - y1)
        if line_len == 0:
            continue
        t = max(0, min(1, ((mx - x1) * (x2 - x1) + (my - y1) * (y2 - y1)) / (line_len ** 2)))
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        if math.hypot(mx - proj_x, my - proj_y) < 15:
            return edge
    return None

def check_node_click(mouse_pos, nodes):
    mx, my = mouse_pos
    for i, (nx, ny) in enumerate(nodes):
        if math.hypot(mx - nx, my - ny) < 25:
            return i
    return None

def smooth_slide_animation(screen, manager, nodes, edges, old_pos_idx, new_pos_idx, cat_node, mouse_node, render_func, is_cat=False):
    start_pos = nodes[old_pos_idx]
    end_pos = nodes[new_pos_idx]
    frames = 15
    for i in range(frames + 1):
        t = i / frames
        curr_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        curr_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        
        if is_cat:
            render_func(screen, manager, nodes, edges, custom_cat_pos_xy=(curr_x, curr_y), cat_node_idx=old_pos_idx, mouse_node_idx=mouse_node)
        else:
            render_func(screen, manager, nodes, edges, cat_node_idx=cat_node, custom_mouse_pos_xy=(curr_x, curr_y), mouse_node_idx=old_pos_idx)
        pygame.display.flip()
        pygame.time.delay(15)

def handle_click_event(event, manager, current_nodes, current_edges, cat_node, mouse_node, screen, render_func):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = event.pos

        # 1. Головне меню та вибір режиму
        if manager.state in ["MENU", "MODE_SELECT"]:
            res = handle_menu_click((mx, my), manager)
            if res is True:
                return generate_graph(manager.scale)
            elif res in ["random", "player"]:
                manager.start_game_with_mode(res, current_nodes, current_edges, cat_node, mouse_node)
                return current_nodes, current_edges, cat_node, mouse_node

        # 2. Кнопка "Меню" під час гри (відкриває паузу)
        if manager.state == "PLAYING" and WIDTH_BTN_CHECK_MENU(mx, my):
            manager.pause_timer()
            manager.state = "PAUSE"
            return current_nodes, current_edges, cat_node, mouse_node

        # 3. Меню паузи
        elif manager.state == "PAUSE":
            from config import WIDTH, HEIGHT
            cx, cy = WIDTH // 2, HEIGHT // 2
            
            # Продовжити
            if cx - 140 <= mx <= cx + 140 and cy - 100 <= my <= cy - 60:
                manager.resume_timer()
                manager.state = "PLAYING"
                
            # Почати спочатку
            elif cx - 140 <= mx <= cx + 140 and cy - 45 <= my <= cy - 5:
                manager.resume_timer()
                manager.state = "PLAYING"
                manager.turn = "PLAYER"
                manager.turn_message = "Ваш хід: оберіть рух або знищення містка"
                manager.reset_timer()
                return list(manager.initial_nodes), list(manager.initial_edges), manager.initial_cat, manager.initial_mouse
                
            # Новий граф
            elif cx - 140 <= mx <= cx + 140 and cy + 10 <= my <= cy + 50:
                manager.resume_timer()
                manager.state = "PLAYING"
                manager.turn = "PLAYER"
                manager.reset_timer()
                nodes, edges, cat, mouse = generate_graph(manager.scale)
                manager.save_current_level(nodes, edges, cat, mouse)
                return nodes, edges, cat, mouse
                
            # У головне меню
            elif cx - 140 <= mx <= cx + 140 and cy + 65 <= my <= cy + 105:
                manager.state = "MENU"
                
            return current_nodes, current_edges, cat_node, mouse_node

        # 4. Повернення з WIN / LOSS
        if manager.state in ["WIN", "LOSS"]:
            manager.state = "MENU"
            return current_nodes, current_edges, cat_node, mouse_node

        # 5. Хід гравця (Кота)
        elif manager.state == "PLAYING" and manager.turn == "PLAYER":
            clicked_node = check_node_click((mx, my), current_nodes)
            if clicked_node is not None and clicked_node != cat_node:
                is_connected = any((u == cat_node and v == clicked_node) or (u == clicked_node and v == cat_node) for u, v, _ in current_edges)
                if is_connected:
                    old_cat = cat_node
                    cat_node = clicked_node
                    smooth_slide_animation(screen, manager, current_nodes, current_edges, old_cat, cat_node, cat_node, mouse_node, render_func, is_cat=True)
                    
                    if cat_node == mouse_node:
                        manager.state = "WIN"
                    else:
                        manager.turn = "AGENT"
                        manager.turn_message = "Хід агента (миші)..."
                        manager.reset_timer()
                    return current_nodes, current_edges, cat_node, mouse_node

            clicked_edge = check_edge_click((mx, my), current_nodes, current_edges)
            if clicked_edge:
                cat_edges = get_connected_edges(cat_node, current_edges)
                if clicked_edge in cat_edges:
                    current_edges.remove(clicked_edge)
                    manager.turn = "AGENT"
                    manager.turn_message = "Хід агента (миші)..."
                    manager.reset_timer()

    return current_nodes, current_edges, cat_node, mouse_node

def WIDTH_BTN_CHECK_MENU(mx, my):
    from config import WIDTH, HEIGHT
    return (WIDTH - 110) <= mx <= (WIDTH - 20) and (HEIGHT - 50) <= my <= (HEIGHT - 15)