from sqlalchemy import func, and_, or_
from telegram import Update, Bot

from core.functions.triggers import trigger_decorator
from core.types import User, Character, SquadMember
from core.utils import send_async, update_group, ping_users


def select_users(group, min_lvl, max_lvl, session):
    characters = session.query(Character.user_id, func.max(Character.date)).group_by(Character.user_id).all()
    characters = session.query(Character).filter(or_(*(and_(Character.user_id == user_id, Character.date == date)
                                                 for (user_id, date) in characters))).subquery('characters')
    users = session.query(User).join(characters).join(SquadMember)
    users = users.filter(SquadMember.squad_id == group.id)
    if min_lvl:
        users = users.filter(characters.c.level >= min_lvl)
    if max_lvl:
        users = users.filter(characters.c.level <= max_lvl)
    return users.all()


@trigger_decorator
def boss_leader(bot: Bot, update: Update, session):
    group = update_group(update.message.chat, session)
    if len(group.squad) == 1:
        users = select_users(group, 15, 25, session)
        ping_users(bot, users, update.message.chat.id)


@trigger_decorator
def boss_zhalo(bot: Bot, update: Update, session):
    group = update_group(update.message.chat, session)
    if len(group.squad) == 1:
        users = select_users(group, 26, 35, session)
        ping_users(bot, users, update.message.chat.id)


@trigger_decorator
def boss_monoeye(bot: Bot, update: Update, session):
    group = update_group(update.message.chat, session)
    if len(group.squad) == 1:
        users = select_users(group, 36, 45, session)
        ping_users(bot, users, update.message.chat.id)


@trigger_decorator
def boss_hydra(bot: Bot, update: Update, session):
    group = update_group(update.message.chat, session)
    if len(group.squad) == 1:
        users = select_users(group, 46, 0, session)
        ping_users(bot, users, update.message.chat.id)
