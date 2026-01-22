clear()

# --- СИСТЕМНЫЕ ФУНКЦИИ ---


def core_move(tx, ty):
    while get_pos_x() < tx:
        move(East)
    while get_pos_x() > tx:
        move(West)
    while get_pos_y() < ty:
        move(North)
    while get_pos_y() > ty:
        move(South)


def core_safe_plant(entity):
    # Деревья и Трава — на луг, Морковь и Кусты — на грядку
    if entity == Entities.Tree or entity == Entities.Grass:
        if get_ground_type() != Grounds.Grassland:
            till()
    else:
        if get_ground_type() != Grounds.Soil:
            till()

    # Если на клетке уже что-то есть — собираем, если это не то, что нам нужно
    if get_entity_type() != entity:
        if can_harvest():
            harvest()
        plant(entity)


# --- ЛОГИКА ПОЛИКУЛЬТУРЫ ---


def manage_companions():
    # Проверяем, есть ли под нами растение, которому нужен компаньон
    comp_data = get_companion()
    if comp_data != None:
        c_type, c_pos = comp_data  # Распаковка: тип и кортеж координат
        c_x, c_y = c_pos  # Распаковка координат

        # Запоминаем, где стояли
        old_x, old_y = get_pos_x(), get_pos_y()

        # Летим и высаживаем компаньона
        core_move(c_x, c_y)
        core_safe_plant(c_type)

        # Возвращаемся к основному дереву
        core_move(old_x, old_y)


# --- ОСНОВНОЙ ЦИКЛ ---

size = get_world_size()

# Инициализация поля (первичная застройка)
for x in range(size):
    for y in range(size):
        core_move(x, y)
        if (x + y) % 2 == 0:
            core_safe_plant(Entities.Tree)
        else:
            core_safe_plant(Entities.Grass)

while True:
    for x in range(size):
        for y in range(size):
            # Работаем только по шахматной сетке для деревьев
            if (x + y) % 2 == 0:
                core_move(x, y)

                # 1. Проверка: если дерево созрело — собираем и сажаем заново
                if can_harvest():
                    harvest()
                    core_safe_plant(Entities.Tree)
                    # После пересадки сразу ищем нового компаньона
                    manage_companions()

                # 2. Проверка: если клетка вдруг пустая — засаживаем
                elif get_entity_type() == None:
                    core_safe_plant(Entities.Tree)
                    manage_companions()

                # 3. Опционально: полив, если дерево еще растет
                else:
                    if get_water() < 0.6:
                        if num_items(Items.Water) > 0:
                            use_item(Items.Water)
