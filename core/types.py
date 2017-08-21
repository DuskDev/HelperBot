# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, UnicodeText, BigInteger
from sqlalchemy.dialects.mysql import DATETIME
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy import event
from sqlalchemy.pool import Pool
import logging
from enum import Enum
from config import DB
import requests
from json import loads
from core.enums import Castle
import threading


class AdminType(Enum):
    SUPER = 0
    FULL = 1
    GROUP = 2


engine = create_engine(DB, echo=False, pool_size=200, max_overflow=50)
logger = logging.getLogger('sqlalchemy.engine')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = scoped_session(Session)()
last_update = datetime.now() - timedelta(minutes=10)


@event.listens_for(Pool, "connect")
def set_unicode(dbapi_conn, conn_record):
    cursor = dbapi_conn.cursor()
    try:
        cursor.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_unicode_ci'")
    except Exception as e:
        logger.error(e)


class Group(Base):
    __tablename__ = 'groups'

    id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText(250))
    title = Column(UnicodeText(250))
    welcome_enabled = Column(Boolean, default=False)
    allow_trigger_all = Column(Boolean, default=False)
    allow_pin_all = Column(Boolean, default=False)
    bot_in_group = Column(Boolean, default=True)

    group_items = relationship('OrderGroupItem', back_populates='chat')
    squad = relationship('Squad', back_populates='chat')
    orders = relationship('Order', back_populates='chat')


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText(250))
    first_name = Column(UnicodeText(250))
    last_name = Column(UnicodeText(250))
    date_added = Column(DateTime, default=datetime.now())

    character = relationship('Character', back_populates='user', order_by='Character.date.desc()', uselist=False)
    orders_confirmed = relationship('OrderCleared', back_populates='user')
    member = relationship('SquadMember', back_populates='user', uselist=False)
    equip = relationship('Equip', back_populates='user', order_by='Equip.date.desc()', uselist=False)
    stock = relationship('Stock', back_populates='user', order_by='Stock.date.desc()', uselist=False)

    def __repr__(self):
        user = ''
        if self.first_name:
            user += self.first_name + ' '
        if self.last_name:
            user += self.last_name + ' '
        if self.username:
            user += '(@' + self.username + ')'
        return user

    def __str__(self):
        user = ''
        if self.first_name:
            user += self.first_name + ' '
        if self.last_name:
            user += self.last_name
        return user


class WelcomeMsg(Base):
    __tablename__ = 'welcomes'

    chat_id = Column(BigInteger, primary_key=True)
    message = Column(UnicodeText(2500))


class Wellcomed(Base):
    __tablename__ = 'wellcomed'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    chat_id = Column(BigInteger, ForeignKey(WelcomeMsg.chat_id), primary_key=True)


class Trigger(Base):
    __tablename__ = 'triggers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    trigger = Column(UnicodeText(2500))
    message = Column(UnicodeText(2500))


class Admin(Base):
    __tablename__ = 'admins'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    admin_type = Column(Integer)
    admin_group = Column(BigInteger, primary_key=True, default=0)


class OrderGroup(Base):
    __tablename__ = 'order_groups'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(UnicodeText(250))

    items = relationship('OrderGroupItem', back_populates='group', cascade="save-update, merge, delete, delete-orphan")


class OrderGroupItem(Base):
    __tablename__ = 'order_group_items'

    group_id = Column(Integer, ForeignKey(OrderGroup.id, ondelete='CASCADE'), primary_key=True)
    chat_id = Column(BigInteger, ForeignKey(Group.id), primary_key=True)

    group = relationship('OrderGroup', back_populates='items')
    chat = relationship('Group', back_populates='group_items')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey(Group.id))
    text = Column(UnicodeText(2500))
    confirmed_msg = Column(BigInteger)
    date = Column(DATETIME(fsp=6), default=datetime.now())

    cleared = relationship('OrderCleared', back_populates='order')
    chat = relationship('Group', back_populates='orders')


class OrderCleared(Base):
    __tablename__ = 'order_cleared'

    order_id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    date = Column(DATETIME(fsp=6), default=datetime.now())

    order = relationship('Order', back_populates='cleared')
    user = relationship('User', back_populates='orders_confirmed')


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(User.id))
    stock = Column(UnicodeText(2500))
    date = Column(DATETIME(fsp=6), default=datetime.now())
    stock_type = Column(Integer)

    user = relationship('User', back_populates='stock')


class Character(Base):
    __tablename__ = 'characters'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    date = Column(DATETIME(fsp=6), primary_key=True)
    name = Column(UnicodeText(250))
    prof = Column(UnicodeText(250))
    pet = Column(UnicodeText(250), nullable=True, default=None)
    petLevel = Column(Integer, default=0)
    maxStamina = Column(Integer, default=5)
    level = Column(Integer)
    attack = Column(Integer)
    defence = Column(Integer)
    exp = Column(Integer)
    needExp = Column(Integer, default=0)
    castle = Column(UnicodeText(100))
    gold = Column(Integer, default=0)
    donateGold = Column(Integer, default=0)

    user = relationship('User', back_populates='character')


class Squad(Base):
    __tablename__ = 'squads'

    chat_id = Column(BigInteger, ForeignKey(Group.id), primary_key=True)
    invite_link = Column(UnicodeText(250), default='')
    squad_name = Column(UnicodeText(250))
    thorns_enabled = Column(Boolean, default=True)
    hiring = Column(Boolean, default=False)

    members = relationship('SquadMember', back_populates='squad')
    chat = relationship('Group', back_populates='squad')


class SquadMember(Base):
    __tablename__ = 'squad_members'

    squad_id = Column(BigInteger, ForeignKey(Squad.chat_id))
    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    approved = Column(Boolean, default=False)

    squad = relationship('Squad', back_populates='members')
    user = relationship('User', back_populates='member')


class Equip(Base):
    __tablename__ = 'equip'

    user_id = Column(BigInteger, ForeignKey(User.id), primary_key=True)
    date = Column(DATETIME(fsp=6), primary_key=True)

    equip = Column(UnicodeText(250))

    user = relationship('User', back_populates='equip')


def admin(adm_type=AdminType.FULL):
    def decorate(func):
        def wrapper(bot, update, *args, **kwargs):
            session = Session()
            adms = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
            allowed = False
            for adm in adms:
                if adm is not None and adm.admin_type <= adm_type.value and \
                        (adm.admin_group in [0, update.message.chat.id] or
                         update.message.chat.id == update.message.from_user.id):
                    if adm.admin_group != 0:
                        group = session.query(Group).filter_by(id=adm.admin_group).first()
                        if group and group.bot_in_group:
                            allowed = True
                            break
                    else:
                        allowed = True
                        break
            if allowed:
                func(bot, update, *args, **kwargs)
        return wrapper
    return decorate


def data_update(func):
    def wrapper(bot, update, *args, **kwargs):
        global last_update
        if datetime.now() - last_update > timedelta(minutes=10):
            last_update = datetime.now()

            def upd():
                session = Session()
                resp = requests.get('https://ker.su/json.php', auth=('ruckus', 'Ruarpamcotkong'))
                data = loads(resp.text)
                for player in data['players']:
                    user = session.query(User).filter_by(id=player['tgid']).first()
                    if user is None:
                        user = User()
                        user.id = player['tgid']
                        user.first_name = player['name']
                        if player['username'] is not None:
                            user.username = player['username'][1:]
                        session.add(user)
                    else:
                        updated = False
                        if player['username'] and user.username != player['username'][1:]:
                            user.username = player['username'][1:]
                            updated = True
                        if updated:
                            session.add(user)
                    character = session.query(Character).filter_by(user_id=user.id,
                                                                   date=datetime.strptime(player['last_update'],
                                                                                          '%Y-%m-%d %H:%M:%S')).first()
                    if character is None:
                        character = Character()
                        character.user_id = user.id
                        character.date = datetime.strptime(player['last_update'], '%Y-%m-%d %H:%M:%S')
                        character.castle = Castle.MINT.value
                        character.prof = player['class']
                        character.name = player['player']
                        character.level = player['level']
                        character.attack = player['attack']
                        character.defence = player['defence']
                        character.exp = player['exp']
                        character.gold = player['gold']
                        session.add(character)
                    member = session.query(SquadMember).filter_by(user_id=user.id).first()
                    squad = session.query(Squad).filter_by(chat_id=player['squad_id']).first()
                    if squad is None:
                        group = session.query(Group).filter_by(id=player['squad_id']).first()
                        if group is not None:
                            squad = Squad()
                            squad.chat_id = player['squad_id']
                            squad.squad_name = player['squad']
                            session.add(squad)
                    if squad is not None and (member is None or member.squad_id != player['squad_id']):
                        if member is None:
                            member = SquadMember()
                            member.user_id = user.id
                            member.approved = True
                        member.squad_id = player['squad_id']
                        session.add(member)
                    session.commit()
            threading.Thread(target=upd).start()
        func(bot, update, *args, **kwargs)
    return wrapper


def with_session(fn):
    def go(*args, **kw):
        try:
            return fn(*args, **kw)
        except:
            session.rollback()
            raise
    return go


Base.metadata.create_all(engine)
