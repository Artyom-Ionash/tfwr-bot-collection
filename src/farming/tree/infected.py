from core import move_to, generate_closed_path, await_harvest

# --- ГИПЕРПАРАМЕТРЫ СЕКТОРА ---
# Размер анализируемой области (меньше область = быстрее реакция)
SECTOR_W = 4  # type: int
SECTOR_H = 4  # type: int

# Смещение (откуда начинать сектор)
OFFSET_X = 0  # type: int
OFFSET_Y = 0  # type: int

# --- НАСТРОЙКИ КУЛЬТУР ---
MAIN_CROP = Entities.Tree
COMPANION_CROP = Entities.Bush


# type: (int, int, int, int) -> list[tuple[int, int]]
def generate_sector_path(start_x, start_y, w, h):
    path = []  # type: list[tuple[int, int]]
    for i in range(w):
        curr_x = start_x + i
        # Змейка внутри сектора
        if i % 2 == 0:
            for y in range(h):
                path.append((curr_x, start_y + y))
        else:
            for y in range(h - 1, -1, -1):
                path.append((curr_x, start_y + y))
    return path


# type: () -> None
def farm_infected_trees():
    # 1. Генерация локального маршрута
    path = generate_sector_path(OFFSET_X, OFFSET_Y, SECTOR_W, SECTOR_H)

    while True:
        for x, y in path:
            move_to(x, y)

            # Шахматная логика для Поликультуры
            # С учетом смещения, чтобы паттерн не ломался при переносе сектора
            is_main_spot = (x + y) % 2 == 0  # type: bool

            # Подготовка почвы
            if get_ground_type() != Grounds.Soil:
                till()

            current_ent = get_entity_type()

            if is_main_spot:
                # ЛОГИКА ДЕРЕВА
                if current_ent != MAIN_CROP:
                    if current_ent != None:
                        harvest()
                    plant(MAIN_CROP)

                # Использование ресурсов
                if can_harvest():
                    harvest()
                    plant(MAIN_CROP)

                # Применяем удобрение только к деревьям
                if num_items(Items.Fertilizer) > 0:
                    use_item(Items.Fertilizer)

                # Полив важен для скорости роста без удобрений
                if num_items(Items.Water) > 0:
                    use_item(Items.Water)

            else:
                # ЛОГИКА КОМПАНИОНА (Поликультура)
                if current_ent != COMPANION_CROP:
                    if current_ent != None:
                        harvest()
                    plant(COMPANION_CROP)

                # Компаньонов (кусты) не удобряем, просто держим их живыми
                if can_harvest():
                    # Собираем только если это выгодно, иначе оставляем для баффа
                    harvest()
                    plant(COMPANION_CROP)


# Запуск
if __name__ == "__main__":
    farm_infected_trees()
