import telebot
from telebot import apihelper

access_token = '804157838:AAFYh6pgcPNpnzmH10fQwJ0EfOzHo1L_6fk'
bot = telebot.TeleBot(access_token)
apihelper.proxy = {'https': 'https://51.158.68.68:8811'}

@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == '__main__':
    bot.polling(none_stop=True)