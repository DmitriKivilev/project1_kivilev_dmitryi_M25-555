#!/usr/bin/env python3

from labyrinth_game.constants import ROOMS

# Состояние игры
game_state = {
    'player_inventory': [],  # Инвентарь игрока
    'current_room': 'entrance',  # Текущая комната
    'game_over': False,  # Флаг окончания игры
    'steps_taken': 0  # Количество шагов
}

def main():
    print("Первая попытка запустить проект!")
    print(f"Текущая комната: {game_state['current_room']}")
    print(f"Всего комнат в лабиринте: {len(ROOMS)}")

if __name__ == "__main__":
    main()
