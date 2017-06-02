from telegram import Update, Bot
from core.types import User, Group, session
from core.template import fill_template
from core.utils import send_async

newbie_msg = 'Новый игрок в замке!\n' \
             'Все на вербовку %username%!'


def newbie(bot: Bot, update: Update):
    if update.message.chat.id in [-1001045426965]:
        if update.message.new_chat_member is not None:
            user = session.query(User).filter(User.id == update.message.new_chat_member.id).first()
            if user is None:
                group = session.query(Group).filter(Group.id == -1001106022956).first()
                if group is not None:
                    send_async(bot, chat_id=update.message.chat.id,
                               text=fill_template(newbie_msg, update.message.new_chat_member))
