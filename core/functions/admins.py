from telegram import Update, Bot

# from core.texts import *
from core.texts import (
    MSG_USER_UNKNOWN, MSG_NEW_GROUP_ADMIN, MSG_DEL_GROUP_ADMIN,
    MSG_NEW_GROUP_ADMIN_EXISTS, MSG_DEL_GROUP_ADMIN_NOT_EXIST,
    MSG_LIST_ADMINS_HEADER, MSG_LIST_ADMINS_FORMAT,
    MSG_EMPTY, MSG_LIST_ADMINS_USER_FORMAT,
    MSG_NEW_GLOBAL_ADMIN, MSG_NEW_GLOBAL_ADMIN_EXISTS,
    MSG_NEW_SUPER_ADMIN, MSG_NEW_SUPER_ADMIN_EXISTS,
    MSG_DEL_GLOBAL_ADMIN, MSG_DEL_GLOBAL_ADMIN_NOT_EXIST
)
from core.types import User, AdminType, Admin, admin_allowed, user_allowed
from core.utils import send_async, ping_users
from config import SUPER_ADMIN_ID


@admin_allowed()
def set_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    msg = msg.replace('@', '')
    if msg != '':
        user = session.query(User).filter_by(username=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            adm = session.query(Admin).filter_by(user_id=user.id,
                                                 admin_group=update.message.chat.id).first()

            if adm is None:
                new_group_admin = Admin(user_id=user.id,
                                        admin_type=AdminType.GROUP.value,
                                        admin_group=update.message.chat.id)

                session.add(new_group_admin)
                session.commit()
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GROUP_ADMIN.format(user.username))

            else:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GROUP_ADMIN_EXISTS.format(user.username))


def del_adm(bot, chat_id, user, session):
    adm = session.query(Admin).filter_by(user_id=user.id,
                                         admin_group=chat_id).first()

    if adm is None:
        send_async(bot,
                   chat_id=chat_id,
                   text=MSG_DEL_GROUP_ADMIN_NOT_EXIST.format(user.username))

    else:
        session.delete(adm)
        session.commit()
        send_async(bot,
                   chat_id=chat_id,
                   text=MSG_DEL_GROUP_ADMIN.format(user.username))


@admin_allowed()
def del_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    if msg.find('@') != -1:
        msg = msg.replace('@', '')
        if msg != '':
            user = session.query(User).filter_by(username=msg).first()
            if user is None:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_USER_UNKNOWN)

            else:
                del_adm(bot, update.message.chat.id, user, session)
    else:
        user = session.query(User).filter_by(id=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            del_adm(bot, update.message.chat.id, user, session)


@admin_allowed()
def list_admins(bot: Bot, update: Update, session):
    admins = session.query(Admin).filter(Admin.admin_group == update.message.chat.id).all()
    users = []
    for admin_user in admins:
        users.append(session.query(User).filter_by(id=admin_user.user_id).first())
    msg = MSG_LIST_ADMINS_HEADER
    send_async(bot, chat_id=update.message.chat.id, text=msg)
    ping_users(bot, users, update.message.chat.id, True)


@user_allowed
def admins_for_users(bot: Bot, update: Update, session):
    admins = session.query(Admin).filter(Admin.admin_group == update.message.chat.id).all()
    users = []
    for admin_user in admins:
        users.append(session.query(User).filter_by(id=admin_user.user_id).first())
    msg = MSG_LIST_ADMINS_HEADER
    send_async(bot, chat_id=update.message.chat.id, text=msg)
    ping_users(bot, users, update.message.chat.id, True)


@admin_allowed(adm_type=AdminType.SUPER)
def set_global_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    msg = msg.replace('@', '')
    if msg != '':
        user = session.query(User).filter_by(username=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            adm = session.query(Admin).filter_by(user_id=user.id,
                                                 admin_type=AdminType.FULL.value).first()

            if adm is None:
                new_group_admin = Admin(user_id=user.id,
                                        admin_type=AdminType.FULL.value,
                                        admin_group=0)
                session.add(new_group_admin)
                session.commit()
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GLOBAL_ADMIN.format(user.username))

            else:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_NEW_GLOBAL_ADMIN_EXISTS.format(user.username))


@user_allowed(False)
def set_super_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    msg = msg.replace('@', '')
    if msg != '':
        user = session.query(User).filter_by(username=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            if user.id == SUPER_ADMIN_ID and update.message.from_user.id == SUPER_ADMIN_ID:
                adm = session.query(Admin).filter_by(user_id=user.id, admin_group=0).first()
                if adm is not None:
                    if adm.admin_type == AdminType.SUPER.value:
                        send_async(bot,
                                   chat_id=update.message.chat.id,
                                   text=MSG_NEW_SUPER_ADMIN_EXISTS.format(user.username))

                    else:
                        adm.admin_type = AdminType.SUPER.value
                        session.add(adm)
                        session.commit()
                        send_async(bot,
                                   chat_id=update.message.chat.id,
                                   text=MSG_NEW_SUPER_ADMIN.format(user.username))

                else:
                    new_super_admin = Admin(user_id=user.id,
                                            admin_type=AdminType.SUPER.value,
                                            admin_group=0)

                    session.add(new_super_admin)
                    session.commit()
                    send_async(bot,
                               chat_id=update.message.chat.id,
                               text=MSG_NEW_SUPER_ADMIN.format(user.username))


@admin_allowed(adm_type=AdminType.SUPER)
def del_global_admin(bot: Bot, update: Update, session):
    msg = update.message.text.split(' ', 1)[1]
    if msg.find('@') != -1:
        msg = msg.replace('@', '')
        if msg != '':
            user = session.query(User).filter_by(username=msg).first()
            if user is None:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_USER_UNKNOWN)

            else:
                adm = session.query(Admin).filter_by(user_id=user.id,
                                                     admin_type=AdminType.FULL.value).first()

                if adm is None:
                    send_async(bot,
                               chat_id=update.message.chat.id,
                               text=MSG_DEL_GLOBAL_ADMIN_NOT_EXIST.format(user.username))

                else:
                    session.delete(adm)
                    session.commit()
                    send_async(bot,
                               chat_id=update.message.chat.id,
                               text=MSG_DEL_GLOBAL_ADMIN.format(user.username))
    else:
        user = session.query(User).filter_by(id=msg).first()
        if user is None:
            send_async(bot,
                       chat_id=update.message.chat.id,
                       text=MSG_USER_UNKNOWN)

        else:
            adm = session.query(Admin).filter_by(user_id=user.id,
                                                 admin_type=AdminType.FULL.value).first()
            if adm is None:
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_DEL_GLOBAL_ADMIN_NOT_EXIST.format(user.username))
            else:
                session.delete(adm)
                session.commit()
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_DEL_GLOBAL_ADMIN.format(user.username))
