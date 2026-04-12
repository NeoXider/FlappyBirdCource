import spritePro as s
import random

class GameScene(s.Scene):
    def __init__(self):
        super().__init__()
        
        # 1. Задний фон
        self.bg = s.Sprite("background.png", pos=s.WH_C, size=s.WH, scene=self, sorting_order=0)
        
        # 2. Игрок — птичка с физикой (без отскока)
        self.player = s.Sprite("bird.png", pos=(100, s.WH_C[1]), size=(50, 50), scene=self, sorting_order=10)
        self.player_body = s.add_physics(self.player, s.PhysicsConfig(bounce=0.0))
        s.physics.set_gravity(980)
        
        # 3. Список труб + таймер спавна каждые 2 секунды
        self.pipes = []
        self.spawn_timer = s.Timer(2.0, self.spawn_pipes, repeat=True, scene=self)
        self.spawn_pipes()  # Первая пара сразу
        
        # 4. Флаг окончания игры
        self.is_game_over = False

    def spawn_pipes(self):
        """Создаёт пару труб с дыркой в случайном месте."""
        gap_y = random.randint(200, 400)  # Центр дырки
        gap_size = 150
        pipe_x = 450  # За правым краем экрана
        
        # Верхняя труба (перевёрнутая на 180°)
        top = s.Sprite("pipe.png", pos=(pipe_x, gap_y - gap_size/2 - 300), size=(80, 600), scene=self, sorting_order=5)
        top.angle = 180
        # Нижняя труба
        bottom = s.Sprite("pipe.png", pos=(pipe_x, gap_y + gap_size/2 + 300), size=(80, 600), scene=self, sorting_order=5)
        
        self.pipes.extend([top, bottom])  # Добавляем обе трубы в общий список

    def trigger_game_over(self):
        """Останавливает игру и показывает надпись."""
        if self.is_game_over:
            return
        self.is_game_over = True
        self.player_body.velocity.y = 0
        s.TextSprite("ИГРА ОКОНЧЕНА", pos=s.WH_C, font_size=40, color=(255, 0, 0), scene=self, sorting_order=30)
        s.TextSprite("Нажмите ПРОБЕЛ для рестарта", pos=(s.WH_C[0], s.WH_C[1] + 50), font_size=20, color=(0, 0, 0), scene=self, sorting_order=30)

    def update(self, dt):
        # --- GAME OVER: ждём рестарт ---
        if self.is_game_over:
            if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
                s.restart_scene()
            return

        # --- Управление: прыжок на пробел или клик ---
        if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
            self.player_body.velocity.y = -350

        # --- Двигаем все трубы влево и проверяем столкновения ---
        for pipe in self.pipes:
            pipe.x -= 200 * s.dt
            if self.player.collides_with(pipe):
                self.trigger_game_over()

        # Удаляем трубы, улетевшие за экран
        for pipe in self.pipes[:]:
            if pipe.x < -100:
                pipe.kill()
                self.pipes.remove(pipe)

        # Смерть от выхода за границы экрана
        if self.player.y > s.WH[1] or self.player.y < 0:
            self.trigger_game_over()

if __name__ == '__main__':
    s.run(scene=GameScene, size=(400, 600), title="Flappy Bird")
