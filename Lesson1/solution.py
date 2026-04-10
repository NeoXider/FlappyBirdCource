import spritePro as s

# ЧАСТЬ 2: Сцена
# Мы перенесли наш "плоский" код из 1-ой части внутрь класса GameScene,
# чтобы иметь возможность использовать игровой цикл (метод update) и оживить игру.
class GameScene(s.Scene):
    def __init__(self):
        super().__init__()
        
        # Исправляем создание объектов: переносим их сюда и добавляем параметр scene=self
        self.bg = s.Sprite("background.png", size=(400, 600), pos=(0, 0), anchor="topleft", scene=self)
        self.player = s.Sprite("bird.png", size=(50, 50), pos=(100, 300), scene=self)
        
        # ЧАСТЬ 2: Физика
        # Делаем птичку "живой" (Dynamic). Задаем отскок = 0, чтобы при касании пола она не прыгала.
        self.player_body = s.add_physics(self.player, s.PhysicsConfig(bounce=0.0))
        
        # Добавляем физические границы экрана, чтобы птичка не выпадала за его пределы
        s.physics.set_bounds(s.pygame.Rect(0, 0, 400, 600))

    def update(self, dt):
        # ЧАСТЬ 2: Система ввода (Input)
        # s.input позволяет отслеживать мышь и клавиатуру.
        # Используем логический оператор `or` (ИЛИ), чтобы дать игроку выбор:
        # прыгать на Пробел либо на Левую Кнопку Мыши.
        if s.input.was_pressed(s.pygame.K_SPACE) or s.input.was_mouse_pressed(1):
            # Задаем скорость вверх (Y в минус) для прыжка
            self.player_body.velocity.y = -400

# Запускаем движок! Используем нашу Сцену вместо пустого запуска.
if __name__ == '__main__':
    s.run(scene=GameScene, size=(400, 600), title="Flappy Bird: Урок 1", fps=60)
