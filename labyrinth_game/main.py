#!/usr/bin/env python3

from labyrinth_game.player_actions import get_input, show_inventory
from labyrinth_game.utils import describe_current_room

# Состояние игры
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}


def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("Для выхода введите 'quit'")
    
    # Описание стартовой комнаты
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("\nВведите команду: ")
        
        if command == "quit":
            print("Спасибо за игру!")
            break
        elif command == "inventory":
            show_inventory(game_state)
        elif command == "look":
            describe_current_room(game_state)
        elif command == "help":
            print("Доступные команды: look, inventory, help, quit")
        else:
            print("Неизвестная команда. Введите 'help' для списка команд.")


if __name__ == "__main__":
    main()
