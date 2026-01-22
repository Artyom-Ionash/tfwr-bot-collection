from core import (
    move_to,
    generate_closed_path,
    await_harvest,
    measure_cactus,
    safe_plant,
)


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

            move_to(target_x, y)

            if get_entity_type() != Entities.Cactus:
                safe_plant(Entities.Cactus)

                # Активация поликультуры для ускорения роста:
                comp_data = get_companion()
                if comp_data != None:
                    c_type, c_pos = comp_data
                    home_x, home_y = get_pos_x(), get_pos_y()
                    move_to(c_pos[0], c_pos[1])
                    safe_plant(c_type)
                    move_to(home_x, home_y)


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

            move_to(x, y)

            # Проверка соседа справа (East):
            if x < size - 1:
                if measure_cactus() > measure_cactus(East):
                    swap(East)
                    swapped = True
                    last_swap_index = i

            # Проверка соседа сверху (North):
            if y < size - 1:
                if measure_cactus() > measure_cactus(North):
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
            move_to(i % size, i // size)
            # Если не кактус или еще не вырос:
            if get_entity_type() != Entities.Cactus:
                safe_plant(Entities.Cactus)
                ready = False
            elif not can_harvest():
                ready = False

    # 3. Сортировка (превращаем поле в ярко-зеленое):
    sort_cactus_matrix(size)

    # 4. Рекурсивный сбор (дает n^2 кактусов):
    move_to(0, 0)
    harvest()
