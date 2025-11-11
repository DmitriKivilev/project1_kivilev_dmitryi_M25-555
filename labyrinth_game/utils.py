# labyrinth_game/utils.py

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """Выводит описание текущей комнаты"""
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]
    
    # Название комнаты
    print(f"\n== {current_room_name.upper()} ==")
    
    # Описание комнаты
    print(room['description'])
    
    # Предметы в комнате
    if room['items']:
        print("Заметные предметы:", ", ".join(room['items']))
    
    # Выходы из комнаты
    if room['exits']:
        exits = [
            f"{direction} ({room_name})" 
            for direction, room_name in room['exits'].items()
        ]
        print("Выходы:", ", ".join(exits))
    
    # Загадка
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
