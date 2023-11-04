# Parser that help to open box
import random

from .database import Box, session


def from_dict_to_string(dict_: dict) -> str:
    """This function help to create dict that can work with database"""

    return f'{dict_}'


def from_string_to_dict(str_: str) -> dict:
    """This function help to create string that can work with database"""

    # "{'1': 20}" 1 - skins id; 20 = 20% !!! Write id in this -> '' !!!
    data = eval(str_)
    return data


def from_string_to_list(str_: str) -> list:
    """This function help to create string that can work with database"""

    data = eval(str_)
    return data


def add_skin_to_list(str_: str, skin_name) -> str:
    data = from_string_to_list(str_)
    data.append(skin_name)
    return f'{data}'


def delete_skin_from_list(str_: str, skin_name) -> str:
    data = from_string_to_list(str_)
    data.remove(f'{skin_name}')
    return f'{data}'


def check_box_work_by(box_name):
    box = session.query(Box).where(Box.name == box_name).first()
    if box:
        return True
    return False


def open_box_with_result(box_name):
    box = session.query(Box).where(Box.name == box_name).first()
    if box:
        if check_box_work_by(box.name):
            list_of_skins = list()
            for key, value in from_string_to_dict(box.skins_dict).items():
                for i in range(value + 1):
                    list_of_skins.append(key)

            skin_name = random.choice(list_of_skins)
            return skin_name

