import bs4
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


API = ''
URL = 'https://api.openweathermap.org/data/2.5/weather'

def get_weater(lat, lon):
    print(lat)
    print(lon)
    params = {'lat' : lat,
              'lon' :  lon,
              'lang' : 'ru',
              'units' : 'metric',
              'appid' : API}
    respons = requests.get(url = URL, params = params).json()
    print(respons)
    city_name = respons['name']
    description = respons['weather'][0]['description']
    code = respons['weather'][0]['id']
    temp = respons['main']['temp']
    temp_feels_like = respons['main']['feels_like']
    hubidity = respons['main']['humidity']
    message = f'Погода в {city_name}\n'
    message += f'{description.capitalize()}.\n'
    message += f'Температура {temp}\n'    
    message += f'Ощущается как {temp_feels_like}\n'
    message += f'Влажность {hubidity}%.\n'
    return message

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location = True))
keyboard.add(KeyboardButton('О проекте'))


@bot.message_handler(commands = ['start'])
def send_message(message):
    text = 'Отправте местоположение, где хотите узнать погоду'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types = ['location'])
def sand_weather(message):
    lon = message.location.longitude
    lan = message.location.latitude
    result = get_weater(lan, lon)
    if result:
        bot.send_message(message.chat.id, result, reply_markup = keyboard)

@bot.message_handler(func = lambda s: 'О проекте' in s.text)
def send_welcome(message):
    text = 'Бот создан для получения погода по координатам \ncreated by Mr_appel_pie'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)



bot.infinity_polling()

