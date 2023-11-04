from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

###

type_of_box_btn1 = InlineKeyboardButton('ㅤ    🟥 Авторські кейси', callback_data='my_box_btn')
type_of_box_btn2 = InlineKeyboardButton('🟧 Фарм кейси', callback_data='farm_box_btn')
type_of_box_btn3 = InlineKeyboardButton('ㅤ      🟨 Колекційні кейси', callback_data='collection_box_btn')
type_of_box_back = InlineKeyboardButton('ㅤ  ⬅ Назад до меню', callback_data='type_of_box_back')

all_boxes = InlineKeyboardMarkup(row_width=1)
all_boxes.add(type_of_box_btn1, type_of_box_btn2, type_of_box_btn3, type_of_box_back)

###

first_box_btn = InlineKeyboardButton('first box', callback_data='first_box_btn')

my_boxes = InlineKeyboardMarkup(row_width=1)
my_boxes.add(first_box_btn)

###

paying_btn = InlineKeyboardButton('💎 Поповнити баланс', callback_data='paying_btn')
paying_back = InlineKeyboardButton('⬅ Назад до меню', callback_data='type_of_box_back')


paying_keyboard = InlineKeyboardMarkup(row_width=1).add(paying_btn, paying_back)

###

start_btn = InlineKeyboardButton('▶ Старт', callback_data='start')
order_box_btn = InlineKeyboardButton('📦 Кейси', callback_data='order_box')
balance_btn = InlineKeyboardButton('💰 Баланс', callback_data='balance')
inventory_btn = InlineKeyboardButton('📭 Інвентар', callback_data='skins')
trade_url_btn = InlineKeyboardButton('✉ Trade силка', callback_data='trade_url')

menu_keyboard = InlineKeyboardMarkup()
menu_keyboard.add(start_btn, order_box_btn, balance_btn, inventory_btn, trade_url_btn)

###

trade_url_btn = InlineKeyboardButton('✉ Додати Trade силку', callback_data='trade_url')
trade_url_btn_back = InlineKeyboardButton('⬅ Назад в інвентар', callback_data='back')
trade_keyboard = InlineKeyboardMarkup(row_width=1).add(trade_url_btn, trade_url_btn_back)

###

admin_start_btn = InlineKeyboardButton('▶ User старт', callback_data='start')
admin_add_box_btn = InlineKeyboardButton('➕ Додати кейс', callback_data='add_box')
admin_show_all_skins_btn = InlineKeyboardButton('🔫 Показати всі скіни', callback_data='show_all_skins')
admin_show_all_box_btn = InlineKeyboardButton('📦 Показати всі кейси', callback_data='show_all_box')

admin_menu_keyboard = InlineKeyboardMarkup(row_width=1)
admin_menu_keyboard.add(admin_start_btn, admin_add_box_btn, admin_show_all_skins_btn, admin_show_all_box_btn)

###

admin_btn_back = InlineKeyboardButton('⬅ Назад в меню', callback_data='admin_back')
admin_back_keyboard = InlineKeyboardMarkup().add(admin_btn_back)
