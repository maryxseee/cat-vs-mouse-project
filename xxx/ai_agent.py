import random
from graph_gen import get_shortest_path_len

def get_connected_edges(node_idx, edges):
    return [e for e in edges if e[0] == node_idx or e[1] == node_idx]

def get_agent_move(mouse_node, cat_node, edges):
    adj = {}
    for u, v, col in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    mouse_neighbors = adj.get(mouse_node, [])
    mouse_edges = get_connected_edges(mouse_node, edges)

    if not mouse_neighbors and not mouse_edges:
        return None

    # КРОК 1: КРИТИЧНА ЗАГРОЗА (Кіт на відстані рівно 1 ребра впритул)
    direct_edge = None
    for u, v, col in mouse_edges:
        if (u == mouse_node and v == cat_node) or (v == mouse_node and u == cat_node):
            direct_edge = (u, v, col)
            break

    # ТІЛЬКИ ТУТ миша має право знищити міст — коли кіт дивиться на неї напряму!
    if direct_edge:
        return ("DESTROY", direct_edge)

    # КРОК 2: ОСНОВНА ВТЕЧА (Шукаємо сусіда, який максимально віддаляє від кота)
    current_dist = get_shortest_path_len(mouse_node, cat_node, edges)

    best_neighbor = None
    max_dist = current_dist
    for neighbor in mouse_neighbors:
        dist = get_shortest_path_len(neighbor, cat_node, edges)
        if dist > max_dist:
            max_dist = dist
            best_neighbor = neighbor

    # Якщо знайшли куди тікати — миша робить крок у безпечніше місце
    if best_neighbor is not None:
        return ("MOVE", best_neighbor)

    # КРОК 3: ЯКЩО ТІКАТИ НІКУДИ (Замкнений простір), але кіт ЩЕ ДАЛЕКО — 
    # миша просто робить випадковий крок до доступного сусіда, А НЕ РУЙНУЄ РЕБРА!
    if mouse_neighbors:
        return ("MOVE", random.choice(mouse_neighbors))

    # Крайній випадок, якщо зовсім немає виходу
    if mouse_edges:
        return ("DESTROY", random.choice(mouse_edges))

    return None