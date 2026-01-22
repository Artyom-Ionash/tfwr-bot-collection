from core import move_to, generate_closed_path, await_harvest, safe_plant


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
        move_to(c_x, c_y)
        safe_plant(c_type)

        # Возвращаемся к основному дереву
        move_to(old_x, old_y)


# --- ОСНОВНОЙ ЦИКЛ ---

size = get_world_size()

# Инициализация поля (первичная застройка)
for x in range(size):
    for y in range(size):
        move_to(x, y)
        if (x + y) % 2 == 0:
            safe_plant(Entities.Tree)
        else:
            safe_plant(Entities.Grass)

while True:
    for x in range(size):
        for y in range(size):
            # Работаем только по шахматной сетке для деревьев
            if (x + y) % 2 == 0:
                move_to(x, y)

                # 1. Проверка: если дерево созрело — собираем и сажаем заново
                if can_harvest():
                    harvest()
                    safe_plant(Entities.Tree)
                    # После пересадки сразу ищем нового компаньона
                    manage_companions()

                # 2. Проверка: если клетка вдруг пустая — засаживаем
                elif get_entity_type() == None:
                    safe_plant(Entities.Tree)
                    manage_companions()

                # 3. Опционально: полив, если дерево еще растет
                else:
                    if get_water() < 0.6:
                        if num_items(Items.Water) > 0:
                            use_item(Items.Water)
