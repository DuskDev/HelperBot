# -*- coding: utf-8 -*-

from datetime import datetime, time, timedelta
import json
import logging
import re

from sqlalchemy import func, tuple_
from telegram import (
    Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
)
from telegram.ext import (
    Updater, CommandHandler, MessageHandler,
    Filters, CallbackQueryHandler
)
from telegram.ext.dispatcher import run_async
from telegram.error import TelegramError

from config import TOKEN, GOVERNMENT_CHAT, CASTLE
from core.chat_commands import CC_SET_WELCOME, CC_HELP, CC_SQUAD, CC_SHOW_WELCOME, CC_TURN_ON_WELCOME, \
    CC_TURN_OFF_WELCOME, CC_SET_TRIGGER, CC_UNSET_TRIGGER, CC_TRIGGER_LIST, CC_ADMIN_LIST, CC_PING, CC_DAY_STATISTICS, \
    CC_WEEK_STATISTICS, CC_BATTLE_STATISTICS, CC_ALLOW_TRIGGER_ALL, CC_DISALLOW_TRIGGER_ALL, CC_ADMINS, \
    CC_ALLOW_PIN_ALL, CC_DISALLOW_PIN_ALL, CC_BOSS_1, CC_BOSS_2, CC_BOSS_3, CC_BOSS_4, CC_OPEN_HIRING, CC_CLOSE_HIRING, \
    CC_PIN, CC_SILENT_PIN, CC_DELETE, CC_KICK
from core.commands import ADMIN_COMMAND_STATUS, ADMIN_COMMAND_RECRUIT, ADMIN_COMMAND_ORDER, ADMIN_COMMAND_SQUAD_LIST, \
    ADMIN_COMMAND_GROUPS, ADMIN_COMMAND_FIRE_UP, USER_COMMAND_ME, USER_COMMAND_BUILD, USER_COMMAND_CONTACTS, \
    USER_COMMAND_SQUAD, USER_COMMAND_STATISTICS, USER_COMMAND_TOP, USER_COMMAND_SQUAD_REQUEST, USER_COMMAND_BACK, \
    TOP_COMMAND_ATTACK, TOP_COMMAND_DEFENCE, TOP_COMMAND_EXP, STATISTICS_COMMAND_EXP, USER_COMMAND_SQUAD_LEAVE, \
    ADMIN_COMMAND_REPORTS, ADMIN_COMMAND_ADMINPANEL, TOP_COMMAND_BUILD, \
    TOP_COMMAND_BATTLES
from core.constants import DAYS_PROFILE_REMIND, DAYS_OLD_PROFILE_KICK
from core.functions.activity import (
    day_activity, week_activity, battle_activity
)
from core.functions.admins import (
    list_admins, admins_for_users, set_admin, del_admin,
    set_global_admin, set_super_admin, del_global_admin
)
from core.functions.ban import unban, ban
from core.functions.bosses import (
    boss_leader, boss_zhalo, boss_monoeye, boss_hydra)
from core.functions.orders import order, orders

from core.functions.common import (
    help_msg, ping, start, error, kick,
    admin_panel, stock_compare, trade_compare,
    delete_msg, delete_user,
    user_panel, web_auth)
from core.functions.inline_keyboard_handling import (
    callback_query, send_status, send_order
)
from core.functions.inline_markup import QueryType
from core.functions.order_groups import group_list, add_group
from core.functions.pin import pin, not_pin_all, pin_all, silent_pin
from core.functions.profile import char_update, char_show, find_by_username, report_received, build_report_received, \
    repair_report_received
from core.functions.squad import (
    add_squad, del_squad, set_invite_link, set_squad_name,
    enable_thorns, disable_thorns,
    squad_list, squad_request, list_squad_requests,
    open_hiring, close_hiring, remove_from_squad, add_to_squad,
    leave_squad_request, squad_about, call_squad, battle_reports_show)
from core.functions.statistics import statistic_about, exp_statistic
from core.functions.top import top_about, attack_top, exp_top, def_top, global_build_top, week_build_top, \
    week_battle_top
from core.functions.triggers import (
    set_trigger, add_trigger, del_trigger, list_triggers, enable_trigger_all,
    disable_trigger_all, trigger_show,
    set_global_trigger, add_global_trigger, del_global_trigger
)
from core.functions.welcome import (
    welcome, set_welcome, show_welcome, enable_welcome, disable_welcome
)
from core.regexp import PROFILE, HERO, REPORT, BUILD_REPORT, REPAIR_REPORT, STOCK, TRADE_BOT
from core.texts import (
    MSG_SQUAD_READY, MSG_FULL_TEXT_LINE, MSG_FULL_TEXT_TOTAL,
    MSG_MAIN_INLINE_BATTLE, MSG_MAIN_READY_TO_BATTLE, MSG_IN_DEV, MSG_UPDATE_PROFILE, MSG_SQUAD_DELETE_OUTDATED,
    MSG_SQUAD_DELETE_OUTDATED_EXT)
from core.types import Session, Order, Squad, Admin, user_allowed, Character, SquadMember, User
from core.utils import add_user, send_async

from sqlalchemy.exc import SQLAlchemyError

# -----constants----
CWBOT_ID = 265204902
TRADEBOT_ID = 278525885
# -------------------

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def battle_time():
    """ Определяет, наступило ли время битвы """
    now = datetime.now().time()
    if now.hour % 4 == 3 and now.minute >= 57:
        return True
    return False


def del_msg(bot, job):
    try:
        bot.delete_message(job.context[0], job.context[1])
    except TelegramError:
        pass


@run_async
@user_allowed
def manage_all(bot: Bot, update: Update, session, chat_data, job_queue):
    add_user(update.message.from_user, session)
    if update.message.chat.type in ['group', 'supergroup', 'channel']:
        squad = session.query(Squad).filter_by(
            chat_id=update.message.chat.id).first()
        admin = session.query(Admin).filter(
            Admin.user_id == update.message.from_user.id and
            Admin.admin_group in [update.message.chat.id, 0]).first()

        if squad is not None and admin is None and battle_time():
            bot.delete_message(update.message.chat.id,
                               update.message.message_id)

        if not update.message.text:
            return

        text = update.message.text.lower()

        if text.startswith(CC_SET_WELCOME):
            set_welcome(bot, update)
        elif text == CC_HELP:
            help_msg(bot, update)
        elif text == CC_SQUAD:
            call_squad(bot, update)
        elif text == CC_SHOW_WELCOME:
            show_welcome(bot, update)
        elif text == CC_TURN_ON_WELCOME:
            enable_welcome(bot, update)
        elif text == CC_TURN_OFF_WELCOME:
            disable_welcome(bot, update)
        elif text.startswith(CC_SET_TRIGGER):
            set_trigger(bot, update)
        elif text.startswith(CC_UNSET_TRIGGER):
            del_trigger(bot, update)
        elif text == CC_TRIGGER_LIST:
            list_triggers(bot, update)
        elif text == CC_ADMIN_LIST:
            list_admins(bot, update)
        elif text == CC_PING:
            ping(bot, update)
        elif text == CC_DAY_STATISTICS:
            day_activity(bot, update)
        elif text == CC_WEEK_STATISTICS:
            week_activity(bot, update)
        elif text == CC_BATTLE_STATISTICS:
            battle_activity(bot, update)
        elif text == CC_ALLOW_TRIGGER_ALL:
            enable_trigger_all(bot, update)
        elif text == CC_DISALLOW_TRIGGER_ALL:
            disable_trigger_all(bot, update)
        elif text in CC_ADMINS:
            admins_for_users(bot, update)
        elif text == CC_ALLOW_PIN_ALL:
            pin_all(bot, update)
        elif text == CC_DISALLOW_PIN_ALL:
            not_pin_all(bot, update)
        elif text in CC_BOSS_1:
            boss_leader(bot, update)
        elif text in CC_BOSS_2:
            boss_zhalo(bot, update)
        elif text in CC_BOSS_3:
            boss_monoeye(bot, update)
        elif text in CC_BOSS_4:
            boss_hydra(bot, update)
        elif text == CC_OPEN_HIRING:
            open_hiring(bot, update)
        elif text == CC_CLOSE_HIRING:
            close_hiring(bot, update)
        elif update.message.reply_to_message is not None:
            if text == CC_PIN:
                pin(bot, update)
            elif text == CC_SILENT_PIN:
                silent_pin(bot, update)
            elif text == CC_DELETE:
                delete_msg(bot, update)
            elif text == CC_KICK:
                delete_user(bot, update)
            else:
                trigger_show(bot, update)
        elif re.search(REPORT, update.message.text):
            if update.message.forward_from.id == CWBOT_ID:
                report_received(bot, update)
        else:
            trigger_show(bot, update)

    elif update.message.chat.type == 'private':
        admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
        is_admin = False
        for _ in admin:
            is_admin = True
            break

        if 'order_wait' in chat_data and chat_data['order_wait']:
            order(bot, update, chat_data)

        elif update.message.text:
            text = update.message.text.lower()

            if text == ADMIN_COMMAND_STATUS.lower():
                send_status(bot, update)
            elif text == USER_COMMAND_BACK.lower():
                user_panel(bot, update)
            elif text == USER_COMMAND_SQUAD_REQUEST.lower():
                squad_request(bot, update)
            elif text == ADMIN_COMMAND_RECRUIT.lower():
                list_squad_requests(bot, update)
            elif text == ADMIN_COMMAND_ORDER.lower():
                orders(bot, update, chat_data)
            elif text == ADMIN_COMMAND_SQUAD_LIST.lower():
                squad_list(bot, update)
            elif text == ADMIN_COMMAND_GROUPS.lower():
                group_list(bot, update)
            elif text == ADMIN_COMMAND_REPORTS.lower():
                battle_reports_show(bot, update)
            elif text == ADMIN_COMMAND_FIRE_UP.lower():
                remove_from_squad(bot, update)
            elif text == USER_COMMAND_ME.lower():
                char_show(bot, update)
            elif text == USER_COMMAND_TOP.lower():
                top_about(bot, update)
            elif text == TOP_COMMAND_ATTACK.lower():
                attack_top(bot, update)
            elif text == TOP_COMMAND_DEFENCE.lower():
                def_top(bot, update)
            elif text == TOP_COMMAND_EXP.lower():
                exp_top(bot, update)
            elif text == TOP_COMMAND_BUILD.lower():
                week_build_top(bot, update)
            elif text == TOP_COMMAND_BATTLES.lower():
                week_battle_top(bot, update)
            elif text == USER_COMMAND_BUILD.lower():
                send_async(bot,
                           chat_id=update.message.chat.id,
                           text=MSG_IN_DEV,
                           parse_mode=ParseMode.HTML)
            elif text == USER_COMMAND_STATISTICS.lower():
                statistic_about(bot, update)
            elif text == STATISTICS_COMMAND_EXP.lower():
                exp_statistic(bot, update)
            elif text == USER_COMMAND_SQUAD.lower():
                squad_about(bot, update)
            elif text == USER_COMMAND_SQUAD_LEAVE.lower():
                leave_squad_request(bot, update)
            elif text == USER_COMMAND_CONTACTS.lower():
                web_auth(bot, update)
            elif text == ADMIN_COMMAND_ADMINPANEL.lower():
                admin_panel(bot, update)
            elif 'wait_group_name' in chat_data and chat_data['wait_group_name']:
                add_group(bot, update, chat_data)

            elif update.message.forward_from:
                from_id = update.message.forward_from.id

                if from_id == CWBOT_ID:
                    if text.startswith(STOCK):
                        stock_compare(bot, update, chat_data)
                    elif re.search(PROFILE, update.message.text) or re.search(HERO, update.message.text):
                        char_update(bot, update)
                    elif re.search(REPORT, update.message.text):
                        report_received(bot, update)
                    elif re.search(BUILD_REPORT, update.message.text):
                        build_report_received(bot, update)
                    elif re.search(REPAIR_REPORT, update.message.text):
                        repair_report_received(bot, update)
                elif from_id == TRADEBOT_ID:
                    if TRADE_BOT in text:
                        trade_compare(bot, update, chat_data)
            elif not is_admin:
                user_panel(bot, update)
            else:
                order(bot, update, chat_data)
        elif not is_admin:
            user_panel(bot, update)
        else:
            order(bot, update, chat_data)


@run_async
def ready_to_battle(bot: Bot, job_queue):
    session = Session()
    try:
        group = session.query(Squad).all()
        for item in group:
            new_order = Order()
            new_order.text = MSG_MAIN_READY_TO_BATTLE
            new_order.chat_id = item.chat_id
            new_order.date = datetime.now()
            new_order.confirmed_msg = 0
            session.add(new_order)
            session.commit()

            callback_data = json.dumps(
                {'t': QueryType.OrderOk.value, 'id': new_order.id})
            markup = InlineKeyboardMarkup([
                [InlineKeyboardButton(MSG_MAIN_INLINE_BATTLE,
                                      callback_data=callback_data)]])

            msg = send_order(bot, new_order.text, 0, new_order.chat_id, markup)

            try:
                msg = msg.result().result()
                if msg is not None:
                    bot.request.post(bot.base_url + '/pinChatMessage',
                                     {'chat_id': new_order.chat_id,
                                      'message_id': msg.message_id,
                                      'disable_notification': False})

            except TelegramError as err:
                bot.logger.error(err.message)

    except SQLAlchemyError as err:
        bot.logger.error(str(err))
        Session.rollback()


@run_async
def ready_to_battle_result(bot: Bot, job_queue):
    session = Session()
    try:
        group = session.query(Squad).all()
        full_attack = 0
        full_defence = 0
        full_text = ''
        full_count = 0

        for item in group:
            ready_order = session.query(Order).filter_by(
                chat_id=item.chat_id,
                text=MSG_MAIN_READY_TO_BATTLE).order_by(Order.date.desc()).first()

            if ready_order is not None:
                attack = 0
                defence = 0
                for clear in ready_order.cleared:
                    if clear.user.character:
                        attack += clear.user.character.attack
                        defence += clear.user.character.defence

                text = MSG_SQUAD_READY.format(len(ready_order.cleared),
                                              item.squad_name,
                                              attack,
                                              defence)

                send_async(bot,
                           chat_id=item.chat_id,
                           text=text,
                           parse_mode=ParseMode.HTML)

                full_attack += attack
                full_defence += defence
                full_count += len(ready_order.cleared)
                full_text += MSG_FULL_TEXT_LINE.format(item.squad_name,
                                                       len(ready_order.cleared),
                                                       attack,
                                                       defence)

        full_text += MSG_FULL_TEXT_TOTAL.format(full_count,
                                                full_attack,
                                                full_defence)

        send_async(bot,
                   chat_id=GOVERNMENT_CHAT,
                   text=full_text,
                   parse_mode=ParseMode.HTML)

    except SQLAlchemyError as err:
        bot.logger.error(str(err))
        Session.rollback()


@run_async
def fresh_profiles(bot: Bot, job_queue):
    session = Session()
    try:
        actual_profiles = session.query(Character.user_id, func.max(Character.date)). \
            group_by(Character.user_id)
        actual_profiles = actual_profiles.all()
        characters = session.query(Character).filter(tuple_(Character.user_id, Character.date)
                                                     .in_([(a[0], a[1]) for a in actual_profiles]),
                                                     datetime.now() - timedelta(
                                                         days=DAYS_PROFILE_REMIND) > Character.date,
                                                     Character.date > datetime.now() - timedelta(
                                                         days=DAYS_OLD_PROFILE_KICK))
        if CASTLE:
            characters = characters.filter_by(castle=CASTLE)
        characters = characters.all()
        for character in characters:
            send_async(bot,
                       chat_id=character.user_id,
                       text=MSG_UPDATE_PROFILE,
                       parse_mode=ParseMode.HTML)
        characters = session.query(Character).filter(tuple_(Character.user_id, Character.date)
                                                     .in_([(a[0], a[1]) for a in actual_profiles]),
                                                     Character.date < datetime.now() - timedelta(
                                                         days=DAYS_OLD_PROFILE_KICK)).all()
        members = session.query(SquadMember, User).filter(SquadMember.user_id
                                                          .in_([character.user_id for character in characters])) \
            .join(User, User.id == SquadMember.user_id).all()
        for member, user in members:
            session.delete(member)
            admins = session.query(Admin).filter_by(admin_group=member.squad_id).all()
            for adm in admins:
                send_async(bot, chat_id=adm.user_id,
                           text=MSG_SQUAD_DELETE_OUTDATED_EXT
                           .format(member.user.character.name, member.user.username, member.squad.squad_name),
                           parse_mode=ParseMode.HTML)
            send_async(bot, chat_id=member.squad_id,
                       text=MSG_SQUAD_DELETE_OUTDATED_EXT.format(member.user.character.name, member.user.username,
                                                                 member.squad.squad_name),
                       parse_mode=ParseMode.HTML)
            send_async(bot,
                       chat_id=member.user_id,
                       text=MSG_SQUAD_DELETE_OUTDATED,
                       parse_mode=ParseMode.HTML)
        session.commit()
    except SQLAlchemyError as err:
        bot.logger.error(str(err))
        Session.rollback()


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    disp = updater.dispatcher

    # on different commands - answer in Telegram
    disp.add_handler(CommandHandler("start", user_panel))
    disp.add_handler(CommandHandler("admin", admin_panel))
    disp.add_handler(CommandHandler("help", help_msg))
    disp.add_handler(CommandHandler("ping", ping))
    disp.add_handler(CommandHandler("set_global_trigger", set_global_trigger))
    disp.add_handler(CommandHandler("add_global_trigger", add_global_trigger))
    disp.add_handler(CommandHandler("del_global_trigger", del_global_trigger))
    disp.add_handler(CommandHandler("set_trigger", set_trigger))
    disp.add_handler(CommandHandler("add_trigger", add_trigger))
    disp.add_handler(CommandHandler("del_trigger", del_trigger))
    disp.add_handler(CommandHandler("list_triggers", list_triggers))
    disp.add_handler(CommandHandler("set_welcome", set_welcome))
    disp.add_handler(CommandHandler("enable_welcome", enable_welcome))
    disp.add_handler(CommandHandler("disable_welcome", disable_welcome))
    disp.add_handler(CommandHandler("show_welcome", show_welcome))
    disp.add_handler(CommandHandler("add_admin", set_admin))
    disp.add_handler(CommandHandler("add_global_admin", set_global_admin))
    disp.add_handler(CommandHandler("del_global_admin", del_global_admin))
    disp.add_handler(CommandHandler("add_super_admin", set_super_admin))
    disp.add_handler(CommandHandler("del_admin", del_admin))
    disp.add_handler(CommandHandler("list_admins", list_admins))
    disp.add_handler(CommandHandler("kick", kick))
    disp.add_handler(CommandHandler("enable_trigger", enable_trigger_all))
    disp.add_handler(CommandHandler("disable_trigger", disable_trigger_all))
    disp.add_handler(CommandHandler("me", char_show))

    disp.add_handler(CommandHandler("add_squad", add_squad))
    disp.add_handler(CommandHandler("del_squad", del_squad))
    disp.add_handler(CommandHandler("enable_thorns", enable_thorns))
    disp.add_handler(CommandHandler("disable_thorns", disable_thorns))
    disp.add_handler(CommandHandler("set_squad_name", set_squad_name))
    disp.add_handler(CommandHandler("set_invite_link", set_invite_link))
    disp.add_handler(CommandHandler("find", find_by_username))
    disp.add_handler(CommandHandler("add", add_to_squad))
    disp.add_handler(CommandHandler("ban", ban))
    disp.add_handler(CommandHandler("unban", unban))

    disp.add_handler(CallbackQueryHandler(callback_query, pass_chat_data=True, pass_job_queue=True))

    # on noncommand i.e message - echo the message on Telegram
    disp.add_handler(MessageHandler(Filters.status_update, welcome))
    # disp.add_handler(MessageHandler(
    # Filters.text, manage_text, pass_chat_data=True))
    disp.add_handler(MessageHandler(
        Filters.all, manage_all, pass_chat_data=True, pass_job_queue=True))

    # log all errors
    disp.add_error_handler(error)

    updater.job_queue.run_daily(ready_to_battle, time(hour=7, minute=50))
    updater.job_queue.run_daily(ready_to_battle_result,
                                time(hour=7, minute=55))
    updater.job_queue.run_daily(ready_to_battle, time(hour=11, minute=50))
    updater.job_queue.run_daily(ready_to_battle_result,
                                time(hour=11, minute=55))
    updater.job_queue.run_daily(ready_to_battle, time(hour=15, minute=50))
    updater.job_queue.run_daily(ready_to_battle_result,
                                time(hour=15, minute=55))
    updater.job_queue.run_daily(ready_to_battle, time(hour=19, minute=50))
    updater.job_queue.run_daily(ready_to_battle_result,
                                time(hour=19, minute=55))
    updater.job_queue.run_daily(ready_to_battle, time(hour=23, minute=50))
    updater.job_queue.run_daily(ready_to_battle_result,
                                time(hour=23, minute=55))
    updater.job_queue.run_daily(fresh_profiles,
                                time(hour=7, minute=40))
    updater.job_queue.run_daily(fresh_profiles,
                                time(hour=11, minute=40))
    updater.job_queue.run_daily(fresh_profiles,
                                time(hour=15, minute=40))
    updater.job_queue.run_daily(fresh_profiles,
                                time(hour=19, minute=40))
    updater.job_queue.run_daily(fresh_profiles,
                                time(hour=23, minute=40))

    # Start the Bot
    updater.start_polling()
    # app.run(port=API_PORT)
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
