from app import dp, bot
from app.settings import PAY_TOKEN
from app.database.db_communicate import *


# Callback handlers

from .callback_handler import *

###
from ..database.add_skin_and_box import add_list_of_skins


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not is_user_in_bd_by(message.chat.id):
        add_user(message.chat.id, message.chat.username)
        add_money_to_user_by(message.chat.id, 24)
    await bot.send_message(message.chat.id, 'Привіт😃\nОбери дії з меню', reply_markup=inline_keyboard.menu_keyboard)


@dp.message_handler(commands=['add_trade_url'])
async def trade_url(message: types.Message):
    change_user_last_message(message.chat.id, 'trade_url')
    await bot.send_message(message.chat.id, 'Напиши сюди свою Trade силку')


@dp.message_handler(commands=['order_box'])
async def order_box(message: types.Message):
    await bot.send_message(message.chat.id, 'Обери тип кейсу, який хочеш відкрити!',
                           reply_markup=inline_keyboard.all_boxes)


@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    await bot.send_message(message.chat.id, f'💵 Ваш баланс {show_balance_by_(message.chat.id)} грн',
                           reply_markup=inline_keyboard.paying_keyboard)


@dp.message_handler(commands=['skins'])
async def balance(message: types.Message):
    skins_keyboard = InlineKeyboardMarkup(row_width=1)
    for skin_name in show_all_user_skins_by(message.chat.id):
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        skin_btn = InlineKeyboardButton(f'✅{skin.name}', callback_data=f'{skin.id}')
        skins_keyboard.add(skin_btn)
    inventory_back_btn = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')
    inventory_sell_all_btn = InlineKeyboardButton('💰 Продати всі скіни', callback_data='sell_all')
    skins_keyboard.add(inventory_sell_all_btn, inventory_back_btn)
    await bot.send_message(message.chat.id, f'📭 Ваш інвертар',
                           reply_markup=skins_keyboard)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.chat.id == ADMIN_ID:
        await bot.send_message(message.chat.id, 'Добрий день\nОсь панель для Адміна',
                               reply_markup=inline_keyboard.admin_menu_keyboard)


@dp.message_handler(commands=['add_easy_money'])
async def balance(message: types.Message):
    add_money_to_user_by(message.chat.id, 12)


@dp.message_handler(content_types=types.ContentTypes.SUCCESSFUL_PAYMENT)
async def successful_pay(message: types.Message):
    if type(show_user_last_message_by(message.chat.id)) == int():
        add_money_to_user_by(message.chat.id, show_user_last_message_by(message.chat.id))
        await message.answer(f'Successful: {message.successful_payment.order_info}')
        await bot.send_message(message.chat.id, 'Обери дії з меню',
                               reply_markup=inline_keyboard.menu_keyboard)
    await message.answer('Щось пішло не так(')


@dp.message_handler()
async def message_handler(message: types.Message):
    if show_user_last_message_by(message.chat.id) == 'paying':
        change_user_last_message(message.chat.id, '')
        try:
            print(int(message.text))
        except ValueError:
            await bot.send_message(message.chat.id, 'Ви щось ввели неправильно\nПовторіть спробу')
            change_user_last_message(message.chat.id, 'paying')
            return None
        sum_ = int(message.text)
        if sum_ >= 40:
            await bot.send_invoice(message.chat.id,
                                   'Поповнення рахунку',
                                   'Поповнення рахунку для збільшення балансу',
                                   'invoice',
                                   PAY_TOKEN,
                                   'UAH',
                                   [types.LabeledPrice('Поповнення рахунку', sum_ * 100)]
                                   )
            change_user_last_message(message.chat.id, sum_)
            return None
        else:
            await bot.send_message(message.chat.id, "Можна поповнити мінімум на 40 грн!\nПовторіть спробу")
            change_user_last_message(message.chat.id, 'paying')
            return None
    elif show_user_last_message_by(message.chat.id) == 'trade_url':
        res = create_steam_href_by(message.chat.id, message.text)
        await bot.send_message(message.chat.id, res)
        change_user_last_message(message.chat.id, '')
    elif show_user_last_message_by(message.chat.id) == 'add_box':
        box_data = message.text.split('@')
        try:
            add_list_of_skins(box_data[3], box_data[0], box_data[1], box_data[2])
            await bot.send_message(message.chat.id, f'✅ Кейс додано! ✅\nПеревірте наявність \nкейсу в списку',
                                   reply_markup=inline_keyboard.admin_menu_keyboard)
        except Exception as err:
            await bot.send_message(message.chat.id, f'❌ Щось сталося не так, або ви ввели дані неправильно!\n{err}',
                                   reply_markup=inline_keyboard.admin_menu_keyboard)
    change_user_last_message(message.chat.id, '')

# All handlers of this app
