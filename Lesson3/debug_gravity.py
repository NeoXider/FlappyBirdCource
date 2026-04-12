import spritePro as s

class DebugScene(s.Scene):
    def __init__(self):
        super().__init__()
        self.bg = s.Sprite("background.png", pos=s.WH_C, size=s.WH, scene=self, sorting_order=0)
        self.player = s.Sprite("bird.png", pos=(100, s.WH_C[1]), size=(50, 50), scene=self, sorting_order=10)
        self.player_body = s.add_physics(self.player, s.PhysicsConfig(bounce=0.0))
        s.physics.set_gravity(980)
        
        # Добавляем ParticleEmitter как в Lesson3
        self.jump_emitter = s.ParticleEmitter(s.ParticleConfig(
            amount=8,
            size_range=(3, 6),
            speed_range=(60, 140),
            angle_range=(160, 200),
            lifetime_range=(0.2, 0.5),
            fade_speed=400,
            colors=[(255, 255, 100), (255, 200, 50)],
        ))

        # Добавляем TextSprite как в Lesson3
        self.score = 0
        self.score_text = s.TextSprite(
            f"Счёт: {self.score}", pos=(s.WH_C[0], 50),
            font_size=40, color=(0, 0, 0), scene=self, sorting_order=20
        )

        # Добавляем трубы + таймер
        self.pipes = []
        self.spawn_timer = s.Timer(2.0, self.spawn_pipes, repeat=True, scene=self)
        
        self.frame = 0
        self.is_game_over = False

    def spawn_pipes(self):
        import random
        gap_y = random.randint(200, 400)
        gap_size = 150
        pipe_x = 450
        top = s.Sprite("pipe.png", pos=(pipe_x, gap_y - gap_size/2 - 300), size=(80, 600), scene=self, sorting_order=5)
        top.angle = 180
        bottom = s.Sprite("pipe.png", pos=(pipe_x, gap_y + gap_size/2 + 300), size=(80, 600), scene=self, sorting_order=5)
        self.pipes.extend([top, bottom])

    def update(self, dt):
        self.frame += 1
        
        # Тот же angle что в Lesson3
        self.player.angle = max(-30, min(30, -self.player_body.velocity.y / 12))
        
        if self.frame <= 10 or self.frame % 30 == 0:
            print(f"[F{self.frame}] y={self.player.y:.1f} vel_y={self.player_body.velocity.y:.1f} angle={self.player.angle:.1f}", flush=True)

if __name__ == '__main__':
    s.run(scene=DebugScene, size=(400, 600), title="DEBUG: Full Test")
