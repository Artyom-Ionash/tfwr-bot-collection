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
    # Выбор типа почвы
    target_ground = Grounds.Soil
    if entity == Entities.Tree or entity == Entities.Grass:
        target_ground = Grounds.Grassland

    if get_ground_type() != target_ground:
        till()

    if get_entity_type() != entity:
        if can_harvest():
            harvest()
        plant(entity)


# ====================================================================
# [STRATEGY] - ИНИЦИАЛИЗАЦИЯ И ПОДДЕРЖКА
# ====================================================================


def fill_all_field(size):
    # Первый проход: засаживаем всё поле базово
    for x in range(size):
        for y in range(size):
            core_move(x, y)
            if (x + y) % 2 == 0:
                core_safe_plant(Entities.Tree)
            else:
                core_safe_plant(Entities.Grass)


def manage_companions():
    # Функция проверяет дерево под дроном и летит сажать ему компаньона
    comp_data = get_companion()
    if comp_data != None:
        c_type = comp_data[0]
        c_pos = comp_data[1]
        c_x = c_pos[0]
        c_y = c_pos[1]

        # Запоминаем текущую позицию
        old_x = get_pos_x()
        old_y = get_pos_y()

        # Летим сажать компаньона
        core_move(c_x, c_y)
        core_safe_plant(c_type)

        # Возвращаемся обратно к дереву
        core_move(old_x, old_y)


# ====================================================================
# [MAIN] - ЦИКЛ РАБОТЫ
# ====================================================================

size = get_world_size()

# 1. Инициализация (заполняем поле сразу)
fill_all_field(size)

# 2. Основной цикл (сбор и умная подсадка)
while True:
    for x in range(size):
        for y in range(size):
            # Работаем только с клетками деревьев (шахматка)
            if (x + y) % 2 == 0:
                core_move(x, y)

                # Если дерево созрело - собираем
                if can_harvest():
                    harvest()
                    core_safe_plant(Entities.Tree)

                # Если дерева нет (пусто) - сажаем
                if get_entity_type() == None:
                    core_safe_plant(Entities.Tree)

                # Проверяем/обновляем компаньона для этой клетки
                manage_companions()

            # На нечетных клетках ничего не делаем специально,
            # их заполнит функция manage_companions
