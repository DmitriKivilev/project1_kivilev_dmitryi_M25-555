import math

from labyrinth_game.constants import (
    EVENT_PROBABILITY,
    EVENT_TYPES_COUNT,
    ROOMS,
)
from labyrinth_game.player_actions import get_input


def pseudo_random(seed, modulo):
    """Генерирует псевдослучайное число в диапазоне [0, modulo)"""
    x = math.sin(seed * 12.9898) * 43758.5453
    fractional_part = x - math.floor(x)
    return math.floor(fractional_part * modulo)

def trigger_trap(game_state):
    """Активирует ловушку с негативными последствиями"""
    print("Ловушка активирована! Пол стал дрожать...")
    
    # Увеличиваем счетчик ловушек
    game_state['traps_triggered'] += 1
    
    inventory = game_state['player_inventory']
    
    if inventory:
        item_index = pseudo_random(game_state['traps_triggered'], len(inventory))
        lost_item = inventory.pop(item_index)
        print(f"Из вашего инвентаря выпал и потерялся: {lost_item}")
    else:
        # Используем traps_triggered для случайности
        damage_chance = pseudo_random(game_state['traps_triggered'], 10)
        if damage_chance < 1:  # 10% шанс
            print("Ловушка нанесла критический урон! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от ловушки!")

def random_event(game_state):
    """Случайные события при перемещении"""
    # Проверяем, произойдет ли событие (10% вероятность)
    event_chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    if event_chance != 0:
        return
    
    # Выбираем тип события
    event_type = pseudo_random(game_state['steps_taken'] + 1, EVENT_TYPES_COUNT)
    current_room = game_state['current_room']
    room_data = ROOMS[current_room]
    inventory = game_state['player_inventory']
    
    match event_type:
        case 0:
            # Находка
            print("Вы заметили что-то блестящее на полу...")
            if 'coin' not in room_data['items']:
                room_data['items'].append('coin')
                print("Вы нашли монетку! Она добавлена в комнату.")
            else:
                print("Это была всего лишь пыль.")
        
        case 1:
            # Испуг
            print("Вы услышали подозрительный шорох в темноте...")
            if 'sword' in inventory:
                print("Благодаря мечу в руках, вы отпугнули существо!")
            else:
                print("Шорох быстро стих, но вы почувствовали беспокойство.")
        
        case 2:
            # Срабатывание ловушки
            if current_room == 'trap_room' and 'torch' not in inventory:
                print("Вы не заметили ловушку в темноте!")
                trigger_trap(game_state)
            else:
                print("Показалось, что что-то щелкнуло под ногами, "
                      "но ничего не произошло.")

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
    
    # Проверка альтернативных вариантов ответа
    correct_answers = [correct_answer]
    if correct_answer == '10':
        correct_answers.extend(['десять', '10'])
    
    if user_answer in correct_answers:
        print("Правильно! Загадка решена.")
        room_data['puzzle'] = None  # Убираем загадку
        
        # Награда в зависимости от комнаты
        if current_room == 'treasure_room':
            print("Вы получаете treasure_key!")
            game_state['player_inventory'].append('treasure_key')
        elif current_room == 'hall':
            print("Вы получаете доступ к новым возможностям!")
        elif current_room == 'trap_room':
            print("Ловушка деактивирована!")
        else:
            print("Вы чувствуете, что стали ближе к разгадке тайны.")
    else:
        print("Неверно. Попробуйте снова.")
        # В trap_room неверный ответ активирует ловушку
        if current_room == 'trap_room':
            print("Неверный ответ активировал ловушку!")
            trigger_trap(game_state)

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

def show_help(commands):
    """Показывает список доступных команд"""
    print("Доступные команды:")
    for command, description in commands.items():
        # Форматирование с выравниванием
        print(f"  {command:<16} - {description}")
