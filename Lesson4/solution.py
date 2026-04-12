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
        
        # 3. Трубы + таймер
        self.pipes = []
        self.spawn_timer = s.Timer(2.0, self.spawn_pipes, repeat=True, scene=self)
        self.spawn_pipes()
        
        # 4. Счёт текущий
        self.score = 0
        self.score_text = s.TextSprite(
            f"Счёт: {self.score}", pos=(s.WH_C[0], 50),
            font_size=40, color=(0, 0, 0), scene=self, sorting_order=20
        )
        
        # 5. Лучший счёт (загружаем из файла!)
        saved = s.save_load.load("best_score.json", default_value={"best": 0})
        self.best_score = saved["best"]
        
        # 6. Партиклы на прыжок
        self.jump_emitter = s.ParticleEmitter(s.ParticleConfig(
            amount=8,
            size_range=(3, 6),
            speed_range=(60, 140),
            angle_range=(160, 200),
            lifetime_range=(0.2, 0.5),
            fade_speed=400,
            colors=[(255, 255, 100), (255, 200, 50)],
        ))
        
        # 7. Партиклы на смерть (красные)
        self.death_emitter = s.ParticleEmitter(s.ParticleConfig(
            amount=25,
            size_range=(4, 8),
            speed_range=(100, 250),
            angle_range=(0, 360),
            lifetime_range=(0.4, 1.0),
            fade_speed=300,
            colors=[(255, 80, 80), (255, 40, 40), (255, 160, 60)],
        ))
        
        # 8. Музыка и звуки
        s.audio_manager.play_music("Monkeys-Spinning-Monkeys(chosic.com).mp3")
        self.snd_jump = s.load_sound("jump", "whoosh.wav")
        self.snd_punch = s.load_sound("punch", "punch.mp3")
        
        # 9. Состояние
        self.is_game_over = False

    def spawn_pipes(self):
        """Создаёт пару труб с дыркой в случайном месте."""
        gap_y = random.randint(200, 400)
        gap_size = 150
        pipe_x = 450
        
        top = s.Sprite("pipe.png", pos=(pipe_x, gap_y - gap_size/2 - 300), size=(80, 600), scene=self, sorting_order=5)
        top.angle = 180
        bottom = s.Sprite("pipe.png", pos=(pipe_x, gap_y + gap_size/2 + 300), size=(80, 600), scene=self, sorting_order=5)
        bottom.passed = False
        
        self.pipes.extend([top, bottom])

    def trigger_game_over(self):
        """Останавливает игру, сохраняет рекорд и показывает результат."""
        if self.is_game_over:
            return
        self.is_game_over = True
        self.player_body.velocity.y = 0
        
        # Спецэффекты при смерти
        s.shake_camera(strength=(12, 12), duration=0.35)
        self.death_emitter.emit(self.player.position)
        self.snd_punch.play()
        
        # Проверяем и сохраняем рекорд
        is_new_record = self.score > self.best_score
        if is_new_record:
            self.best_score = self.score
            s.save_load.save({"best": self.best_score}, "best_score.json")
        
        # Надписи
        s.TextSprite("ИГРА ОКОНЧЕНА", pos=(s.WH_C[0], s.WH_C[1] - 30), font_size=40, color=(255, 0, 0), scene=self, sorting_order=30)
        
        # Показываем рекорд
        record_color = (255, 215, 0) if is_new_record else (0, 0, 0)
        record_prefix = "🏆 НОВЫЙ РЕКОРД! " if is_new_record else "Лучший: "
        s.TextSprite(f"{record_prefix}{self.best_score}", pos=s.WH_C, font_size=24, color=record_color, scene=self, sorting_order=30)
        
        s.TextSprite("Нажмите ПРОБЕЛ", pos=(s.WH_C[0], s.WH_C[1] + 40), font_size=20, color=(0, 0, 0), scene=self, sorting_order=30)
        
        # Плавное затухание птички
        s.tween_alpha(self.player, to=80, duration=0.5)

    def update(self, dt):
        # --- GAME OVER ---
        if self.is_game_over:
            if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
                s.restart_scene()
            return

        # --- Управление ---
        if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
            self.player_body.velocity.y = -350
            self.jump_emitter.emit(self.player.position)
            self.snd_jump.play()

        # --- Наклон птички ---
        self.player.angle = max(-30, min(30, -self.player_body.velocity.y / 12))

        # --- Трубы ---
        for pipe in self.pipes:
            pipe.x -= 200 * s.dt
            if self.player.collides_with(pipe):
                self.trigger_game_over()

        for pipe in self.pipes[:]:
            if pipe.x < -100:
                pipe.kill()
                self.pipes.remove(pipe)

        # --- Очки ---
        for pipe in self.pipes:
            if hasattr(pipe, 'passed') and not pipe.passed and pipe.x < self.player.x:
                pipe.passed = True
                self.score += 1
                self.score_text.text = f"Счёт: {self.score}"
                # Пульсация текста при новом очке!
                s.tween_punch_scale(self.score_text, strength=0.3, duration=0.2)

        # Смерть от выхода за экран
        if self.player.y > s.WH[1] or self.player.y < 0:
            self.trigger_game_over()

if __name__ == '__main__':
    s.run(scene=GameScene, size=(400, 600), title="Flappy Bird")
