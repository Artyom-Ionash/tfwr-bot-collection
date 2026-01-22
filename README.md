# 🚜 The Farmer Was Replaced: Ultimate Bot

> Модульный набор скриптов для автоматизации фермерства, написанный на Python с использованием современного инструментария разработки (DX) и статического анализа.

[![Game Version](<https://img.shields.io/badge/Game_Version-20387553_(Oct_2025)-4b32c3>)](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/)
[![Python](https://img.shields.io/badge/Python-Legacy_Syntax-yellow)](https://www.python.org/)
[![Pyright](https://img.shields.io/badge/Pyright-Strict-blue)](https://microsoft.github.io/pyright/)
[![VS Code](https://img.shields.io/badge/VS_Code-Ready-007acc)](https://code.visualstudio.com/)

[📚 Архитектура](./docs/ARCHITECTURE.md) | [📉 Технический долг](./docs/TECH_DEBT.md)

## ✨ Возможности

- 🎃 **Smart Strategies** — Адаптивные алгоритмы для Тыкв, Деревьев, Динозавров и Подсолнухов.
- 🧭 **Robust Navigation** — Умная маршрутизация дрона ("гамильтонов цикл").
- 🧩 **Modular Core** — Единое ядро (`core.py`) с переиспользуемыми примитивами (Navigation, Inventory, Actions).
- 🛠 **Type Safe** — Частичная поддержка IntelliSense и проверки типов в VS Code благодаря системе Mocking.

## 🛠 Технические особенности

Проект решает главную проблему разработки под эту игру — отсутствие привычных разработчикам инструментов отладки:

- **Zero-Runtime Overhead:** Код полностью совместим со встроенным интерпретатором игры (нет `import typing`, нет сторонних библиотек).
- **Static Mocking:** Использование `typings/builtins.pyi` эмулирует API игры для VS Code.
- **Type Comments (PEP 484):** Использование `# type: (...)` вместо аннотаций для совместимости со старым синтаксисом Python.

## 📚 Документация

Мы стремимся к чистой архитектуре. Подробности разнесены по файлам:

- [🏛 Архитектура (ARCHITECTURE.md)](./docs/ARCHITECTURE.md) — Принципы разделения ядра и стратегий, работа с Mock-окружением.
- [📉 Технический долг (TECH_DEBT.md)](./docs/TECH_DEBT.md) — Известные ограничения (Grid Logic, Monolith Core) и Roadmap.

## 🚀 Начало работы

### Предварительные требования

1.  VS Code с расширением **Python (Pylance)**.

### Установка окружения

```bash
# Клонирование репозитория
git clone https://github.com/your-repo/farmer-bot.git
```

### Разработка

1.  Откройте проект в VS Code.
2.  Благодаря файлу `pyrightconfig.json` и папке `typings/`, редактор автоматически подхватит API игры.
3.  Пишите код в `src/farming/`. Используйте `core.py` для общих задач.

### РАзвёртывание в игре

Так как игра не поддерживает импорты файлов с диска:

1.  Скопируйте содержимое `core.py` в буфер обмена.
2.  Вставьте в начало игрового файла.
3.  Скопируйте нужную стратегию (например, `src/farming/pumpkin.py`) и вставьте ниже.
4.  Нажмите **Run** внутри игры.

## 🤖 Совместимость

Проект протестирован и оптимизирован под:

- **Game Build:** `20387553` (Октябрь 2025).
- **Python Runtime:** Встроенный интерпретатор игры (ограниченное подмножество Python).

> **Примечание:** Если API игры изменится (новые предметы или функции), необходимо обновить `typings/builtins.pyi`.
