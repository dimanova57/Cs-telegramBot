from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# If you want to create database write on 6 line ⬇⬇⬇
# engine = create_engine("sqlite:///./app.db?check_same_thread=False")
# BUT THEN ADD /database INTO THIS ⬇⬇⬇
# engine = create_engine("sqlite:///./database/app.db?check_same_thread=False")

engine = create_engine("sqlite:///./database/app.db?check_same_thread=False")
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    nickname = Column(String)
    skins = Column(String)
    last_message = Column(String)
    money = Column(Integer)
    steam_href = Column(Integer)

    def __init__(self, nickname, id):
        self.nickname = nickname
        self.id = id
        self.money = 0
        self.bonus_point = 0
        self.last_message = ''
        self.skins = '[]'


class Skin(Base):
    __tablename__ = "skins"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    steam_href = Column(String)

    def __init__(self, name, price, steam_href):
        self.name = name
        self.price = price
        self.steam_href = steam_href


class Box(Base):
    __tablename__ = "boxes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    skins_dict = Column(String)
    price = Column(Integer)
    type_ = Column(String)

    def __init__(self, name, price, skins_dict, type_):
        self.name = name
        self.price = price
        self.skins_dict = skins_dict
        self.type_ = type_


Base.metadata.create_all(engine)

# skin = Skin('StatTrak™ Mac 10 | Oceanic', 10,
#             'https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20MAC-10%20%7C%20Oceanic%20%28Well-Worn%29')
# session.add(skin)
# skin = Skin('Glock-18 | Off World', 4,
#             'https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Off%20World%20%28Battle-Scarred%29')
# session.add(skin)
# skin = Skin('Desert Eagle | Blue Ply', 4,
#             'https://steamcommunity.com/market/listings/730/Desert%20Eagle%20%7C%20Blue%20Ply%20%28Well-Worn%29')
# session.add(skin)
# skin = Skin('AWP | Capillary', 7,
#             'https://steamcommunity.com/market/listings/730/AWP%20%7C%20Capillary%20%28Field-Tested%29')
# session.add(skin)
# skin = Skin('StatTrak™ MAC-10 | Monkeyflage', 8,
#             'https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20MAC-10%20%7C%20Monkeyflage%20%28Field-Tested%29')
# session.add(skin)
# skin = Skin('Negev | Drop Me', 4,
#             'Drop Me /// https://steamcommunity.com/market/listings/730/Negev%20%7C%20Drop%20Me%20%28Field-Tested%29?l')
# session.add(skin)
# skin = Skin('UMP-45 | Labyrinth', 13,
#             'https://steamcommunity.com/market/listings/730/UMP-45%20%7C%20Labyrinth%20(Factory%20New)?l')
# session.add(skin)
# skin = Skin('USP-S | Black Lotus', 27,
#             'https://steamcommunity.com/market/listings/730/USP-S%20%7C%20Black%20Lotus%20%28Battle-Scarred%29')
# session.add(skin)
# skin = Skin('AK-47 | Safari Mesh', 7,
#             'https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Safari%20Mesh%20%28Field-Tested%29')
# session.add(skin)
# skin = Skin('M4A4 | Converter', 50,
#             'https://steamcommunity.com/market/listings/730/M4A4%20%7C%20Converter%20%28Minimal%20Wear%29')
# session.add(skin)
#
# box = Box('first box', price=12, skins_dict="{'StatTrak™ Mac 10 | Oceanic': 10, "
#                                             "'Glock-18 | Off World': 13, "
#                                             "'Desert Eagle | Blue Ply': 15, "
#                                             "'AWP | Capillary': 10, "
#                                             "'StatTrak™ MAC-10 | Monkeyflage': 12, "
#                                             "'Negev | Drop Me': 15,"
#                                             "'UMP-45 | Labyrinth': 7,"
#                                             "'USP-S | Black Lotus': 5,"
#                                             "'AK-47 | Safari Mesh': 10,"
#                                             "'M4A4 | Converter': 3}", type_='my')
# session.add(box)
#
# session.commit()
