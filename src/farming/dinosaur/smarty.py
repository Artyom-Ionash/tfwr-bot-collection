def main():
    while True:
        # 1. Подготовка
        change_hat(Hats.Brown_Hat)
        if num_items(Items.Cactus) < 1000:
            farm_cactus_quickly()

        # 2. Сброс в начало
        reset_to_start()

        # 3. Умная змейка
        change_hat(Hats.Dinosaur_Hat)
        run_smart_snake()


def run_smart_snake():
    size = get_world_size()
    total_cells = size * size

    # Считаем длину хвоста. Начальная длина = 1 (голова)
    # Добавляем небольшой буфер (+2), чтобы не рисковать при лагах
    snake_len = 3

    target_pos = measure()

    while True:
        # Следим за яблоком
        new_target = measure()
        if new_target != target_pos:
            snake_len += 1
            target_pos = new_target

        x = get_pos_x()
        y = get_pos_y()

        # 1. Получаем стандартный безопасный ход (по рельсам)
        rail_dir = get_rail_direction(x, y, size)

        # 2. Пытаемся оптимизировать (срезать путь)
        final_dir = rail_dir

        if target_pos != None:
            tx, ty = target_pos

            # Находим лучшее направление среди всех 4 сторон
            best_shortcut = None
            min_dist_to_apple = 9999

            # Проверяем все 4 направления
            # Порядок: North, East, South, West
            for d in (North, East, South, West):
                # Координаты соседа
                nx, ny = get_neighbor(x, y, d)

                # Проверка выхода за границы
                if nx < 0 or nx >= size or ny < 0 or ny >= size:
                    continue

                # Вычисляем индексы (позиция на пути змейки)
                idx_current = get_hamiltonian_index(x, y, size)
                idx_neighbor = get_hamiltonian_index(nx, ny, size)
                idx_target = get_hamiltonian_index(tx, ty, size)

                # Длина прыжка по циклу (сколько клеток мы пропускаем)
                # (idx_neighbor - idx_current) % total_cells
                # Если прыжок = 1, это обычный ход. Если > 1, это срез.
                jump_size = (idx_neighbor - idx_current) % total_cells

                # --- ГЛАВНОЕ УСЛОВИЕ БЕЗОПАСНОСТИ ---
                # Мы можем срезать, только если оставшаяся длина петли
                # больше длины змейки.
                # То есть: Total - jump_size > snake_len
                # Или: jump_size < (Total - snake_len)
                allowed_jump = total_cells - snake_len

                if jump_size < allowed_jump:
                    # Ход безопасен. Проверяем, выгоден ли он?
                    # Считаем Манхэттенское расстояние до яблока от соседа
                    dist_to_apple = abs(nx - tx) + abs(ny - ty)

                    if dist_to_apple < min_dist_to_apple:
                        min_dist_to_apple = dist_to_apple
                        best_shortcut = d
                    # Если расстояние такое же, но это "рельсовый" ход, он в приоритете
                    elif dist_to_apple == min_dist_to_apple and d == rail_dir:
                        best_shortcut = d

            # Если нашли хороший срез, используем его
            if best_shortcut != None:
                final_dir = best_shortcut

        # 3. Выполняем движение
        # Перед движением можно сделать harvest, чтобы убрать внезапные препятствия
        harvest()
        if not move(final_dir):
            # Если не смогли двигаться (врезались), выходим
            break


def get_neighbor(x, y, direction):
    if direction == North:
        return x, y + 1
    if direction == East:
        return x + 1, y
    if direction == South:
        return x, y - 1
    if direction == West:
        return x - 1, y
    return x, y


def get_hamiltonian_index(x, y, size):
    # 1. Магистраль возврата (y=0, x > 0)
    # Это самый конец цикла.
    # Путь идет x=Size-1 -> x=1.
    # Индексы: от (Total - (Size - 1)) до (Total - 1)
    if y == 0 and x > 0:
        # Чем больше x, тем меньше индекс (потому что идем влево)
        # return (size * size) - x
        # Проверим: x=1 (последний шаг перед 0,0). Index должен быть Max.
        # x=size-1 (начало возврата). Index должен быть поменьше.
        return (size * size) - x

    # 2. Столбцы
    # Базовое смещение для столбца X.
    # Столбец 0 имеет size клеток. Остальные имеют size-1 клеток.
    if x == 0:
        return y

    # Для x > 0, мы пропустили Col 0 (size клеток)
    # и (x-1) столбцов по (size-1) клеток.
    base = size + (x - 1) * (size - 1)

    # Последний столбец: всегда ВНИЗ (согласно вашему коду)
    if x == size - 1:
        # Идет от y=size-1 до y=1
        # Смещение внутри столбца: (size - 1) - y
        return base + ((size - 1) - y)

    # Четные (Вверх)
    if x % 2 == 0:
        # Идет от y=1 до y=size-1
        # Смещение: y - 1
        return base + (y - 1)

    # Нечетные (Вниз)
    else:
        # Идет от y=size-1 до y=1
        # Смещение: (size - 1) - y
        return base + ((size - 1) - y)


def get_rail_direction(x, y, size):
    # Точная копия логики из вашего рабочего кода
    if y == 0 and x > 0:
        return West
    elif x == size - 1:
        if y > 0:
            return South
        else:
            return West
    elif x % 2 == 0:
        if y < size - 1:
            return North
        else:
            return East
    else:
        if y > 1:
            return South
        else:
            return East


def reset_to_start():
    while get_pos_x() > 0:
        harvest()
        move(West)
    while get_pos_y() > 0:
        harvest()
        move(South)
    harvest()


def farm_cactus_quickly():
    change_hat(Hats.Brown_Hat)
    while num_items(Items.Cactus) < 2000:
        if get_ground_type() != Grounds.Soil:
            till()
        if can_harvest():
            harvest()
        else:
            plant(Entities.Cactus)
        move(North)


# Запуск
main()
