from core import move_to, generate_closed_path, await_harvest, safe_plant

# ====================================================================
# [SMART HARVEST] - ОБВЯЗКА С ПОЛИКУЛЬТУРОЙ
# ====================================================================


def smart_harvest():
    # 1. Проверяем, есть ли под нами растение
    if get_entity_type() == None:
        return

    # 2. Получаем данные о компаньоне
    companion_data = get_companion()

    if companion_data != None:
        c_type = companion_data[0]
        c_pos = companion_data[1]
        c_x = c_pos[0]
        c_y = c_pos[1]

        # Запоминаем текущую позицию
        home_x = get_pos_x()
        home_y = get_pos_y()

        # Быстрый вылет: сажаем компаньона
        move_to(c_x, c_y)
        safe_plant(c_type)

        # Возврат к основной цели
        move_to(home_x, home_y)

    # 3. Финальная проверка на зрелость перед сбором
    while not can_harvest():
        # Пока ждем, поливаем для ускорения
        if get_water() < 0.8:
            if num_items(Items.Water) > 0:
                use_item(Items.Water)

    # 4. Сбор с уже активным бонусом поликультуры
    harvest()


# ====================================================================
# [MAIN] - ПРИМЕР ИСПОЛЬЗОВАНИЯ (Фарм Травы)
# ====================================================================

size = get_world_size()

while True:
    for x in range(3, size - 3):
        for y in range(3, size - 3):
            move_to(x, y)

            # Если клетка пуста — сажаем
            if get_entity_type() == None:
                safe_plant(Entities.Grass)

            # Используем нашу обвязку вместо обычного harvest()
            if can_harvest():
                smart_harvest()
                # После сбора сразу засаживаем заново, чтобы цикл не прерывался
                safe_plant(Entities.Grass)
