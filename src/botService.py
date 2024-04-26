from telebot import TeleBot, apihelper, types
from dotenv import load_dotenv
from os import getenv
from predictorService import pricePredictor
from datasetService import getColumn, createDataset
from datetime import datetime
from i18n import getPhrase
import locale


load_dotenv()

bot = TeleBot(getenv('BOT_TOKEN'))
proxy = getenv('PROXY')

if (proxy):
    apihelper.proxy = {'https': proxy}

print ('~~~~~~~~~~+ Engine Started +~~~~~~~~~~')

#createDataset(getenv('DATASET_PATH'))
carNames = getColumn(0, getenv('DATASET_PATH'))

locale.setlocale(locale.LC_ALL, 'C')

@bot.message_handler(commands=['start'])
def carListMessage(message):
    try:
        inlineMarkup = types.InlineKeyboardMarkup(row_width=3)
        carBtns = []

        for name in carNames:
            carBtns.append(types.InlineKeyboardButton(name, callback_data=name, switch_inline_query_current_chat="command"))

        inlineMarkup.add(*carBtns)
        bot.send_message(text="ماشین مورد نظر را انتخاب کنید:", chat_id=message.from_user.id,reply_markup=inlineMarkup)
    except NameError:
        print(NameError)


def carNameValidator(data):
        if(data.data in carNames):
            return True
        

def carDateValidator(message: types.Message):
        try:
            return bool(datetime.strptime(message.text, "%Y"))
        except:
            bot.reply_to(text='/start', message=message)
            return False


@bot.callback_query_handler(func= carNameValidator)
def callBackHandler(data: types.CallbackQuery):
        chatId = data.from_user.id
        bot.set_state(chat_id=chatId, user_id=chatId, state=data.data)
        
        bot.reply_to(message=data.message, text="سال ساخت ماشین را وارد کنید:")


@bot.message_handler(func=carDateValidator)
def predict(message):
    try:
        chatId = message.from_user.id
        carName = bot.get_state(chat_id=chatId , user_id=chatId)

        if(not carName):
            return bot.send_message(text="لطفا اول ماشین مورد نظر را انتخاب کنید.",chat_id=chatId)

        releaseDate= int(message.text)
        predicted_price = '${:,.2f}'.format(pricePredictor(carName, releaseDate))

        bot.reply_to(text=predicted_price, message=message)
    except:
        print('ERROR')



bot.polling()       