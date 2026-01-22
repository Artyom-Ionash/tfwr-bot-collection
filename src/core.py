def move_to(t_x, t_y):
    # type: (int, int) -> None
    if get_pos_x() == t_x and get_pos_y() == t_y:
        return

    while get_pos_x() < t_x:
        move(East)
    while get_pos_x() > t_x:
        move(West)
    while get_pos_y() < t_y:
        move(North)
    while get_pos_y() > t_y:
        move(South)


def generate_closed_path(w, h):
    # type: (int, int) -> list[tuple[int, int]]

    path = []  # type: list[tuple[int, int]]

    # 1. Верхняя строка (слева направо)
    # Путь: (0,0) -> (1,0) -> ... -> (5,0)
    for x in range(w):
        path.append((x, 0))

    # 2. Остальное поле (змейкой справа налево)
    # Мы начинаем с последнего столбца (w-1) и идем к 0
    for i in range(w):
        # x идет: 5, 4, 3, 2, 1, 0
        current_x = (w - 1) - i

        # Для четных шагов (относительно цикла) идем ВНИЗ
        # Для нечетных идем ВВЕРХ
        # Начинаем с y=1, так как y=0 уже пройден
        if i % 2 == 0:
            # Идем вниз: 1 -> 4
            for y in range(1, h):
                path.append((current_x, y))
        else:
            # Идем вверх: 4 -> 1
            for y in range(h - 1, 0, -1):
                path.append((current_x, y))

    return path


def await_harvest():
    # Режим "Турбо-кемпинг"
    # Ждем созревания, удерживая воду на максимуме
    while not can_harvest():
        quick_print("Ожидание...")  # Можно раскомментировать для отладки
    harvest()


SOIL_PLANTS = {Entities.Carrot, Entities.Pumpkin, Entities.Sunflower, Entities.Cactus}


def safe_plant(entity):
    # type: (EntityType) -> None
    if get_entity_type() == entity:
        return

    # Если на клетке сорняк или остатки — убираем без бонусов
    if can_harvest():
        harvest()

    # Выбор типа почвы
    if entity == Entities.Grass:
        if get_ground_type() != Grounds.Grassland:
            till()
    elif entity in SOIL_PLANTS:
        if get_ground_type() != Grounds.Soil:
            till()

    plant(entity)


def measure_sunflower(d=None):
    # type: (Direction | None) -> int
    m = measure(d)
    if m * 0 == 0:
        return m

    print("Не удалось оценить подсолнух. Проверьте шапку.")
    while True:
        pass


def measure_cactus(d=None):
    # type: (Direction | None) -> int
    m = measure(d)
    if m * 0 == 0:
        return m

    print("Не удалось оценить кактус. Проверьте шапку.")
    while True:
        pass


def measure_dinosaur():
    # type: () -> Vector2
    m = measure()
    if m * 0 == ():
        return m

    print("Яблоко не обнаружено. Проверьте шапку.")
    while True:
        pass
