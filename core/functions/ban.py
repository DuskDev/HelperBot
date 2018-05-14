from datetime import datetime

from telegram import Bot, Update

from core.texts import MSG_USER_UNKNOWN, MSG_USER_BANNED, MSG_YOU_BANNED, MSG_BAN_COMPLETE, MSG_ALREADY_BANNED, \
    MSG_USER_NOT_BANNED, MSG_USER_UNBANNED, MSG_YOU_UNBANNED, MSG_NO_REASON
from core.types import admin_allowed, Ban, User, Squad, SquadMember, Admin
from core.utils import send_async


@admin_allowed()
def ban(bot: Bot, update: Update, session):
    username, reason = update.message.text.split(' ', 2)[1:]
    username = username.replace('@', '')
    user = session.query(User).filter_by(username=username).first()
    if user:
        banned = session.query(Ban).filter_by(user_id=user.id).first()
        if banned:
            send_async(bot, chat_id=update.message.chat.id,
                       text=MSG_ALREADY_BANNED.format(banned.to_date, banned.reason))
        else:
            banned = Ban()
            banned.user_id = user.id
            banned.from_date = datetime.now()
            banned.to_date = datetime.max
            banned.reason = reason or MSG_NO_REASON
            member = session.query(SquadMember).filter_by(user_id=user.id).first()
            if member:
                session.delete(member)
            admins = session.query(Admin).filter_by(user_id=user.id).all()
            for admin in admins:
                session.delete(admin)
            session.add(banned)
            session.commit()
            squads = session.query(Squad).all()
            for squad in squads:
                send_async(bot, chat_id=squad.chat_id, text=MSG_USER_BANNED.format('@' + username))
            send_async(bot, chat_id=user.id, text=MSG_YOU_BANNED.format(banned.reason))
            send_async(bot, chat_id=update.message.chat.id, text=MSG_BAN_COMPLETE)
    else:
        send_async(bot, chat_id=update.message.chat.id, text=MSG_USER_UNKNOWN)


@admin_allowed()
def unban(bot: Bot, update: Update, session):
    username = update.message.text.split(' ', 1)[1]
    username = username.replace('@', '')
    user = session.query(User).filter_by(username=username).first()
    if user:
        banned = session.query(Ban).filter_by(user_id=user.id).first()
        if banned:
            session.delete(banned)
            session.commit()
            send_async(bot, chat_id=user.id, text=MSG_YOU_UNBANNED)
            send_async(bot, chat_id=update.message.chat.id, text=MSG_USER_UNBANNED.format('@' + user.username))
        else:
            send_async(bot, chat_id=update.message.chat.id, text=MSG_USER_NOT_BANNED)
    else:
        send_async(bot, chat_id=update.message.chat.id, text=MSG_USER_UNKNOWN)
