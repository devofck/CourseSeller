from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton, ReplyKeyboardMarkup


def give_offer_btn():
    get = InlineKeyboardButton(
        '💻 Получить',
        callback_data='give_offer'
    )
    return InlineKeyboardMarkup().add(get)


def buy_offer():
    buy = InlineKeyboardButton(
        'Приобрести подписку',
        callback_data='buy_offer'
    )
    get_demo = InlineKeyboardButton(
        'Получить Демо',
        callback_data='get_demo'
    )
    return InlineKeyboardMarkup().add(buy).add(get_demo)


def payed():
    pay = InlineKeyboardButton('✅ Оплатил', callback_data='payed')
    return InlineKeyboardMarkup().add(pay)


def btn_channel_link():
    link = InlineKeyboardButton(
        "Перейти на канал",
        url='https://t.me/+Zj0OK0iHSSYzYmRi'
    )
    return InlineKeyboardMarkup().add(link)


def request_sub():
    link = InlineKeyboardButton(
        "Подать заявку",
        url='https://t.me/+Zj0OK0iHSSYzYmRi'
    )
    return InlineKeyboardMarkup().add(link)


def manager():
    link = InlineKeyboardButton('Перейти к менеджеру', url='https://t.me/teach_media')
    return InlineKeyboardMarkup().add(link)


def buy_after_demo():
    buy = InlineKeyboardButton(
        'Приобрести подписку',
        callback_data='buy_offer'
    )
    return InlineKeyboardMarkup().add(buy)


def admin_panel():
    stats = KeyboardButton("📊 Статистика")
    give_accept = KeyboardButton('💎 Выдать доступ')
    return ReplyKeyboardMarkup(resize_keyboard=True).add(stats).add(give_accept)
