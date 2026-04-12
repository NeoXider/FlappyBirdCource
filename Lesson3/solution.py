import spritePro as s
import random

class GameScene(s.Scene):
    def __init__(self):
        super().__init__()
        
        # 1. Задний фон
        self.bg = s.Sprite("background.png", pos=s.WH_C, size=s.WH, scene=self, sorting_order=0)
        
        # 2. Игрок — птичка с физикой
        self.player = s.Sprite("bird.png", pos=(100, s.WH_C[1]), size=(50, 50), scene=self, sorting_order=10)
        self.player_body = s.add_physics(self.player, s.PhysicsConfig(bounce=0.0))
        s.physics.set_gravity(980)
        
        # 3. Список труб + таймер спавна
        self.pipes = []
        self.spawn_timer = s.Timer(2.0, self.spawn_pipes, repeat=True, scene=self)
        self.spawn_pipes()
        
        # 4. Счёт
        self.score = 0
        self.score_text = s.TextSprite(
            f"Счёт: {self.score}", pos=(s.WH_C[0], 50),
            font_size=40, color=(0, 0, 0), scene=self, sorting_order=20
        )
        
        # 5. Партиклы на прыжок (искры)
        self.jump_emitter = s.ParticleEmitter(s.ParticleConfig(
            amount=8,
            size_range=(3, 6),
            speed_range=(60, 140),
            angle_range=(160, 200),      # Летят назад-вниз
            lifetime_range=(0.2, 0.5),
            fade_speed=400,
            colors=[(255, 255, 100), (255, 200, 50)],
        ))
        
        # 6. Состояние игры
        self.is_game_over = False

    def spawn_pipes(self):
        """Создаёт пару труб с дыркой в случайном месте."""
        gap_y = random.randint(200, 400)
        gap_size = 150
        pipe_x = 450
        
        top = s.Sprite("pipe.png", pos=(pipe_x, gap_y - gap_size/2 - 300), size=(80, 600), scene=self, sorting_order=5)
        top.angle = 180
        bottom = s.Sprite("pipe.png", pos=(pipe_x, gap_y + gap_size/2 + 300), size=(80, 600), scene=self, sorting_order=5)
        bottom.passed = False  # Флаг для подсчёта очков
        
        self.pipes.extend([top, bottom])

    def trigger_game_over(self):
        """Останавливает игру и показывает надпись."""
        if self.is_game_over:
            return
        self.is_game_over = True
        self.player_body.velocity.y = 0
        
        # Тряска камеры при смерти!
        s.shake_camera(strength=(10, 10), duration=0.3)
        
        s.TextSprite("ИГРА ОКОНЧЕНА", pos=s.WH_C, font_size=40, color=(255, 0, 0), scene=self, sorting_order=30)
        s.TextSprite("Нажмите ПРОБЕЛ для рестарта", pos=(s.WH_C[0], s.WH_C[1] + 50), font_size=20, color=(0, 0, 0), scene=self, sorting_order=30)

    def update(self, dt):
        # --- GAME OVER ---
        if self.is_game_over:
            if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
                s.restart_scene()
            return

        # --- Управление: прыжок ---
        if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
            self.player_body.velocity.y = -350
            # Выпускаем искры при прыжке!
            self.jump_emitter.emit(self.player.position)

        # --- Наклон птички по скорости ---
        # Летим вверх → наклон вверх (-30°), падаем → наклон вниз (30°)
        self.player.angle = max(-30, min(30, -self.player_body.velocity.y / 12))

        # --- Двигаем трубы и проверяем столкновения ---
        for pipe in self.pipes:
            pipe.x -= 200 * s.dt
            if self.player.collides_with(pipe):
                self.trigger_game_over()

        # Удаляем трубы за экраном
        for pipe in self.pipes[:]:
            if pipe.x < -100:
                pipe.kill()
                self.pipes.remove(pipe)

        # --- Подсчёт очков ---
        for pipe in self.pipes:
            if hasattr(pipe, 'passed') and not pipe.passed and pipe.x < self.player.x:
                pipe.passed = True
                self.score += 1
                self.score_text.text = f"Счёт: {self.score}"

        # Смерть от выхода за экран
        if self.player.y > s.WH[1] or self.player.y < 0:
            self.trigger_game_over()

if __name__ == '__main__':
    s.run(scene=GameScene, size=(400, 600), title="Flappy Bird")
