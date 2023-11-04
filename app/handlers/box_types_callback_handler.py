from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app import dp, bot
from app.database.database import session, Box


@dp.callback_query_handler(lambda cb: cb.data == 'my_box_btn')
async def my_type_box(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    my_boxes = session.query(Box).where(Box.type_ == 'my')
    my_boxes_keyboard = InlineKeyboardMarkup(row_width=1)
    for box in my_boxes:
        my_box_btn = InlineKeyboardButton(f'🎁 {box.name} ({box.price} грн)', callback_data=f'dbox-{box.name}')
        my_boxes_keyboard.add(my_box_btn)
    box_back = InlineKeyboardButton('⬅ Назад до типів кейсу', callback_data='back_to_type_of_box')
    my_boxes_keyboard.add(box_back)

    await bot.send_message(callback_query.message.chat.id, 'Авторські кейси:', reply_markup=my_boxes_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'farm_box_btn')
async def farm_type_box(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    my_boxes = session.query(Box).where(Box.type_ == 'farm')
    my_boxes_keyboard = InlineKeyboardMarkup(row_width=1)
    for box in my_boxes:
        my_box_btn = InlineKeyboardButton(f'🎁 {box.name} ({box.price} грн)', callback_data=f'dbox-{box.name}')
        my_boxes_keyboard.add(my_box_btn)
    box_back = InlineKeyboardButton('⬅ Назад до типів кейсу', callback_data='back_to_type_of_box')
    my_boxes_keyboard.add(box_back)

    await bot.send_message(callback_query.message.chat.id, 'Фарм кейси:', reply_markup=my_boxes_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'collection_box_btn')
async def collection_type_box(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    boxes = session.query(Box).where(Box.type_ == 'collection')
    boxes_keyboard = InlineKeyboardMarkup(row_width=1)
    for box in boxes:
        box_btn = InlineKeyboardButton(f'🎁 {box.name} ({box.price} грн)', callback_data=f'dbox-{box.name}')
        boxes_keyboard.add(box_btn)
    box_back = InlineKeyboardButton('⬅ Назад до типів кейсу', callback_data='back_to_type_of_box')
    boxes_keyboard.add(box_back)

    await bot.send_message(callback_query.message.chat.id, 'Колекційні кейси:', reply_markup=boxes_keyboard)
