# Callback handlers
from aiogram import types
from aiogram.utils.exceptions import MessageToDeleteNotFound

from app import bot, dp
from app.database.database import User
from app.database.db_communicate import open_box_for_user, delete_skin_from_user_inventory_by
from ..database.parser import from_string_to_dict
from ..settings import ADMIN_ID


@dp.callback_query_handler(lambda cb: cb.data == 'paying_btn')
async def paying(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.message.chat.id, 'Введіть суму поповнення')
    change_user_last_message(callback_query.message.chat.id, 'paying')


@dp.callback_query_handler(lambda cb: cb.data == 'sell_all')
async def inventory_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    for skin_name in show_all_user_skins_by(callback_query.message.chat.id):
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        add_money_to_user_by(callback_query.message.chat.id, skin.price)
        delete_skin_from_user_inventory_by(callback_query.message.chat.id, skin_name)

    skins_keyboard = InlineKeyboardMarkup(row_width=1)
    for skin_name in show_all_user_skins_by(callback_query.message.chat.id):
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        skin_btn = InlineKeyboardButton(f'✅{skin.name}', callback_data=f'{skin.id}')
        skins_keyboard.add(skin_btn)
    inventory_back_btn = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')
    inventory_sell_all_btn = InlineKeyboardButton('💰 Продати всі скіни', callback_data='sell_all')
    skins_keyboard.add(inventory_sell_all_btn, inventory_back_btn)
    await bot.send_message(callback_query.message.chat.id,
                           f'💰 Ваш баланс: {show_balance_by_(callback_query.message.chat.id)} грн')
    await bot.send_message(callback_query.message.chat.id, '📭 Ваш інвентар',
                           reply_markup=skins_keyboard)


@dp.callback_query_handler(lambda cb: cb.data == 'in_inventory')
async def inventory_back(callback_query: types.CallbackQuery):
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


from .back_handlers import *
from .menu_callback_handler import *
from .box_types_callback_handler import *
from .admin_callback_handler import *


@dp.callback_query_handler(lambda cb: cb.data)
async def another_handler(callback_query: types.CallbackQuery):
    if 'sell' in callback_query.data or 'invent' in callback_query.data:
        if 'sell' in callback_query.data:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            skin_name = callback_query.data.split('sell-')[1]
            skin = session.query(Skin).where(Skin.name == skin_name).first()
            add_money_to_user_by(callback_query.message.chat.id, skin.price)
            delete_skin_from_user_inventory_by(callback_query.message.chat.id, skin_name)
            skins_keyboard = InlineKeyboardMarkup(row_width=1)
            for skin_name in show_all_user_skins_by(callback_query.message.chat.id):
                skin = session.query(Skin).where(Skin.name == skin_name).first()
                skin_btn = InlineKeyboardButton(f'✅{skin.name}', callback_data=f'{skin.id}')
                skins_keyboard.add(skin_btn)
            inventory_back_btn = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')
            skins_keyboard.add(inventory_back_btn)
            await bot.send_message(callback_query.message.chat.id, f'💰 Скін успішно продався\nБаланс'
                                                                   f': {show_balance_by_(callback_query.message.chat.id)}'
                                                                   f' грн')
            await bot.send_message(callback_query.message.chat.id, f'📭 Ваш інвентар',
                                   reply_markup=skins_keyboard)
        else:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
            skin_name = callback_query.data.split('invent-')[1]
            user = session.query(User).where(User.id == callback_query.message.chat.id).first()
            if user.steam_href:
                delete_btn = InlineKeyboardButton('🗑 Виконано', callback_data='delete_msg')
                delete_keyboard = InlineKeyboardMarkup().add(delete_btn)

                await bot.send_message(ADMIN_ID, f'Вивід в Steam account\nName: {user.nickname}\nId: {user.id}\n'
                                                 f'Skin: {skin_name}\nTrade url: {user.steam_href}',
                                       reply_markup=delete_keyboard)
                delete_skin_from_user_inventory_by(callback_query.message.chat.id, skin_name)
                await bot.send_message(callback_query.message.chat.id,
                                       f'Скін успішно куплено\nОчікуйте на продавця\nЦе '
                                       f'може зайняти 7-9 днів')
                await bot.send_message(callback_query.message.chat.id, 'Обери дії з меню',
                                       reply_markup=inline_keyboard.menu_keyboard)
                return None
            else:
                await bot.send_message(callback_query.message.chat.id,
                                       f'Для початку додайте вашу Trade силку!',
                                       reply_markup=inline_keyboard.trade_keyboard)
                return None
    if 'dbox' in callback_query.data or '':
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        box_name = callback_query.data.split('box-')[1]
        box = session.query(Box).where(Box.name == box_name).first()
        await bot.answer_callback_query(callback_query.id)
        skins_keyboard = InlineKeyboardMarkup()
        buy_keyboard = InlineKeyboardMarkup(row_width=1)
        for skin_name in from_string_to_dict(box.skins_dict).keys():
            skin = session.query(Skin).where(Skin.name == skin_name).first()
            skin_btn = InlineKeyboardButton(f'{skin.name} ({skin.price} грн)', callback_data=f'skin-{skin.id}'
                                                                                             f'skin-{box_name}')
            skins_keyboard.add(skin_btn)
        buy_box_btn = InlineKeyboardButton('🛍 Придбати 🛍', callback_data=f'buy_box_btn-{box.name}')
        back_box_btn = InlineKeyboardButton('⬅ Назад до кейсів', callback_data='back_to_type_of_box2')

        buy_keyboard.add(buy_box_btn, back_box_btn)

        await bot.send_message(callback_query.message.chat.id, 'Всі скіни кейсу', reply_markup=skins_keyboard)
        await bot.send_message(callback_query.message.chat.id, 'Придбай зараз цей кейсㅤ                  ㅤ',
                               reply_markup=buy_keyboard)

    elif 'skin-' in callback_query.data:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id + 1)
        skin_id = callback_query.data.split('skin-')[1]
        skin = session.query(Skin).where(Skin.id == skin_id).first()
        back_btn = InlineKeyboardButton('⬅ Назад до кейсу',
                                        callback_data=f"dbox-{callback_query.data.split('skin-')[2]}")
        back_keyboard = InlineKeyboardMarkup().add(back_btn)

        await bot.send_message(callback_query.message.chat.id, f'{skin.steam_href}\n\nІм`я: {skin.name}\nЦіна: '
                                                               f'{skin.price}', reply_markup=back_keyboard)
    elif 'info-' in callback_query.data:
        await bot.delete_message(chat_id=callback_query.message.chat.id,
                                 message_id=callback_query.message.message_id)
        skin_name = callback_query.data.split('info-')[1]
        skin = session.query(Skin).where(Skin.name == skin_name).first()
        skin_btn3 = InlineKeyboardButton('⬅ Назад в інвентар', callback_data='back')
        skins_task_keyboard = InlineKeyboardMarkup().add(skin_btn3)
        await bot.send_message(callback_query.message.chat.id,
                               f'{skin.steam_href}\nІм`я: {skin.name}\nЦіна: {skin.price}',
                               reply_markup=skins_task_keyboard)

    elif 'buy_box_btn-' in callback_query.data:
        await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id - 1)
        except MessageToDeleteNotFound:
            pass
        box_name = callback_query.data.split('buy_box_btn-')[1]
        await bot.answer_callback_query(callback_query.id)
        res = open_box_for_user(callback_query.message.chat.id, box_name)
        if res != 'Невистачає грошей' and res != False:
            skin = session.query(Skin).where(Skin.name == res).first()
            buy_box_btn = InlineKeyboardButton('🛍 Придбати знову', callback_data=f'buy_box_btn-{box_name}')
            buy_first_box_btn2 = InlineKeyboardButton('📭 В інвертар', callback_data='in_inventory')
            type_of_box_back2 = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')

            buy_first_box_again = InlineKeyboardMarkup(row_width=1).add(buy_box_btn, buy_first_box_btn2,
                                                                        type_of_box_back2)
            await bot.send_message(callback_query.message.chat.id,
                                   f'{skin.steam_href}\n\n🎉🎉🎉 УУУрррааа! 🎉🎉🎉\n\n⬇⬇⬇ Вам випав скін ⬇⬇⬇\n{res}\n\nЦіна: {skin.price} грн\n'
                                   f'Баланс: {show_balance_by_(callback_query.message.chat.id)} грн',
                                   reply_markup=buy_first_box_again)
            return None
        await bot.send_message(callback_query.message.chat.id, f'{res}', reply_markup=inline_keyboard.paying_keyboard)
    elif callback_query.data:
        try:
            await bot.delete_message(chat_id=callback_query.message.chat.id,
                                     message_id=callback_query.message.message_id)
        except MessageToDeleteNotFound:
            pass
        await bot.answer_callback_query(callback_query.id)
        skin = session.query(Skin).where(Skin.id == callback_query.data).first()
        skins_task_keyboard = InlineKeyboardMarkup(row_width=1)
        try:
            skin_btn1 = InlineKeyboardButton('💵 Продати', callback_data=f'sell-{skin.name}')
            skin_btn2 = InlineKeyboardButton('📪 Вивести в Steam', callback_data=f'invent-{skin.name}')
            skin_btn4 = InlineKeyboardButton('📜 Інформація', callback_data=f'info-{skin.name}')
            skin_btn3 = InlineKeyboardButton('⬅ Назад', callback_data='back')
            skins_task_keyboard.add(skin_btn1, skin_btn2, skin_btn4, skin_btn3)
            await bot.send_message(callback_query.message.chat.id, f'Скін: {skin.name}\nЦіна: {skin.price} грн',
                                   reply_markup=skins_task_keyboard)
        except AttributeError:
            pass
