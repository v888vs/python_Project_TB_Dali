import telebot, wikipedia, requests, re
from telebot import types
from datetime import datetime
import api_key


bot = telebot.TeleBot(api_key.api_key_Dali)
wikipedia.set_lang('ru')

@bot.message_handler(commands=['start'])
def start(message):
    stiker = open('stickers/dali.webp', 'rb')
    bot.send_sticker(message.chat.id, stiker)
    user_full_name = message.from_user.full_name
    bot.send_message(message.chat.id, f'Привет, {user_full_name} ✌')
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item2 = types.KeyboardButton("Запрос курса криптовалюты")
    item3 = types.KeyboardButton("Запрос номера телефона")
    item4 = types.KeyboardButton("Как дела?")
    markup1.add(item2, item3, item4)
    bot.send_message(message.chat.id, 'Выбери команду или введите слово', reply_markup=markup1)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Запрос курса криптовалюты' \
            or message.text == 'Как дела?' \
            or message.text == 'Запрос номера телефона'\
            or message.text == 'Назад':
        bot.register_next_step_handler(message.text, send_text(message))
    else:
        bot.send_message(message.chat.id, getwiki(message.text))

def send_text(message):
    if message.chat.type == 'private':
        if message.text == 'Запрос курса криптовалюты':
            bot.send_message(message.chat.id, get_data())
        elif message.text == 'Запрос номера телефона':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            kn1 = types.KeyboardButton("Предоставить номер телефона", request_contact=True)
            kn2 = types.KeyboardButton("Назад")
            markup.add(kn1, kn2)
            bot.send_message(message.chat.id, 'Нажмите кнопку ниже', reply_markup=markup)
        elif message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item2 = types.KeyboardButton("Запрос курса криптовалюты")
            item3 = types.KeyboardButton("Запрос номера телефона")
            item4 = types.KeyboardButton("Как дела?")
            markup.add(item2, item3, item4)
            bot.send_message(message.chat.id, 'Выбери команду или введите слово', reply_markup=markup)
        elif message.text == 'Как дела?':
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Плохо", callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if (len(x.strip()) > 3):
                    wikitext2 = wikitext2 + x + '.'
                else:
                    break
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        return wikitext2
    except Exception as e:
        return 'Такой информации нет'

def get_data():
    req = requests.get('https://yobit.net/api/3/ticker/btc_usd')
    response = req.json()
    sell_price = response['btc_usd']['sell']
    return f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nСтоимость BTC: {sell_price}$"

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, '✌️')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Сочувствую!')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Как дела?',
                                  reply_markup=None)
    except Exception as e:
        print(repr(e))

bot.infinity_polling()