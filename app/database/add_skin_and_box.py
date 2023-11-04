import math

from app.database.database import session, Skin, Box


def add_list_of_skins(list_of_skins: str, box_name, box_price, box_type):
    """This function is help to create and change admin account"""

    list_of_skins = list_of_skins.split('\n- ')
    skins_dict = dict()
    print(list_of_skins)
    for skin in list_of_skins:
        skin_list = skin.split('+++')
        print(skin_list)
        skins_dict[skin_list[0]] = int(skin_list[2])
        list_of_skins = session.query(Skin).all()
        res = True
        for skin_ in list_of_skins:
            if skin_list[0] == skin_.name:
                print('No, No, No!')
                res = False
                break
        if res:
            skin_obj = Skin(skin_list[0], int(skin_list[2]), skin_list[1])
            session.add(skin_obj)
            print('skin added')

    session.commit()
    max_price = max(skins_dict.values())
    min_price = min(skins_dict.values())
    for k, v in skins_dict.items():
        skin_count = ((max_price - v) / (max_price - min_price + 1)) * 100
        skins_dict[k] = skin_count
    sum_of_skin_count = sum(skins_dict.values())
    for k, v in skins_dict.items():
        normal_skin_count = (v / sum_of_skin_count) * 500
        if math.ceil(normal_skin_count) > 0:
            skins_dict[k] = math.ceil(normal_skin_count)
        else:
            skins_dict[k] = 2
    print(sum(skins_dict.values()))
    print(skins_dict)
    box_obj = Box(box_name, box_price, skins_dict=f"{skins_dict}", type_=box_type)
    session.add(box_obj)
    session.commit()


list_of_skinsAk = '''АК-47 (StatTrak™) | Елітна серія+++https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20AK-47%20%7C%20Elite%20Build%20%28Field-Tested%29+++140
- АК-47 | Сталева дельта+++https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Steel%20Delta%20%28Minimal%20Wear%29+++110
- Glock-18 | Готовий до зими+++https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Winterized%20%28Well-Worn%29+++2
- P2000 | Покруч+++https://steamcommunity.com/market/listings/730/P2000%20%7C%20Gnarled%20%28Well-Worn%29+++2
- FAMAS (Сувенір) | Каліфорнійський камуфляж+++https://steamcommunity.com/market/listings/730/Souvenir%20FAMAS%20%7C%20CaliCamo%20%28Well-Worn%29+++1
- Nova (Сувенір) | Осердя+++https://steamcommunity.com/market/listings/730/Souvenir%20Nova%20%7C%20Mandrel%20%28Factory%20New%29+++2
- Ґаліль | Руйнівник+++https://steamcommunity.com/market/listings/730/Galil%20AR%20%7C%20Destroyer%20%28Battle-Scarred%29+++2
- Револьвер R8 (Сувенір) | Ніч+++https://steamcommunity.com/market/listings/730/Souvenir%20R8%20Revolver%20%7C%20Night%20%28Well-Worn%29+++1
- SSG 08 | Синя хвоя+++https://steamcommunity.com/market/listings/730/SSG%2008%20%7C%20Blue%20Spruce%20%28Well-Worn%29+++1
- Tec-9 | Армійська сітка+++https://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Army%20Mesh%20%28Field-Tested%29+++1'''
