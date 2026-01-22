clear()

# ====================================================================
# [CORE] - НАВИГАЦИЯ И ПОДГОТОВКА
# ====================================================================


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
    # Кактусы растут только на грядках:
    if get_ground_type() != Grounds.Soil:
        till()

    if get_entity_type() != entity:
        if can_harvest():
            harvest()
        plant(entity)


# ====================================================================
# [LOGIC] - ПРЕДВАРИТЕЛЬНАЯ ПОДГОТОВКА ПОЛЯ
# ====================================================================


def prepare_field(size):
    for y in range(size):
        for x in range(size):
            # Движение змейкой:
            target_x = x
            if y % 2 != 0:
                target_x = size - 1 - x

            core_move(target_x, y)

            if get_entity_type() != Entities.Cactus:
                core_safe_plant(Entities.Cactus)

                # Активация поликультуры для ускорения роста:
                comp_data = get_companion()
                if comp_data != None:
                    c_type, c_pos = comp_data
                    home_x, home_y = get_pos_x(), get_pos_y()
                    core_move(c_pos[0], c_pos[1])
                    core_safe_plant(c_type)
                    core_move(home_x, home_y)


# ====================================================================
# [SORTING] - 2D BUBBLE SORT С ГРАНИЦАМИ И ЗМЕЙКОЙ
# ====================================================================


def sort_cactus_matrix(size):
    # max_index_to_check — это граница, за которую дрон не пойдет:
    max_index_to_check = size * size

    while True:
        swapped = False
        last_swap_index = 0

        for i in range(max_index_to_check):
            # Координаты змейкой:
            y = i // size
            x = i % size
            if y % 2 != 0:
                x = size - 1 - x

            core_move(x, y)

            # Проверка соседа справа (East):
            if x < size - 1:
                if measure() > measure(East):
                    swap(East)
                    swapped = True
                    last_swap_index = i

            # Проверка соседа сверху (North):
            if y < size - 1:
                if measure() > measure(North):
                    swap(North)
                    swapped = True
                    last_swap_index = i

        # Сокращаем область поиска до последнего места обмена:
        max_index_to_check = last_swap_index + 1

        # Если обменов не было — поле идеально отсортировано (зеленое):
        if not swapped or max_index_to_check <= 1:
            break


# ====================================================================
# [MAIN] - УПРАВЛЯЮЩИЙ ЦИКЛ
# ====================================================================

size = get_world_size()

while True:
    # 1. Засаживаем поле и ускоряем рост:
    prepare_field(size)

    # 2. Ожидание созревания и очистка от компаньонов:
    ready = False
    while not ready:
        ready = True
        for i in range(size * size):
            core_move(i % size, i // size)
            # Если не кактус или еще не вырос:
            if get_entity_type() != Entities.Cactus:
                core_safe_plant(Entities.Cactus)
                ready = False
            elif not can_harvest():
                ready = False

    # 3. Сортировка (превращаем поле в ярко-зеленое):
    sort_cactus_matrix(size)

    # 4. Рекурсивный сбор (дает n^2 кактусов):
    core_move(0, 0)
    harvest()
