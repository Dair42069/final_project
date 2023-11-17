import requests
import json
import telebot
from currency_converter import CurrencyConverter
from telebot import types

bot = telebot.TeleBot('6648781717:AAH6UpGGmAFAlNJ46iMkhqfpIKlm__69Zjw', parse_mode=None)
wet = '004b7245bfbdcd07440025cd18fb0078'
currency = CurrencyConverter()
amount = 0

@bot.message_handler(commands=['dog'])
def send_dog(message):
    response = requests.get("https://random.dog/woof.json")
    data = json.loads(response.text)

    bot.send_message(message.chat.id, data["url"])

@bot.message_handler(commands=['convert'])
def convert(message):
    bot.send_message(message.chat.id, 'Input sum of money')
    bot.register_next_step_handler(message, summa)

def summa(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Invalid format, enter the number')
        bot.register_next_step_handler(message, summa)
        return
    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur')
        btn2 = types.InlineKeyboardButton('GBP/JPY', callback_data='gbp/jpy')
        btn3 = types.InlineKeyboardButton('Another amount', callback_data='else')
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id, 'Choose a currency pair', reply_markup=markup)
    else:
         bot.send_message(message.chat.id, 'Number must be more than 0. Please write correct number')
         bot.register_next_step_handler(message, summa)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'There is: {round(res, 2)}.')
    else:
        bot.send_message(call.message.chat.id, 'Enter some numbers with /')
        bot.register_next_step_handler(call.message, my_currency)

def my_currency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'There is: {round(res, 2)}.')
        bot.register_next_step_handler(message, summa)
    except Exception:
        bot.send_message(message.chat.id, 'There is something wrong. Write a number again')
        bot.register_next_step_handler(message, my_currency)




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hi, how can I help you today?')

@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, 'Write name of city')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={wet}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        bot.reply_to(message, f'Now weather is: {data["main"]["temp"]}')
    else:
        bot.reply_to(message, 'Incorrect name of city')
        return



bot.infinity_polling()