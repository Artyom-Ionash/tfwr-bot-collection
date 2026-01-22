from core import move_to, generate_closed_path, await_harvest

# Направления для обхода
DIRS = [North, East, South, West]
# Противоположные направления для возврата
OPPOSITES = {
    North: South,
    East: West,
    South: North,
    West: East,
}  # type: dict[Direction, Direction]


# type: () -> None
def create_maze():
    # 1. Подготовка куста
    if get_entity_type() != Entities.Bush:
        if get_entity_type() is not None:
            harvest()
        plant(Entities.Bush)

    # 2. Расчет вещества (по формуле из документации)
    # n * 2^(уровень - 1)
    maze_lvl = num_unlocked(Unlocks.Mazes)
    substance_amount = get_world_size() * (2 ** (maze_lvl - 1))

    # 3. Превращение в лабиринт
    use_item(Items.Weird_Substance, substance_amount)


# type: () -> None
def solve_maze():
    visited = set()  # type: set[tuple[int, int]]
    path_stack = []  # type: list[Direction]

    start_pos = (get_pos_x(), get_pos_y())
    visited.add(start_pos)

    while get_entity_type() != Entities.Treasure:
        current_pos = (get_pos_x(), get_pos_y())
        moved = False

        # Пробуем пойти в любую неразведанную сторону
        for d in DIRS:
            if can_move(d):
                # Симулируем координаты после шага
                new_x, new_y = current_pos
                if d == North:
                    new_y += 1
                elif d == South:
                    new_y -= 1
                elif d == East:
                    new_x += 1
                elif d == West:
                    new_x -= 1

                # Зацикливание мира (если поле зациклено)
                new_x %= get_world_size()
                new_y %= get_world_size()

                if (new_x, new_y) not in visited:
                    if move(d):
                        visited.add((new_x, new_y))
                        path_stack.append(d)
                        moved = True
                        break

        # Если зашли в тупик - возвращаемся назад по стеку
        if not moved:
            if not path_stack:
                quick_print("Ошибка: Клад не найден, стек пуст")
                break
            last_dir = path_stack.pop()
            move(OPPOSITES[last_dir])

    # Нашли сокровище!
    harvest()


# type: () -> None
def run():
    while True:
        # Перемещаемся в точку старта (0,0), чтобы строить лабиринт всегда там
        # (Или в любую удобную свободную точку)
        move_to(0, 0)

        if (
            get_entity_type() != Entities.Treasure
            and get_entity_type() != Entities.Hedge
        ):
            create_maze()

        solve_maze()


if __name__ == "__main__":
    run()
