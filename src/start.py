import telebot
from .functions import get_list, get_d, get_prediction, pred_message
from .Mode import Mode

bot = telebot.TeleBot("1499557789:AAFYOxnEFgYadWCz6fJOfuUJffRrzbt82Gc")
moder = Mode()
d = get_d()


@bot.message_handler(commands=['start'])
def start_cmd(message):
    name = message.chat.first_name
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.KeyboardButton(text='Предсказать')
    btn2 = telebot.types.KeyboardButton(text='Тикеры компаний')
    keybd.add(btn1)
    keybd.add(btn2)
    text = 'Привет, {}! \n \n'.format(name)
    text += "Я - предсказатель поведения акций на бирже💵\n\n" \
            "❗️ Перейди в режим \'Предсказать\'\n" \
            "❗️ Введи имя или тикер компании\n\n" \
            "А я скажу: стоит ли их БЕЗДУМНО СКУПАТЬ📈 или БЕССОВЕСТНО ПРОДАВАТЬ📉"

    bot.send_message(message.chat.id, text, reply_markup=keybd)


# Обработчик 0-положения
@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.INITIAL_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text

    if text == 'Предсказать':
        message = "Введи имя или тикер компании:"
        moder.mode = Mode.States.RECORDING_STATE
    elif text == 'Тикеры компаний':
        message = get_list()
    else:
        message = 'Для начала выберите режим, мой друг!'
    bot.send_message(chat_id, message)


@bot.message_handler(content_types=['text'], func=lambda message: moder.mode == Mode.States.RECORDING_STATE)
def send_text(message):
    chat_id = message.chat.id
    text = message.text
    if text == 'Предсказать':
        message = "Введи имя или тикер компании:"
        moder.mode = Mode.States.RECORDING_STATE
    elif text == 'Тикеры компаний':
        message = get_list()
        moder.mode = Mode.States.INITIAL_STATE
    else:
        if text in d:
            message = pred_message(get_prediction(d[text]))
        elif text in d.values():
            message = pred_message(get_prediction(text))
        else:
            message = "В нашей базе данных нет информации о таком имени или тикере!\n" \
                      "Попробуйте ввести еще разок"
    bot.send_message(chat_id, message)


bot.polling()
