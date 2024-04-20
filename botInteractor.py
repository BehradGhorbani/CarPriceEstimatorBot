from telebot import TeleBot, apihelper, types
from dotenv import load_dotenv
from os import getenv
from estimator import pricePredictor

load_dotenv()

bot = TeleBot(getenv('BOT_TOKEN'))

apihelper.proxy = {'https':'http://127.0.0.1:1080'}


@bot.message_handler(commands=['start'])
def welcome(m):
    keyboardMarkup = types.ReplyKeyboardMarkup(row_width=2)
    aboutMeBtn = types.KeyboardButton(text="/predict")

    keyboardMarkup.add(aboutMeBtn)

    bot.send_message(text='Welcome.', chat_id=406045600,reply_markup=keyboardMarkup)

@bot.message_handler(commands=['predict'])
def predict(message):
    splitted_msg = message.text.split(' ')

    if ((len(splitted_msg) > 3 or len(splitted_msg) <= 0)):
        bot.send_message(text='Send Car Data in this format: /predict (car) (date).', chat_id=message.from_user.id)
        return

    [command, car , date] = splitted_msg

    predicted_price = pricePredictor(car, date)

    bot.send_message(text=f'price is {predicted_price}', chat_id=message.from_user.id)



bot.polling()       