from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app import dp, bot
from app.settings import ADMIN_ID
from app.database.database import session, Skin
from app.database.db_communicate import show_all_user_skins_by, is_user_in_bd_by, add_user, add_money_to_user_by
from app.keyboard import inline_keyboard


@dp.callback_query_handler(lambda cb: cb.data == 'back')
async def back_after_skin_info(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    skins_keyboard = InlineKeyboardMarkup(row_width=1)
    for skin_name in show_all_user_skins_by(callback_query.message.chat.id):
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        skin_btn = InlineKeyboardButton(f'✅{skin.name}', callback_data=f'{skin.id}')
        skins_keyboard.add(skin_btn)
    inventory_back_btn = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')
    inventory_sell_all_btn = InlineKeyboardButton('💰 Продати всі скіни', callback_data='sell_all')
    skins_keyboard.add(inventory_sell_all_btn, inventory_back_btn)
    await bot.send_message(callback_query.message.chat.id, '🗄 Ваш інвертар',
                           reply_markup=skins_keyboard)


# back_to_type_of_box

@dp.callback_query_handler(lambda cb: cb.data == 'type_of_box_back')
async def type_of_box_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    if not is_user_in_bd_by(callback_query.message.chat.id):
        add_user(callback_query.message.chat.id, callback_query.message.chat.username)
        add_money_to_user_by(callback_query.message.chat.id, 24)
    await bot.send_message(callback_query.message.chat.id, 'Привіт😃\nОбери дії з меню',
                           reply_markup=inline_keyboard.menu_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'admin_back')
async def type_of_box_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Обери дію з меню',
                           reply_markup=inline_keyboard.admin_menu_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'delete_msg')
async def type_of_box_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=ADMIN_ID, message_id=callback_query.message.message_id)



