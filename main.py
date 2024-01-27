from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup
from asd import read_json, write_json

bot = TeleBot("6367969204:AAH-kktm0eVKfQEQmhwX5h8nSlvkxJzk_pk")

locations = read_json("location.json")
players = read_json()


@bot.message_handler(commands=['start'])
def start(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/помощь', '/играть'])
    bot.send_message(message.from_user.id, "Приветствую дорогой игрок!Желаю удачи пройти игру с комфортом",reply_markup=menu_keyboard)


@bot.message_handler(commands=['помощь', 'help'])
def start(message):
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*['/играть'])
    bot.send_message(message.from_user.id, "Скорее нажми на кнопку, чтобы пройти эту игру!", reply_markup=menu_keyboard)


@bot.message_handler(commands=['играть', 'play'])
def play(message):
    p_id = str(message.from_user.id)
    if new_player(p_id): return
    send_info(p_id)


@bot.message_handler(func=lambda message: True)
def engine(message):
    p_id = str(message.from_user.id)
    if new_player(p_id): return
    try:
        p_new_location = locations[players[p_id]['location']]['actions'][message.text]
        players[p_id]['location'] = p_new_location
        exec(locations[players[p_id]['location']].get("def", ""))
        write_json(players)
    except:
        bot.send_message(p_id, "Ошибка выбора деуствия")

    send_info(p_id)


def new_player(p_id):
    if p_id not in players:
        players[p_id] = {"location": "forest", "death": 0, 'arsenal': []}
        write_json(players)
        send_info(p_id)
        return True

    return False


def send_info(p_id):
    text = locations[players[p_id]['location']]['description']
    img = open(locations[players[p_id]['location']]['image'], 'rb')
    actions = list(locations[players[p_id]['location']]['actions'].keys())
    menu_keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    menu_keyboard.add(*actions)
    bot.send_photo(p_id, photo=img, caption=text, reply_markup=menu_keyboard)


def check_key(p_id):
    if "key" in players[p_id]['arsenal']:
        players[p_id]['location'] = "lawn"
    else:
        players[p_id]['location'] = "key"


def equip_key(p_id):
    players[p_id]['arsenal'].append("key")


def count_death(p_id):
    players[p_id]['death'] += 1


bot.polling()
