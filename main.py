import telebot
from pyexpat.errors import messages
from telebot import types

bot = telebot.TeleBot('7829023044:AAH0bw1sF5DV2Ha3LCDqfDRhpHY5wq025vo')

@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Поиск запчастей', callback_data='search')
    btn2 = types.InlineKeyboardButton('Доставка', callback_data='delievery')
    markup.row(btn1, btn2)
    btn3 = types.InlineKeyboardButton('Список магазинов партнёров', callback_data='list')
    btn4 = types.InlineKeyboardButton('Вызвать менеджера', callback_data='call_manager')
    markup.row(btn3, btn4)
    btn_send = types.InlineKeyboardButton('Барахолка', callback_data='send')
    markup.row(btn_send)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! Выберите пункт меню, который Вас интересует', reply_markup=markup)

@bot.message_handler()
def search_part(message):
    bot.send_message(message.chat.id, f'Введите название запчасти')
    global vin
    vin = message.text
    bot.register_next_step_handler(message, search_name)

def search_name(message):
    bot.send_message(message.chat.id, f'Введите свои контакты (Имя и номер телефона)')
    global part_name
    part_name = message.text
    bot.register_next_step_handler(message, search_summary)

def search_summary(message):
    global contacts
    contacts = message.text
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Всё верно', callback_data='yes')
    btn_no = types.InlineKeyboardButton('Вернуться в основное меню', callback_data='no')
    markup.row(btn_yes, btn_no)
    bot.send_message(message.chat.id, f'Проверьте правильность введённых данных: \n\nVIN-код или номер запчасти: {vin}\nНазвание запчасти: {part_name}\nИмя и номер телефона: {contacts}\n', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'search':
        markup = types.InlineKeyboardMarkup()
        btn5 = types.InlineKeyboardButton('Поиск по vin-коду', callback_data='search_vin')
        btn6 = types.InlineKeyboardButton('Поиск по номеру запчасти', callback_data='search_number')
        markup.row(btn5, btn6)
        bot.send_message(callback.message.chat.id, f'Выберите каким образом искать запчасть', reply_markup=markup)
    elif callback.data == 'list':
        bot.send_message(callback.message.chat.id, f'Список магазинов партнёров будет опубликован в ближайшее время!')
        main(callback.message)
    elif callback.data == 'delievery':
        bot.send_message(callback.message.chat.id, f'Доставку запчастей планируем запустить в ближайшее время, будем держать Вас в курсе событий!')
        main(callback.message)
    elif callback.data == 'send':
        markup = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton('Перейти в барахолку', url='https://t.me/+JCVGb1ZSE6Q1OTcy')
        markup.add(url_btn)
        bot.send_message(callback.message.chat.id, 'Перейти в барахолку', reply_markup=markup)
    elif callback.data == 'search_vin':
        bot.send_message(callback.message.chat.id, f'Введите vin-код')
        bot.register_next_step_handler(callback.message, search_part)
    elif callback.data == 'search_number':
        bot.send_message(callback.message.chat.id, f'Введите введите номер запчасти')
        bot.register_next_step_handler(callback.message, search_part)
    elif callback.data == 'yes':
        bot.send_message(callback.message.chat.id, f'Благодарим Вас за запрос, свяжемся с Вами в ближайшее время!')
        bot.forward_message(7626049922, callback.message.chat.id, callback.message.message_id)
    elif callback.data == 'no':
        main(callback.message)
    elif callback.data == 'call_manager':
        markup = types.InlineKeyboardMarkup()
        url_btn = types.InlineKeyboardButton('Позвать менеджера', url='https://t.me/avtorynok_streleckiy')
        markup.add(url_btn)
        bot.send_message(callback.message.chat.id, 'Позвать менеджера', reply_markup=markup)



bot.polling(none_stop=True)
