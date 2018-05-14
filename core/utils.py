import http.client

from telegram import Bot
from telegram.error import TelegramError
from telegram.ext.dispatcher import run_async

from core.texts import MSG_LIST_ADMINS_USER_FORMAT, MSG_EMPTY, MSG_LIST_USER_FORMAT
from core.types import Session, User, Group


@run_async
def send_async(bot: Bot, *args, **kwargs):
    try:
        return bot.sendMessage(*args, **kwargs)

    except TelegramError as err:
        bot.logger.error(err.message)
        session = Session()
        group = session.query(Group).filter_by(id=kwargs['chat_id']).first()
        if group is not None:
            group.bot_in_group = False
            session.add(group)
            session.commit()
        return None


def add_user(tg_user, session):
    user = session.query(User).filter_by(id=tg_user.id).first()
    if user is None:
        user = User(id=tg_user.id, username=tg_user.username or '',
                    first_name=tg_user.first_name or '',
                    last_name=tg_user.last_name or '')
        session.add(user)
    else:
        updated = False
        if user.username != tg_user.username:
            user.username = tg_user.username
            updated = True
        if user.first_name != tg_user.first_name:
            user.first_name = tg_user.first_name
            updated = True
        if user.last_name != tg_user.last_name:
            user.last_name = tg_user.last_name
            updated = True
        if updated:
            session.add(user)
    session.commit()
    return user


def update_group(grp, session):
    if grp.type in ['group', 'supergroup', 'channel']:
        group = session.query(Group).filter_by(id=grp.id).first()
        if group is None:
            group = Group(id=grp.id, title=grp.title,
                          username=grp.username)
            session.add(group)

        else:
            updated = False
            if group.username != grp.username:
                group.username = grp.username
                updated = True
            if group.title != grp.title:
                group.title = grp.title
                updated = True
            if not group.bot_in_group:
                group.bot_in_group = True
                updated = True
            if updated:
                session.add(group)

        session.commit()
        return group
    return None


def ping_users(bot: Bot, users: [User], chat_id, long_style=False, *args, **kwargs):
    if not len(users):
        send_async(bot, chat_id=chat_id, text=MSG_EMPTY, *args, **kwargs)
        return

    i = 0
    msg = ''
    if long_style:
        text_format = MSG_LIST_ADMINS_USER_FORMAT
    else:
        text_format = MSG_LIST_USER_FORMAT

    for user in users:
        msg += text_format.format(user.username or '',
                                  user.first_name or '',
                                  user.last_name or '')
        i += 1
        if i == 5:
            send_async(bot, chat_id=chat_id, text=msg, *args, **kwargs)
            i = 0
            msg = ''
    if i != 0:
        send_async(bot, chat_id=chat_id, text=msg, *args, **kwargs)
