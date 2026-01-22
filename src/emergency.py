from core import move_to, generate_closed_path, await_harvest


def emergency_harvest_all():
    size = get_world_size()

    for y in range(size):
        # Двигаемся змейкой, чтобы не тратить время на возвраты
        for x in range(size):
            # Если y четный, идем слева направо, если нечетный — справа налево
            actual_x = x
            if y % 2 != 0:
                actual_x = size - 1 - x

            move_to(actual_x, y)

            # 1. Проверяем, есть ли что-то на клетке
            entity = get_entity_type()
            if entity != None:
                # 2. Ждем созревания (чтобы забрать урожай, а не просто удалить)
                # Это важно для кактусов, деревьев и тыкв
                while not can_harvest():
                    # Если есть вода, ускоряем процесс, чтобы не стоять долго
                    if get_water() < 0.5:
                        if num_items(Items.Water) > 0:
                            use_item(Items.Water)
                    # Если это сорняк, он может не созреть, его просто срезаем
                    if entity == Entities.Bush:  # Пример для сорняков
                        break

                # 3. Собираем содержимое
                harvest()

            # 4. Приводим почву в базовое состояние (травяной луг)
            # Это полезно, чтобы следующий скрипт начал с "чистого листа"
            if get_ground_type() == Grounds.Soil:
                till()

    # Возвращаемся в начало
    move_to(0, 0)


change_hat(Hats.Brown_Hat)

emergency_harvest_all()
