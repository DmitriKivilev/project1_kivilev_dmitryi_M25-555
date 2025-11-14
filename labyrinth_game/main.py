#!/usr/bin/env python3

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)

# Состояние игры
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}


def process_command(game_state, command):
    """Обрабатывает команды игрока"""
    parts = command.split()
    if not parts:
        return
    
    main_command = parts[0]
    argument = parts[1] if len(parts) > 1 else ""
    
    match main_command:
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go" if argument:
            move_player(game_state, argument)
            describe_current_room(game_state)
        case "take" if argument:
            take_item(game_state, argument)
        case "use" if argument:
            use_item(game_state, argument)
        case "solve":
            if game_state['current_room'] == 'treasure_room' and 'treasure_key' in game_state['player_inventory']:
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "north" | "south" | "east" | "west":
            move_player(game_state, main_command)
            describe_current_room(game_state)
        case "help":
            show_help(COMMANDS)
        case "quit" | "exit":
            game_state['game_over'] = True
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Для выхода введите 'quit'")
    
    # Описание стартовой комнаты
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        process_command(game_state, command)
    
    print("Спасибо за игру!")


if __name__ == "__main__":
    main()
