from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input


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


def solve_puzzle(game_state):
    """Решает загадку в текущей комнате"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if not room_data['puzzle']:
        print("Загадок здесь нет.")
        return
    
    question, correct_answer = room_data['puzzle']
    print(f"Загадка: {question}")
    
    user_answer = get_input("Ваш ответ: ")
    
    if user_answer == correct_answer:
        print("Правильно! Загадка решена.")
        room_data['puzzle'] = None  # Убираем загадку
        # Добавляем награду
        if current_room == 'treasure_room':
            print("Вы получаете treasure_key!")
            game_state['player_inventory'].append('treasure_key')
        else:
            print("Вы чувствуете, что стали ближе к разгадке тайны.")
    else:
        print("Неверно. Попробуйте снова.")


def attempt_open_treasure(game_state):
    """Пытается открыть сундук с сокровищами"""
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    
    if 'treasure_chest' not in room_data['items']:
        print("Здесь нет сундука с сокровищами.")
        return False
    
    # Проверка ключа
    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_data['items'].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return True
    
    # Предложение ввести код
    print("Сундук заперт. У вас нет ключа, но можно попробовать ввести код.")
    choice = get_input("Ввести код? (да/нет): ")
    
    if choice == 'да':
        if room_data['puzzle']:
            _, correct_code = room_data['puzzle']
            user_code = get_input("Введите код: ")
            
            if user_code == correct_code:
                print("Код верный! Сундук открывается!")
                room_data['items'].remove('treasure_chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
                return True
            else:
                print("Неверный код. Сундук остается запертым.")
                return False
        else:
            print("Здесь нет загадки для взлома сундука.")
            return False
    else:
        print("Вы отступаете от сундука.")
        return False
