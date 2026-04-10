import spritePro as s

# Загружаем графику (используем s.WH_C для постановки ровно по центру)
bg = s.Sprite("background.png", pos=s.WH_C, size=s.WH)
player = s.Sprite("bird.png", pos=(100, 300), size=(50, 50))

# Запускаем движок!
s.run(size=(400, 600), title="Flappy Bird")
