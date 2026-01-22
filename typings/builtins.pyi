# Мы импортируем вспомогательные инструменты для типов.
# Pylance понимает этот импорт, но в саму игру он не попадет.
from typing import (
    TypeVar,
    Generic,
    Iterator,
    Literal,
    TypeAlias,
    Optional,
    Tuple,
    List,
    Dict,
    TypeGuard,
    Any,
    Callable,
)

def is_int(val: Any) -> TypeGuard[int]:
    """Проверяет, является ли значение целым числом (ID или размер)."""

# Объявляем переменные типа (шаблоны)
_T = TypeVar("_T")
_T_co = TypeVar("_T_co", covariant=True)
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

# === ЧАСТЬ 1: ФУНДАМЕНТ PYTHON ===

class object:
    def __init__(self) -> None: ...

class type: ...

class NoneType:
    def __bool__(self) -> bool: ...

# --- Базовые типы ---

# Числа
class int:
    def __add__(self, other: int) -> int: ...
    def __sub__(self, other: int) -> int: ...
    def __mul__(self, other: int) -> int: ...
    def __pow__(self, other: int) -> int: ...
    def __truediv__(self, other: object) -> float: ...
    def __floordiv__(self, other: object) -> int: ...
    def __mod__(self, other: object) -> int: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...
    def __le__(self, other: object) -> bool: ...
    def __ge__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __abs__(self) -> int: ...
    def __hash__(self) -> int: ...

class float:
    def __add__(self, other: object) -> float: ...
    def __sub__(self, other: object) -> float: ...
    def __lt__(self, other: object) -> bool: ...
    def __gt__(self, other: object) -> bool: ...

class bool(int): ...

class str:
    def __add__(self, other: object) -> str: ...
    def format(self, *args: object, **kwargs: object) -> str: ...
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...

# --- Коллекции (Generic) ---

# Добавляем Generic[_T], чтобы работало list[int]
class list(Generic[_T]):
    def append(self, item: _T) -> None: ...
    def pop(self, index: int = -1) -> _T: ...
    def remove(self, item: _T) -> None: ...
    def __len__(self) -> int: ...
    # Iterator позволяет делать "for x in list" с правильным типом x
    def __iter__(self) -> Iterator[_T]: ...
    def __getitem__(self, index: int) -> _T: ...
    def __setitem__(self, index: int, value: _T) -> None: ...

# Добавляем Generic[_T_co], чтобы работало tuple[int, int]
# Pylance обрабатывает tuple магически, но Generic нужен для синтаксиса []
class tuple(Generic[_T_co]):
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T_co]: ...
    def __getitem__(self, index: int) -> _T_co: ...
    def __mul__(self, other: int) -> tuple: ...

# Добавляем set
class set(Generic[_T]):
    def add(self, item: _T) -> None: ...
    def remove(self, item: _T) -> None: ...
    def __contains__(self, item: object) -> bool: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_T]: ...

class dict(Generic[_KT, _VT]):
    def get(self, key: _KT, default: object = None) -> _VT: ...
    def __getitem__(self, key: _KT) -> _VT: ...
    def __setitem__(self, key: _KT, value: _VT) -> None: ...
    def __contains__(self, key: object) -> bool: ...
    def items(self) -> Iterator[tuple[_KT, _VT]]: ...
    def keys(self) -> Iterator[_KT]: ...
    def values(self) -> Iterator[_VT]: ...

class range:
    def __iter__(self) -> Iterator[int]: ...

# --- Глобальные функции ---
def len(obj: object) -> int: ...
def abs(x: object) -> int: ...
def min(a: object, b: object) -> int: ...
def max(a: object, b: object) -> int: ...

# --- TYPE ALIASES ---
# Определяем Vector2 как кортеж из двух целых чисел
Vector2 = Tuple[int, int]
# Определяем путь как список таких векторов
Path = List[Vector2]

# === ЧАСТЬ 2: API ИГРЫ ===

# 1. Создаем "Призрачный тип" для всех направлений
# Он нужен только для того, чтобы объединить константы в одну группу
class _DirectionObject:
    # Явно разрешаем сравнение (eq)
    def __eq__(self, other: object) -> bool: ...
    def __ne__(self, other: object) -> bool: ...
    # Разрешаем использование в качестве ключей словаря/множества
    def __hash__(self) -> int: ...

# 2. Объявляем North, East... как ЭКЗЕМПЛЯРЫ этого типа
# Теперь для анализатора они "одного поля ягоды" и их можно сравнивать
North: _DirectionObject
East: _DirectionObject
South: _DirectionObject
West: _DirectionObject

# 3. Общий тип (принимает и наши объекты, и числа 0-3)
Direction: TypeAlias = _DirectionObject | int

class Items:
    # Теперь анализатор знает точное значение
    Water: Literal["Water"]
    Wood: Literal["Wood"]
    Hay: Literal["Hay"]
    Power: Literal["Power"]
    Cactus: Literal["Cactus"]
    Pumpkin: Literal["Pumpkin"]
    Carrot: Literal["Carrot"]
    Fertilizer: Literal["Fertilizer"]
    Weird_Substance: Literal["Weird_Substance"]

# Группируем их в один тип для удобства аргументов функций
ItemType: TypeAlias = Literal[
    "Water",
    "Wood",
    "Hay",
    "Power",
    "Cactus",
    "Pumpkin",
    "Fertilizer",
    "Weird_Substance",
]

class Entities:
    Pumpkin: Literal["Pumpkin"]
    Grass: Literal["Grass"]
    Bush: Literal["Bush"]
    Tree: Literal["Tree"]
    Carrot: Literal["Carrot"]
    Sunflower: Literal["Sunflower"]
    Hedge: Literal["Hedge"]
    Treasure: Literal["Treasure"]
    Cactus: Literal["Cactus"]

EntityType: TypeAlias = Literal[
    "Pumpkin",
    "Grass",
    "Bush",
    "Tree",
    "Carrot",
    "Sunflower",
    "Hedge",
    "Treasure",
    "Cactus",
]

class Grounds:
    Soil: Literal["Soil"]
    Turf: Literal["Turf"]
    Grassland: Literal["Grassland"]

GroundType: TypeAlias = Literal["Soil", "Turf", "Grassland"]

class Hats:
    Brown_Hat: Literal["Brown_Hat"]
    Dinosaur_Hat: Literal["Dinosaur_Hat"]

HatType: TypeAlias = Literal["Brown_Hat", "Dinosaur_Hat"]

class Unlocks:
    Mazes: Literal["Mazes"]

UnlocksType: TypeAlias = Literal["Mazes"]

# Функции игры
def can_harvest() -> bool:
    """
    Используется, чтобы узнать, созрели ли растения.

    Возвращает `True`, если под дроном есть объект-сущность, доступный для сбора, в противном случае — `False`.

    Выполнение занимает 1 тик.

    Пример:
    ```
    if can_harvest():
        harvest()
    ```
    """
    ...

def can_move(d: Direction) -> bool:
    """
    Проверяет, может ли дрон двигаться в указанном направлении `d`.

    Возвращает `True`, если дрон может двигаться, в противном случае — `False`.

    Выполнение занимает 1 тик.

    Пример:
    ```
    if can_move(North):
        move(North)
    ```
    """
    ...

def change_hat(h: HatType) -> None:
    """
    Меняет шляпу дрона на `h`.

    Возвращает `None`.

    Выполнение занимает 200 тиков.

    Пример:
    ```
    change_hat(Hats.Dinosaur_Hat)
    ```
    """
    ...

def clear() -> None:
    """
    Удаляет всё с фермы, возвращает дрон на позицию `(0,0)` и меняет шляпу на соломенную.

    Возвращает `None`.

    Выполнение занимает 200 тиков.

    Пример:
    ```
    clear()
    ```
    """
    ...

def get_companion() -> Optional[Tuple[EntityType, Vector2]]:
    """
    Получает предпочтительного компаньона для растения под дроном.

    Возвращает кортеж вида (`companion_type`, (`companion_x_position`, `companion_y_position`))

    Выполнение занимает 1 тик.

    Пример:
    ```
    companion = get_companion()
    if companion != None:
        print(companion)
    ```
    """
    ...

def get_cost(thing: object) -> Dict[str, int]:
    """
    Получает стоимость вещи `thing`.

    Если `thing` — это объект-сущность, получает стоимость его посадки.
    Если `thing` — это технология, получает стоимость её разблокировки.

    Возвращает словарь с предметами в качестве ключей и числами в качестве значений. Каждый предмет сопоставлен с необходимым его количеством.
    Возвращает `{}`, если применяется к улучшаемой технологии, достигшей максимального уровня.

    Выполнение занимает 1 тик.

    Пример:
    ```
    cost = get_cost(Unlocks.Carrots)
    for item in cost:
        if num_items(item) < cost[item]:
            print("Недостаточно предметов для разблокировки моркови")
    ```
    """
    ...

def get_entity_type() -> Optional[str]:
    """
    Узнает, какой тип объекта-сущности находится под дроном.

    Возвращает None, если клетка пуста, в противном случае — тип объекта под дроном.

    Выполнение занимает 1 тик.

    Пример:
    ```
    if get_entity_type() == Entities.Grass:
        harvest()
    ```
    """
    ...

def get_ground_type() -> str:
    """
    Узнает, какой тип земли находится под дроном.

    Возвращает тип земли под дроном.

    Выполнение занимает 1 тик.

    Пример:
    ```
    if get_ground_type() != Grounds.Soil:
        till()
    ```
    """
    ...

def get_pos_x() -> int:
    """
    Получает текущую позицию дрона по оси X.
    Значение позиции X начинается с 0 на западе и увеличивается в направлении востока.

    Возвращает число, представляющее текущую координату X дрона.

    Выполнение занимает 1 тик.

    Пример:
    ```
    x, y = get_pos_x(), get_pos_y()
    ```
    """
    ...

def get_pos_y() -> int:
    """
    Получает текущую позицию дрона по оси Y.
    Значение позиции Y начинается с 0 на западе и увеличивается в направлении востока.

    Возвращает число, представляющее текущую координату Y дрона.

    Выполнение занимает 1 тик.

    Пример:
    ```
    x, y = get_pos_x(), get_pos_y()
    ```
    """
    ...

def get_time() -> float:
    """
    Получает текущее время в игре.

    Возвращает время в секундах с начала игры.

    Выполнение занимает 1 тик.

    Пример:
    ```
    start = get_time()

    do_something()

    time_passed = get_time() - start
    ```
    """
    ...

def get_water() -> float:
    """
    Получает текущий уровень воды под дроном.

    Возвращает уровень воды под дроном в виде числа от 0 до 1.

    Выполнение занимает 1 тик.

    Пример:
    ```
    if get_water() < 0.5:
        use_item(Items.Water)
    ```
    """
    ...

def get_world_size() -> int:
    """
    Получает текущий размер фермы.

    Возвращает длину стороны поля с севера на юг.

    Выполнение занимает 1 тик.

    Пример:
    ```
    for i in range(get_world_size()):
        move(North)
    ```
    """
    ...

def harvest() -> None:
    """
    Собирает объект-сущность под дроном.
    Если собрать объект, не подлежащий сбору, он будет уничтожен.

    Возвращает `True`, если объект удален, в противном случае — `False`.

    Выполнение занимает `200` тиков, если объект удален, в противном случае — `1` тик.

    Пример:
    ```
    harvest()
    ```
    """
    ...

def measure(d: Optional[Direction] = None) -> Optional[int | Vector2]:
    """
    Может измерять определенные значения некоторых объектов-сущностей. Результат зависит от объекта.

    Если значение `d` не `None`, измеряет соседний объект в указанном направлении.

    - Возвращает количество лепестков у подсолнуха.
    - Возвращает следующую позицию для клада или яблока.
    - Возвращает размер кактуса.
    - Возвращает загадочное число для тыквы.
    - Возвращает `None` для всех остальных объектов.

    Выполнение занимает 1 тик.

    Пример:
    ```
    num_petals = measure()
    ```
    """
    ...

def move(d: Direction) -> bool:
    """
    Перемещает дрон на одну клетку в указанном направлении `d`.
    Если дрон вылетает за пределы фермы, то появляется с её противоположной стороны.

    ```
    East   =  вправо
    West   =  влево
    North  =  вверх
    South  =  вниз
    ```

    Возвращает `True`, если дрон переместился, в противном случае — `False`.

    Выполнение занимает **200** тиков, если дрон переместился, в противном случае — **1** тик.

    Пример:
    ```
    move(North)
    ```
    """
    ...

def num_items(i: ItemType) -> int:
    """
    Узнает запас предметов `i`.

    Возвращает количество `i` в инвентаре.

    Выполнение занимает `1` тик.

    Пример:
    ```
    if num_items(Items.Fertilizer) > 0:
        use_item(Items.Fertilizer)
    ```
    """
    ...

def num_unlocked(thing: EntityType | ItemType | UnlocksType) -> int:
    """
    Используется для проверки, разблокированы ли технология, объект-сущность, земля, предмет или шляпа.

    Возвращает 1 плюс количество выполненных улучшений вещи `thing`, если её можно улучшать. В противном случае возвращает 1, если `thing` разблокирована, 0 — если нет.

    Выполнение занимает 1 тик.

    Пример:
    ```
    plant(Entities.Bush)
    n_substance = get_world_size() * num_unlocked(Unlocks.Mazes)
    use_item(Items.Weird_Substance, n_substance)
    ```
    """
    ...

def plant(e: EntityType) -> None:
    """
    Сажает указанный объект-сущность entity под дроном, потратив ресурсы.
    Не сработает, если не хватает ресурсов, не подходит тип земли или на этом месте уже что-то растет.

    Возвращает `True` в случае успеха, в противном случае — `False`.

    Выполнение занимает 200 тиков в случае успеха, в противном случае — 1 тик.

    Пример:
    ```
    plant(Entities.Bush)
    ```
    """
    ...

def print(*args: object) -> None:
    """
    Выводит все аргументы args в воздухе над дроном с помощью дыма. На это действие не влияет повышение скорости.
    Можно вывести несколько значений одновременно.

    Возвращает `None`.

    Выполнение занимает 1 секунду.

    Пример:
    ```
    print("Земля:", get_ground_type())
    ```
    """
    ...

def quick_print(msg: object) -> None:
    """
    Выводит значение так же, как print(*args), но не останавливается, чтобы написать его в воздухе. Значение можно увидеть только на странице вывода.

    Возвращает `None`.

    Выполнение занимает 0 тиков.

    Пример:
    ```
    quick_print("привет, мам")
    ```
    """
    ...

def swap(d: Direction) -> None:
    """
    Меняет местами объект-сущность под дроном с другим, находящимся рядом в указанном направлении `d`.
    Совместимо не со всеми объектами-сущностями.
    Также действует, если один из объектов (или оба) — `None`.

    Возвращает True в случае успеха, в противном случае — `False`.

    Выполнение занимает 200 тиков в случае успеха, в противном случае — 1 тик.

    Пример:
    ```
    swap(North)
    ```
    """
    ...

def till() -> None:
    """
    Вскапывает землю под дроном, превращая её в грядку `Grounds.Soil`. Если там уже грядка, она возвращается в состояние луга `Grounds.Grassland`.

    Возвращает `None`.

    Выполнение занимает 200 тиков.

    Пример:
    ```
    till()
    ```
    """
    ...

def spawn_drone(filename: Callable):
    """
    На той же позиции, где дрон выполнил команду `spawn_drone(function)`, создает новый дрон. Он начинает выполнять указанную функцию и по завершении автоматически пропадает.

    Возвращает идентификатор нового дрона или `None`, если все дроны уже созданы.

    Выполнение занимает 200 тиков, если дрон был создан, в противном случае — 1.

    Пример:
    ```
    def harvest_column():
        for _ in range(get_world_size()):
            harvest()
            move(North)

    while True:
        if spawn_drone(harvest_column):
            move(East)
    ```
    """
    ...

def use_item(item: ItemType, n=1) -> None:
    """
    Пытается использовать указанный предмет item n раз. Можно использовать только с некоторыми предметами, включая `Items.Water` и `Items.Fertilizer`.

    Возвращает `True`, если предмет был использован, в противном случае — `False`.

    Выполнение занимает 200 тиков в случае успеха, в противном случае — 1 тик.

    Пример:
    ```
    use_item(Items.Fertilizer)
    ```
    """
    ...
