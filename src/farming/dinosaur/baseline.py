def main():
    while True:
        # 1. Подготовка
        change_hat(Hats.Brown_Hat)

        # Если кактусов мало, фармим их
        if num_items(Items.Cactus) < 1000:
            farm_cactus_quickly()

        # 2. Идем на старт (0,0) и чистим поле
        reset_to_start()

        # 3. Запуск Динозавра
        change_hat(Hats.Dinosaur_Hat)
        run_dino_cycle()


def run_dino_cycle():
    size = get_world_size()

    while True:
        x = get_pos_x()
        y = get_pos_y()

        # Очищаем клетку перед собой.
        # Яблоки появляются только на пустой земле.
        harvest()

        dest = North

        # --- Логика движения (Гамильтонов цикл) ---
        # Предполагаем (0,0) в нижнем левом углу.

        # 1. Возвратная магистраль (самый низ, y=0)
        # Если мы внизу, но не в начале (0,0), бежим влево
        if y == 0 and x > 0:
            dest = West

        # 2. Последний столбец
        # Всегда спускаемся вниз, чтобы попасть на магистраль
        elif x == size - 1:
            if y > 0:
                dest = South
            else:
                dest = West

        # 3. Четные столбцы (0, 2, 4...) - ВВЕРХ
        elif x % 2 == 0:
            if y < size - 1:
                dest = North
            else:
                dest = East  # Переход вправо на самом верху

        # 4. Нечетные столбцы (1, 3, 5...) - ВНИЗ (до y=1)
        else:
            if y > 1:
                dest = South
            else:
                dest = East  # Переход вправо на уровне y=1 (y=0 занят возвратом)

        # Пытаемся сделать шаг
        can_move = move(dest)

        # Если move вернул False, змейка заполнила поле
        if not can_move:
            break


def reset_to_start():
    # Идет в точку (0,0), очищая путь
    # Сначала идем влево
    while get_pos_x() > 0:
        harvest()
        move(West)

    # Потом идем вниз
    while get_pos_y() > 0:
        harvest()
        move(South)

    # Финальная очистка (0,0)
    harvest()


def farm_cactus_quickly():
    # Быстрый сбор кактусов
    change_hat(Hats.Brown_Hat)
    print("Farming cactus...")
    while num_items(Items.Cactus) < 2000:
        # Если почва не вспахана - вспахиваем
        # Вместо несуществующего Turf проверяем != Soil
        if get_ground_type() != Grounds.Soil:
            till()

        if can_harvest():
            harvest()
        else:
            plant(Entities.Cactus)

        move(North)


main()
