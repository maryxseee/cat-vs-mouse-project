import pygame
import sys
from config import WIDTH, HEIGHT, FONT
from game_state import GameManager
from renderer import (
    render_all, 
    get_bg_sky, 
    get_cat_large, 
    get_mouse_large, 
    play_win_explosion_animation
)
from event_handler import handle_click_event, smooth_slide_animation
from loss_screen import render_loss_screen
from win_screen import render_win_screen
from graph_gen import generate_graph, get_shortest_path_len
from ai_agent import get_agent_move, get_connected_edges
from menu_screen import render_main_menu, render_mode_select_menu, render_pause_menu
from pixel_font import pixel_font

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Кіт і Миша: Графічна головоломка")
    clock = pygame.time.Clock()

    manager = GameManager()
    current_nodes, current_edges, cat_node, mouse_node = generate_graph("small")

    wheel_frame_counter = 0

    while True:
        # Логіка рулетки жеребкування (~3 секунди)
        if manager.state == "WHEEL":
            wheel_frame_counter += 1
            if wheel_frame_counter >= 5:
                wheel_frame_counter = 0
                manager.wheel_step += 1
                manager.turn = "PLAYER" if manager.wheel_step % 2 == 0 else "AGENT"

                if manager.wheel_step >= manager.wheel_max_steps:
                    manager.resolve_wheel()

        elif manager.state == "PLAYING" and manager.turn == "AGENT":
            pygame.time.delay(500)
            
            agent_action = get_agent_move(mouse_node, cat_node, current_edges)
            if agent_action:
                act_type, act_data = agent_action
                if act_type == "MOVE":
                    old_mouse = mouse_node
                    mouse_node = act_data
                    smooth_slide_animation(screen, manager, current_nodes, current_edges, old_mouse, mouse_node, cat_node, mouse_node, render_all, is_cat=False)
                elif act_type == "DESTROY" and act_data in current_edges:
                    manager.animating_edge = act_data
                    render_all(screen, manager, current_nodes, current_edges, cat_node_idx=cat_node, mouse_node_idx=mouse_node)
                    pygame.display.flip()
                    pygame.time.delay(300)
                    current_edges.remove(act_data)
                    manager.animating_edge = None

            if cat_node == mouse_node:
                play_win_explosion_animation(screen, current_nodes, cat_node, mouse_node, current_edges, render_all, manager)
                manager.state = "WIN"
            else:
                path_len = get_shortest_path_len(cat_node, mouse_node, current_edges)
                cat_has_edges = len(get_connected_edges(cat_node, current_edges)) > 0
                
                if not cat_has_edges or path_len == float('inf'):
                    manager.state = "LOSS"
                else:
                    manager.turn = "PLAYER"
                    manager.turn_message = "Ваш хід: Оберіть рух або знищення"
                    manager.reset_timer()

        if manager.state == "PLAYING" and manager.turn == "PLAYER":
            if manager.get_time_left() <= 0:
                manager.state = "LOSS"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            res = handle_click_event(
                event, manager, current_nodes, current_edges, cat_node, mouse_node, screen, render_all
            )
            if res and len(res) == 4:
                current_nodes, current_edges, cat_node, mouse_node = res

        # --- РЕНДЕРИНГ ЕКРАНІВ ---

        if manager.state == "MENU":
            render_main_menu(screen)

        elif manager.state == "MODE_SELECT":
            render_mode_select_menu(screen)

        elif manager.state == "WHEEL":
            bg_sky = get_bg_sky()
            if bg_sky:
                screen.blit(bg_sky, (0, 0))
            else:
                screen.fill((30, 144, 255))

            # Заголовок жеребкування твоїм акуратним піксельним шрифтом
            wheel_title_surf = pixel_font.render("Визначення першого ходу...", scale=0.02)
            screen.blit(wheel_title_surf, (WIDTH // 2 - wheel_title_surf.get_width() // 2, 120))

            img_to_show = get_cat_large((200, 200)) if manager.turn == "PLAYER" else get_mouse_large((140, 140))
            if img_to_show:
                screen.blit(img_to_show, (WIDTH // 2 - img_to_show.get_width() // 2, HEIGHT // 2 - img_to_show.get_height() // 2))

            # Нижній текст повністю прибрано

        elif manager.state == "PLAYING":
            render_all(screen, manager, current_nodes, current_edges, cat_node_idx=cat_node, mouse_node_idx=mouse_node)

        elif manager.state == "PAUSE":
            render_all(screen, manager, current_nodes, current_edges, cat_node_idx=cat_node, mouse_node_idx=mouse_node)
            render_pause_menu(screen)

        elif manager.state == "LOSS":
            render_loss_screen(screen)
        elif manager.state == "WIN":
            render_win_screen(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()