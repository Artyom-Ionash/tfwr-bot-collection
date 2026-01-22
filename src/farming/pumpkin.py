from core import move_to, generate_closed_path, await_harvest, safe_plant


def farm_pumpkins():
    w = get_world_size()
    h = get_world_size()

    # Генерируем маршрут один раз
    path = generate_closed_path(w, h)

    while True:
        all_ready = True
        has_mature = False
        suspects = []  # Список координат с подозрением на "мертвые" тыквы

        # --- Проход 1: Полив, посадка и анализ ---
        for x, y in path:
            move_to(x, y)

            # 3. Посадка
            if get_entity_type() != Entities.Pumpkin:
                safe_plant(Entities.Pumpkin)
                all_ready = False
                continue

            # 4. Анализ состояния
            if can_harvest():
                has_mature = True
            else:
                # Клетка занята, но не готова.
                all_ready = False
                plant(Entities.Pumpkin)

        # --- Проход 2: Синхронизация поля ---

        if all_ready:
            # Идеальный сценарий: все поле готово, собираем Мега-Тыкву
            harvest()


# Запуск
farm_pumpkins()
