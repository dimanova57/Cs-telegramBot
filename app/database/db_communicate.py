from .database import session, User, Box, Skin
from .parser import open_box_with_result, add_skin_to_list, from_string_to_list, delete_skin_from_list


def add_user(user_id, user_name):
    """This function create and add user to bd"""

    user = User(user_name, user_id)
    session.add(user)
    session.commit()


def change_user_last_message(user_id, message):
    user = session.query(User).where(User.id == user_id).first()
    user.last_message = message
    session.commit()


def show_user_last_message_by(user_id):
    user = session.query(User).where(User.id == user_id).first()
    return user.last_message


def get_skin_list():
    skin_list = session.query(Skin).all()
    return skin_list


def get_box_list():
    box_list = session.query(Box).all()
    return box_list


def show_balance_by_(user_id):
    user = session.query(User).where(User.id == user_id).first()
    return user.money


def add_money_to_user_by(user_id, money):
    user = session.query(User).where(User.id == user_id).first()
    if user:
        user.money += money
        session.commit()
    else:
        print('this user isn`t in bd!!!')


def is_user_in_bd_by(user_id):
    user = session.query(User).where(User.id == user_id).first()
    if user:
        return True
    return False


def open_box_for_user(user_id, box_name):
    user = session.query(User).where(User.id == user_id).first()
    box = session.query(Box).where(Box.name == box_name).first()
    if box and user:
        if user.money - box.price >= 0:
            user.money -= box.price
            skin_name = open_box_with_result(box.name)
            new_list = add_skin_to_list(user.skins, skin_name)
            user.skins = new_list
            session.commit()
            return skin_name
        return 'Невистачає грошей'
    return False


def show_all_user_skins_by(user_id) -> list:
    user = session.query(User).where(User.id == user_id).first()
    return from_string_to_list(user.skins)


def delete_skin_from_user_inventory_by(user_id, skin_name):
    user = session.query(User).where(User.id == user_id).first()
    user.skins = delete_skin_from_list(user.skins, skin_name)
    session.commit()


def create_steam_href_by(user_id, steam_href):
    user = session.query(User).where(User.id == user_id).first()
    if user and 'https://steamcommunity.com/tradeoffer' in steam_href:
        user.steam_href = steam_href
        session.commit()
        return 'Ваша Trade силка успішно закріплена за вами!'
    else:
        return 'Введіть вашу Trade силку, щось мені підказує, але це не вона('

