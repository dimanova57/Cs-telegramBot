from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app import dp, bot
from app.database.database import session, Skin
from app.database.db_communicate import show_all_user_skins_by, is_user_in_bd_by, add_user, add_money_to_user_by, \
    show_balance_by_, change_user_last_message
from app.keyboard import inline_keyboard


@dp.callback_query_handler(lambda cb: cb.data == 'start' or cb.data == 'type_of_box_back')
async def cb_start(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    if not is_user_in_bd_by(callback_query.message.chat.id):
        add_user(callback_query.message.chat.id, callback_query.message.chat.username)
        add_money_to_user_by(callback_query.message.chat.id, 24)
    await bot.send_message(callback_query.message.chat.id, 'Привіт😃\nОбери дії з меню',
                           reply_markup=inline_keyboard.menu_keyboard)


# type_of_box_back

@dp.callback_query_handler(lambda cb: cb.data == 'order_box' or cb.data == 'back_to_type_of_box')
async def cb_order_box(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Обери тип кейсу, який хочеш відкрити!',
                           reply_markup=inline_keyboard.all_boxes)


@dp.callback_query_handler(lambda cb: cb.data == 'back_to_type_of_box2')
async def cb_order_box(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id-1)
    await bot.send_message(callback_query.message.chat.id, 'Обери тип кейсу, який хочеш відкрити!',
                           reply_markup=inline_keyboard.all_boxes)


@dp.callback_query_handler(lambda cb: cb.data == 'balance')
async def cb_balance(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id,
                           f'💵 Ваш баланс {show_balance_by_(callback_query.message.chat.id)} грн',
                           reply_markup=inline_keyboard.paying_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'skins')
async def cb_skins(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    skins_keyboard = InlineKeyboardMarkup(row_width=1)
    for skin_name in show_all_user_skins_by(callback_query.message.chat.id):
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        skin_btn = InlineKeyboardButton(f'✅{skin.name}', callback_data=f'{skin.id}')
        skins_keyboard.add(skin_btn)
    inventory_back_btn = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')
    inventory_sell_all_btn = InlineKeyboardButton('💰 Продати всі скіни', callback_data='sell_all')
    skins_keyboard.add(inventory_sell_all_btn, inventory_back_btn)
    await bot.send_message(callback_query.message.chat.id, f'📭 Ваш інвентар',
                           reply_markup=skins_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'trade_url')
async def cb_balance(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    change_user_last_message(callback_query.message.chat.id, 'trade_url')
    await bot.send_message(callback_query.message.chat.id, 'Напиши сюди свою Trade силку')
