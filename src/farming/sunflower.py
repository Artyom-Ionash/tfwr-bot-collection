from core import move_to, generate_closed_path, await_harvest

# --- ГИПЕРПАРАМЕТРЫ ---
WIDTH = 6  # Должно быть ЧЁТНЫМ числом для идеального цикла!
HEIGHT = 5  # Может быть любым
WATER_THRESHOLD = 0.75

# --- ИНИЦИАЛИЗАЦИЯ ---
clear()
# Генерируем идеальный путь один раз
path = generate_closed_path(WIDTH, HEIGHT)

# --- ФАЗА 1: БЫСТРЫЙ ЗАСЕВ ---
for pos in path:
    x, y = pos
    move_to(x, y)

    if get_entity_type() != Entities.Sunflower:
        if get_entity_type() != None:
            harvest()
        if get_ground_type() != Grounds.Soil:
            till()
        plant(Entities.Sunflower)

    if get_water() < WATER_THRESHOLD:
        use_item(Items.Water)

# --- ФАЗА 2: БЕСКОНЕЧНЫЙ ЦИКЛ ---
while True:
    # Благодаря структуре path, переход от последней точки к первой
    # будет шагом (0, 1) -> (0, 0). Никаких прыжков через поле!
    for pos in path:
        x, y = pos
        move_to(x, y)

        if get_water() < WATER_THRESHOLD:
            use_item(Items.Water)

        # Проверка наличия
        if get_entity_type() != Entities.Sunflower:
            if get_entity_type() != None:
                harvest()
            if get_ground_type() != Grounds.Soil:
                till()
            plant(Entities.Sunflower)

        await_harvest()
        plant(Entities.Sunflower)
