# Функции для действий игрока
# labyrinth_game/player_actions.py

def get_input(prompt="> "):
    """Получает ввод от пользователя с обработкой ошибок"""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"


def show_inventory(game_state):
    """Показывает инвентарь игрока"""
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ", ".join(inventory))
    else:
        print("Ваш инвентарь пуст.")
