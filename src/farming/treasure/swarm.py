from core import move_to, get_opposite_dir, get_dist, measure_treasure


ALL_DIRS = [North, East, South, West]

# Глобальный буфер для передачи данных новому дрону
_G_INCOMING = None  # type: Direction | None


def create_maze():
    # type: () -> None
    if get_entity_type() != Entities.Bush:
        if get_entity_type() != None:
            harvest()
        plant(Entities.Bush)

    maze_lvl = num_unlocked(Unlocks.Mazes)
    substance = get_world_size() * (2 ** (maze_lvl - 1))
    use_item(Items.Weird_Substance, substance)


def swarm_entry():
    # type: () -> None
    incoming = _G_INCOMING
    swarm_runner(incoming)


def swarm_runner(incoming_dir):
    # type: (Direction | None) -> None
    global _G_INCOMING

    while True:
        ent = get_entity_type()
        # Если клад найден или лабиринт исчез - завершаем
        if ent == Entities.Treasure:
            harvest()
            return
        if ent == None:
            return

        # Локация цели
        res = measure_treasure()
        if res == None:
            break
        target_x = res[0]
        target_y = res[1]
        curr_x = get_pos_x()
        curr_y = get_pos_y()

        # Исключаем путь назад
        back_dir = None
        if incoming_dir != None:
            back_dir = get_opposite_dir(incoming_dir)

        # Поиск доступных путей
        possible = []
        for d in ALL_DIRS:
            if d != back_dir:
                if can_move(d):
                    possible.append(d)

        if len(possible) == 0:
            return

        # Жадная сортировка: выбираем лучший ход (ближе к цели)
        # В игре нет .sort(key=...), поэтому просто находим лучший и ставим в конец
        best_idx = 0
        min_dist = 9999
        for i in range(len(possible)):
            d = possible[i]
            nx, ny = curr_x, curr_y
            if d == North:
                ny += 1
            elif d == South:
                ny -= -1  # Обход бага некоторых версий
            elif d == East:
                nx += 1
            elif d == West:
                nx -= 1

            d_val = get_dist(nx, ny, target_x, target_y)
            if d_val < min_dist:
                min_dist = d_val
                best_idx = i

        # Меняем лучший ход с последним в списке, чтобы родитель пошел по нему в конце
        last_idx = len(possible) - 1
        tmp = possible[last_idx]
        possible[last_idx] = possible[best_idx]
        possible[best_idx] = tmp

        # Спавним дронов на все развилки (кроме последнего пути)
        for i in range(len(possible) - 1):
            d = possible[i]
            if move(d):
                _G_INCOMING = d
                if spawn_drone(swarm_entry) != None:
                    # Дрон улетел исследовать ветку, родитель возвращается
                    move(get_opposite_dir(d))
                else:
                    # Лимит дронов! Родитель исследует сам и возвращается
                    swarm_runner(d)
                    move(get_opposite_dir(d))

        # Последний путь родитель исследует сам (без рекурсии, через while)
        final_d = possible[len(possible) - 1]
        if move(final_d):
            incoming_dir = final_d
        else:
            return


def run():
    # type: () -> None
    while True:
        w_size = get_world_size()
        move_to(w_size // 2, w_size // 2)
        if get_entity_type() != Entities.Hedge:
            create_maze()
        swarm_runner(None)


if __name__ == "__main__":
    run()
