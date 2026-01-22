clear()

# ====================================================================
# [CORE] - СИСТЕМНЫЕ ФУНКЦИИ
# ====================================================================


def core_prepare(ground_type, water_threshold):
    if get_ground_type() != ground_type:
        till()
    if get_water() < water_threshold:
        if num_items(Items.Water) > 0:
            use_item(Items.Water)


def core_plant(entity, seed, ground, water):
    core_prepare(ground, water)
    curr = get_entity_type()
    if curr != entity and curr != None:
        if can_harvest():
            harvest()
    if get_entity_type() == None:
        # Автозакупка (Морковь или Тыква)
        if seed != None:
            print("Семена закончились!")
        plant(entity)


def core_move_snake(n, size):
    x = get_pos_x()
    y = get_pos_y()
    if n < (size * size) - 1:
        if x % 2 == 0:
            if y < size - 1:
                move(North)
            else:
                move(East)
        else:
            if y > 0:
                move(South)
            else:
                move(East)


# ====================================================================
# [STRATEGIES] - ЛОГИКА КУЛЬТУР
# ====================================================================


def manage_carrots():
    # Режим моркови: посадка и мгновенный сбор
    core_plant(Entities.Carrot, Items.Carrot, Grounds.Soil, 0.6)
    if can_harvest():
        harvest()
    return True


def manage_pumpkins(gold_limit):
    # Режим тыкв: ожидание синхронизации для гигантских форм
    core_plant(Entities.Pumpkin, Items.Pumpkin, Grounds.Soil, 0.9)
    if can_harvest():
        return True
    return False


# ====================================================================
# [MAIN] - УПРАВЛЯЮЩИЙ ЦИКЛ
# ====================================================================

# cfg: [0]HayLim, [1]WoodLim, [2]GoldBuf, [3]CoreSize, [4]MODE
# MODE 0: Морковь (по умолчанию), MODE 1: Тыквы
cfg = [1000, 1000, 2000, 10, 0]
world_size = get_world_size()

while True:
    all_ready = True

    for n in range(world_size * world_size):
        if n < cfg[3]:
            # Энерго-ядро: подсолнухи бесплатны и бесконечны
            core_plant(Entities.Sunflower, None, Grounds.Soil, 0.5)
        else:
            # Проверка лимитов сена и дерева
            if num_items(Items.Hay) < cfg[0]:
                core_plant(Entities.Grass, None, Grounds.Grassland, 0.0)
                all_ready = False
            elif num_items(Items.Wood) < cfg[1]:
                if (get_pos_x() + get_pos_y()) % 2 == 0:
                    core_plant(Entities.Tree, None, Grounds.Grassland, 0.0)
                else:
                    core_plant(Entities.Grass, None, Grounds.Grassland, 0.0)
                all_ready = False
            else:
                # Выбор стратегии заработка
                if cfg[4] == 0:
                    manage_carrots()
                else:
                    if not manage_pumpkins(cfg[2]):
                        all_ready = False

        core_move_snake(n, world_size)

    # Массовая жатва тыкв (только если выбраны тыквы и все созрели)
    if cfg[4] == 1:
        if all_ready:
            while get_pos_x() > 0:
                move(West)
            while get_pos_y() > 0:
                move(South)
            for n in range(world_size * world_size):
                if n >= cfg[3]:
                    harvest()
                core_move_snake(n, world_size)

    # Возврат в точку 0,0 для стабильности
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)
