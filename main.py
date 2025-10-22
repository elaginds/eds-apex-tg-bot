import telebot
import os
import json
from datetime import datetime, time, timedelta

TOKEN = os.getenv('EDS_APEX_TG_BOT_TOKEN')
# MODES_LIST = ['Control', 'Gun Run', 'Deathmatch']
# MODES_LIST = [
#     {
#     'mode': 'Control',
#     'name': 'Caustic Treatment'
# }, {
#     'mode': 'Gun Run',
#     'name': 'Monument'
# }, {
#     'mode': 'Deathmatch',
#     'name': 'Zeus Station'
# }, {
#     'mode': 'Control',
#     'name': 'Barometer'
# }, {
#     'mode': 'Gun Run',
#     'name': 'Estates'
# }, {
#     'mode': 'Deathmatch',
#     'name': 'Estates'
# }, {
#     'mode': 'Control',
#     'name': 'Lava Siphon'
# }, {
#     'mode': 'Gun Run',
#     'name': 'Skull Town'
# }, {
#     'mode': 'Deathmatch',
#     'name': 'Fragment East'
# }, {
#     'mode': 'Control',
#     'name': 'Hammond Labs'
# }, {
#     'mode': 'Gun Run',
#     'name': 'Wattsons Pylon'
# }, {
#     'mode': 'Deathmatch',
#     'name': 'Skull Town'
# }]
NEXT_MODES_COUNT = 3

with open('nodes-list.json', 'r') as file:
    MODES_LIST = json.load(file)
    print('MODES_LIST', MODES_LIST)

print('TOKEN', TOKEN)
if not TOKEN:
    raise RuntimeError('EDS_APEX_TG_BOT_TOKEN не задан')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    print('START')
    bot.send_message(message.chat.id, 'HELLO!')

@bot.message_handler(commands=['now', 'mix'])
def main(message):
    print('NOW')
    msg = getMessage()
    bot.send_message(message.chat.id, msg)

# Создаем ответ
def getMessage():
    changes = getChanges()
    print('changes', changes)
    mode_index = getNowModeIndex(changes)
    print('NOW MODE', mode_index, MODES_LIST[mode_index])
    next_modes_list = getNextModes(mode_index, changes)
    print('NEXT_MODES', next_modes_list)
    answer = createAnswer(mode_index, next_modes_list)
    print('answer', answer)

    return answer

# Сколько прошло 15-ти минутных смен режимов с 0:00 часов сегодня
def getChanges():
    # Get the current datetime
    now = datetime.now()

    # Create a datetime object for the beginning of today (midnight)
    midnight = datetime.combine(now.date(), time.min)

    # Calculate the difference between now and midnight
    time_difference = now - midnight

    # Get the total seconds from the timedelta object
    seconds_of_today = time_difference.total_seconds()

    return int(seconds_of_today // 900)

# Получаем номер текущего режима из списка MODES_LIST
def getNowModeIndex(changes):
    return int(changes % len(MODES_LIST))

# Получаем список следующих режимов после текущего
def getNextModes(mode_index, changes):
    extended_list = MODES_LIST + MODES_LIST
    # next_list = extended_list[mode_index + 1:mode_index + 1 + NEXT_MODES_COUNT]

    result = list()
    start_time = getStartTime(changes)

    for n in range(0, NEXT_MODES_COUNT):
        result.append(f'{getTime(start_time, n)} - {extended_list[mode_index + 1 + n]["mode"]} - {extended_list[mode_index + 1 + n]["name"]}')

    return result

# Получаем время начала следующих режимов
def getTime(startTime, step):
    return (startTime + timedelta(minutes=step * 15)).strftime("%H:%M")

# Получаем время начала следующего режима
def getStartTime(changes):
    now = datetime.now()
    midnight = datetime.combine(now.date(), time.min)
    time_delta = timedelta(minutes=changes * 15 + 15)
    return midnight + time_delta

# Создаем строку ответа
def createAnswer(mode_index, next_modes_list):
    arr = [f'Now - {MODES_LIST[mode_index]["mode"]} - {MODES_LIST[mode_index]["name"]}'] + next_modes_list
    result_str = ''

    for item in arr:
        result_str += f'{item}\n'

    return result_str

# getMessage()
bot.polling(none_stop=True)