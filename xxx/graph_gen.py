import random
import math

PALETTE = [
    (236, 72, 153),   # Рожевий
    (34, 197, 94),    # Зелений
    (234, 179, 8),    # Жовтий
    (168, 85, 247),   # Фіолетовий
    (249, 115, 22),   # Оранжевий
    (20, 184, 166),   # Бірюзовий
    (244, 63, 94),    # Малиновий
]

def do_intersect(p1, p2, p3, p4):
    def ccw(A, B, C):
        return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def get_shortest_path_len(start, goal, edges):
    if start == goal:
        return 0
    adj = {}
    for u, v, _ in edges:
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    visited = {start}
    queue = [(start, 0)]
    while queue:
        node, dist = queue.pop(0)
        if node == goal:
            return dist
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return float('inf')

def generate_graph(scale_type):
    if scale_type == "small":
        num_nodes = 6
        max_degree = 3  # Маленький: не більше 3 ребер на вершину
    elif scale_type == "medium":
        num_nodes = 9
        max_degree = 3  # Середній: не більше 3 ребер на вершину
    else:
        num_nodes = 12
        max_degree = 4  # Великий: не більше 4 ребер на вершину

    cat_node = 0
    mouse_node = num_nodes // 2  # Розносимо мишу в протилежну частину графа на старті

    for _ in range(3000):
        nodes = []
        while len(nodes) < num_nodes:
            x = random.randint(120, 680)
            y = random.randint(100, 500)
            if all(math.hypot(x - nx, y - ny) > 110 for nx, ny in nodes):
                nodes.append((x, y))

        raw_edges = set()
        
        # Функція для підрахунку кількості ребер у кожного вузла
        def get_degrees(edges_set):
            deg = {i: 0 for i in range(num_nodes)}
            for u, v in edges_set:
                deg[u] += 1
                deg[v] += 1
            return deg

        # Генеруємо базовий каркас (кільце) без прямих з'єднань між стартом кота і миші
        for i in range(num_nodes):
            target = (i + 1) % num_nodes
            if not ((i == cat_node and target == mouse_node) or (i == mouse_node and target == cat_node)):
                raw_edges.add((min(i, target), max(i, target)))

        extra_edges = num_nodes
        attempts = 0
        while len(raw_edges) < num_nodes + extra_edges and attempts < 150:
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            attempts += 1
            if u != v:
                if (u == cat_node and v == mouse_node) or (u == mouse_node and v == cat_node):
                    continue
                p1, p2 = min(u, v), max(u, v)
                if not any(e[0] == p1 and e[1] == p2 for e in raw_edges):
                    # Перевіряємо ліміт ребер для обох вершин перед додаванням
                    current_deg = get_degrees(raw_edges)
                    if current_deg[p1] < max_degree and current_deg[p2] < max_degree:
                        raw_edges.add((p1, p2))

        colored_edges = []
        for u, v in raw_edges:
            p1, p2 = nodes[u], nodes[v]
            forbidden_colors = set()
            for existing_u, existing_v, existing_col in colored_edges:
                ep1, ep2 = nodes[existing_u], nodes[existing_v]
                if do_intersect(p1, p2, ep1, ep2):
                    forbidden_colors.add(existing_col)
                    
            chosen_color = PALETTE[0]
            for color in PALETTE:
                if color not in forbidden_colors:
                    chosen_color = color
                    break
            else:
                chosen_color = random.choice(PALETTE)
                
            colored_edges.append((u, v, chosen_color))

        # Перевірка найкоротшого шляху: він зобов'язаний бути строго більшим за 1 ребро
        path_len = get_shortest_path_len(cat_node, mouse_node, colored_edges)
        
        if path_len > 1 and path_len != float('inf'):
            return nodes, colored_edges, cat_node, mouse_node

    return nodes, colored_edges, cat_node, mouse_node