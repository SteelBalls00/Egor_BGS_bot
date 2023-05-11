import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Я нигерийский принц и скоро получу огромное наследство, " \
           "но для этого мне нужна финансовая помощь, взамен я вас щедро вознагражу! " \
           "Поможет любая сумма. Для удобства расчетов здесь есть конвертер валют. " \
           "\n\n" \
           "Поддерживаемые валюты - /values" \
           "\n\n" \
           "Инструкция - /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = "Вводите через пробел: " \
           "имя валюты, цену которой хотите узнать, " \
           "имя валюты в которой нужно узнать цену первой валюты, " \
           "количество конвертируемой валюты."\
           "\n\n" \
           "Поддерживаемые валюты - /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for i in exchanges:
        text += f'\n{i}'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    print(values)
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
