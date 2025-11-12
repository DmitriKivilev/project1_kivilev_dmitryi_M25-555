# Функции для действий игрока
# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS


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


def move_player(game_state, direction):
    """Перемещает игрока в указанном направлении"""
    from labyrinth_game.utils import random_event
    
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if direction in room_data['exits']:
        new_room = room_data['exits'][direction]
        
        # Проверка на treasure_room
        if (new_room == 'treasure_room' and 
                'rusty_key' not in game_state['player_inventory']):
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        
        if (new_room == 'treasure_room' and 
                'rusty_key' in game_state['player_inventory']):
            print("Вы используете найденный ключ, чтобы "
                  "открыть путь в комнату сокровищ.")
        
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        print(f"Вы пошли {direction}...")
        
        # Вызываем случайное событие после перемещения
        random_event(game_state)
        return True
    else:
        print("Нельзя пойти в этом направлении.")
        return False

def take_item(game_state, item_name):
    """Берет предмет из комнаты и добавляет в инвентарь"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    # Проверка на сундук
    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return False
    
    if item_name in room_data['items']:
        room_data['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
        return True
    else:
        print("Такого предмета здесь нет.")
        return False

def use_item(game_state, item_name):
    """Использует предмет из инвентаря"""
    inventory = game_state['player_inventory']
    
    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return False
    
    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее!")
    elif item_name == 'sword':
        print("Вы почувствовали уверенность, держа меч в руках.")
    elif item_name == 'bronze_box':
        if 'rusty_key' not in inventory:
            inventory.append('rusty_key')
            print("Вы открыли бронзовую шкатулку и нашли внутри rusty_key!")
        else:
            print("Шкатулка пуста.")
    else:
        print(f"Вы не знаете, как использовать {item_name}.")
    return True
