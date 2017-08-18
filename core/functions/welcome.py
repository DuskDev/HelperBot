from telegram import Update, Bot
from core.types import User, Wellcomed, WelcomeMsg, Group, AdminType, admin, session, Squad, Admin
from core.template import fill_template
from time import time
from core.utils import send_async, add_user, update_group
from core.functions.newbies import newbie
from core.texts import *

last_welcome = 0


def welcome(bot: Bot, update: Update):
    newbie(bot, update)
    global last_welcome
    if update.message.chat.type in ['group', 'supergroup']:
        if update.message.new_chat_member is not None:
            group = update_group(update.message.chat)
            user = add_user(update.message.new_chat_member)
            administrator = session.query(Admin).filter_by(user_id=user.id).all()
            allow_anywhere = False
            for adm in administrator:
                if adm.admin_type == AdminType.FULL.value:
                    allow_anywhere = True
                    break
            if len(group.squad) == 1 and group.squad[0].thorns_enabled and user.id != 386494081 and \
                    (user.member or user.member not in group.squad[0].members) and not allow_anywhere:
                send_async(bot, chat_id=update.message.chat.id,
                           text=MSG_THORNS.format(str(user)))
                bot.kickChatMember(update.message.chat.id, update.message.new_chat_member.id)
                bot.unbanChatMember(update.message.chat.id, update.message.new_chat_member.id)
            else:
                if group.welcome_enabled:
                    welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
                    if welcome_msg is None:
                        welcome_msg = WelcomeMsg(chat_id=group.id, message=MSG_WELCOME_DEFAULT)
                        session.add(welcome_msg)

                    welcomed = session.query(Wellcomed).filter_by(user_id=update.message.new_chat_member.id,
                                                                  chat_id=update.message.chat.id).first()
                    if welcomed is None:
                        if time() - last_welcome > 30:
                            send_async(bot, chat_id=update.message.chat.id,
                                       text=fill_template(welcome_msg.message, user))
                            last_welcome = time()
                        welcomed = Wellcomed(user_id=update.message.new_chat_member.id, chat_id=update.message.chat.id)
                        session.add(welcomed)
                    session.commit()


@admin(adm_type=AdminType.GROUP)
def set_welcome(bot: Bot, update: Update):
    if update.message.chat.type in ['group', 'supergroup']:
        group = update_group(update.message.chat)
        welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
        if welcome_msg is None:
            welcome_msg = WelcomeMsg(chat_id=group.id, message=update.message.text.split(' ', 1)[1])
        else:
            welcome_msg.message = update.message.text.split(' ', 1)[1]
        session.add(welcome_msg)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_SET)


@admin(adm_type=AdminType.GROUP)
def enable_welcome(bot: Bot, update: Update):
    if update.message.chat.type in ['group', 'supergroup']:
        group = update_group(update.message.chat)
        group.welcome_enabled = True
        session.add(group)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_ENABLED)


@admin(adm_type=AdminType.GROUP)
def disable_welcome(bot: Bot, update: Update):
    if update.message.chat.type in ['group', 'supergroup']:
        group = update_group(update.message.chat)
        group.welcome_enabled = False
        session.add(group)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_WELCOME_DISABLED)


@admin(adm_type=AdminType.GROUP)
def show_welcome(bot: Bot, update):
    if update.message.chat.type in ['group', 'supergroup']:
        group = update_group(update.message.chat)
        welcome_msg = session.query(WelcomeMsg).filter_by(chat_id=group.id).first()
        if welcome_msg is None:
            welcome_msg = WelcomeMsg(chat_id=group.id, message=MSG_WELCOME_DEFAULT)
            session.add(welcome_msg)
            session.commit()
        send_async(bot, chat_id=group.id, text=welcome_msg.message)
