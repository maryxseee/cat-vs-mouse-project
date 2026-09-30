import time

class GameManager:
    def __init__(self):
        self.state = "MENU"  # MENU, MODE_SELECT, WHEEL, PLAYING, PAUSE, WIN, LOSS
        self.scale = "small"
        self.turn = "PLAYER"  # "PLAYER" або "AGENT"
        self.turn_message = "Ваш хід: оберіть рух або знищення містка"
        self.turn_time_limit = 20  # секунд на хід
        self.turn_start_time = 0
        self.animating_edge = None
        
        self.paused_time_left = 0

        # Рулетка жеребкування (швидка, біля 3 секунд)
        self.wheel_step = 0
        self.wheel_max_steps = 15

        # Зберігаємо дані поточного рівня для кнопки "Почати спочатку"
        self.initial_nodes = []
        self.initial_edges = []
        self.initial_cat = 0
        self.initial_mouse = 0

    def start_scale_selection(self, scale):
        self.scale = scale
        self.state = "MODE_SELECT"

    def save_current_level(self, nodes, edges, cat, mouse):
        self.initial_nodes = list(nodes)
        self.initial_edges = list(edges)
        self.initial_cat = cat
        self.initial_mouse = mouse

    def start_game_with_mode(self, mode, nodes, edges, cat, mouse):
        self.save_current_level(nodes, edges, cat, mouse)
        if mode == "random":
            self.state = "WHEEL"
            self.wheel_step = 0
        else:
            self.state = "PLAYING"
            self.turn = "PLAYER"
            self.turn_message = "Ваш хід: оберіть рух або знищення містка"
            self.reset_timer()

    def resolve_wheel(self):
        self.state = "PLAYING"
        self.turn_message = "Ваш хід: оберіть рух або знищення містка" if self.turn == "PLAYER" else "Хід агента (миші)..."
        self.reset_timer()

    def pause_timer(self):
        elapsed = time.time() - self.turn_start_time
        self.paused_time_left = max(0, self.turn_time_limit - elapsed)

    def resume_timer(self):
        self.turn_start_time = time.time() - (self.turn_time_limit - self.paused_time_left)

    def reset_timer(self):
        self.turn_start_time = time.time()

    def get_time_left(self):
        elapsed = time.time() - self.turn_start_time
        return max(0, int(self.turn_time_limit - elapsed))