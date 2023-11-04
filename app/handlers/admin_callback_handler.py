from aiogram import types

from app import dp, bot
from app.database.db_communicate import get_skin_list, change_user_last_message, get_box_list
from app.keyboard import inline_keyboard


@dp.callback_query_handler(lambda cb: cb.data == 'show_all_skins')
async def cb_start(callback_query: types.CallbackQuery):
    """This function is showing to admin all skins in bd"""

    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    all_skins_str = 'ID  |  NAME'
    skin_list = get_skin_list()
    for skin in skin_list:
        all_skins_str += f'\n{skin.id}  |  {skin.name}'
    await bot.send_message(callback_query.message.chat.id, f'Ось всі скіни які є:\n{all_skins_str}',
                           reply_markup=inline_keyboard.admin_back_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'show_all_box')
async def cb_start(callback_query: types.CallbackQuery):
    """This function is showing to admin all skins in bd"""

    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    all_boxes_str = 'ID  |  NAME'
    box_list = get_box_list()
    for box in box_list:
        all_boxes_str += f'\n{box.id}  |  {box.name}'
    await bot.send_message(callback_query.message.chat.id, f'Ось всі кейси які є:\n{all_boxes_str}',
                           reply_markup=inline_keyboard.admin_back_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'add_box')
async def cb_start(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    change_user_last_message(callback_query.message.chat.id, 'add_box')

    await bot.send_message(callback_query.message.chat.id, '''📦 Створення кейсу! 📦\n\nНапишіть наступним\nповідомленням через @\n- назву кейсу\n- ціну кейсу(числом)\n- тип кейсу(my, farm, collection)\n- скіни кейсу\n\nP.S приклад як повинні виглядати скіни кейсу:\n- <ім'я скіну>+++<силка стім>+++<ціна(числом)>''',
                           reply_markup=inline_keyboard.admin_back_keyboard)
