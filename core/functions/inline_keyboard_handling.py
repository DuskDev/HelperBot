from datetime import datetime, timedelta
import json
from json import loads
import logging

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError, ParseMode
from telegram.ext import JobQueue, Job
from telegram.ext.dispatcher import run_async

from core.enums import Castle, Icons
from core.functions.admins import del_adm
from core.functions.inline_markup import generate_group_info, generate_order_chats_markup, generate_order_groups_markup, \
    generate_ok_markup, generate_groups_manage, generate_group_manage, generate_profile_buttons, generate_squad_list, \
    generate_leave_squad, generate_other_reports, generate_squad_members, QueryType
from core.functions.reply_markup import generate_user_markup
from core.functions.squad import leave_squad
from core.functions.top import global_build_top, week_build_top, week_battle_top, global_battle_top, \
    week_squad_build_top, global_squad_build_top
from core.template import fill_char_template
from core.types import (
    User, Admin, admin_allowed, Order, OrderGroup,
    OrderGroupItem, OrderCleared, Squad, user_allowed,
    SquadMember, MessageType, AdminType, Report)
from core.texts import *
from core.utils import send_async, update_group, add_user

from sqlalchemy import and_

LOGGER = logging.getLogger('MyApp')


order_updated = {}


@admin_allowed()
def send_status(bot: Bot, update: Update, session):
    msg = MSG_GROUP_STATUS_CHOOSE_CHAT
    squads = session.query(Squad).all()
    inline_keys = []
    for squad in squads:
        inline_keys.append(InlineKeyboardButton(squad.squad_name,
                                                callback_data=json.dumps({'t': QueryType.GroupInfo.value,
                                                                          'id': squad.chat_id})))
    inline_markup = InlineKeyboardMarkup([[key] for key in inline_keys])
    send_async(bot, chat_id=update.message.chat.id, text=msg, reply_markup=inline_markup)


@run_async
def send_order(bot, order, order_type, chat_id, markup):
    try:
        msg_sent = None
        if order_type == MessageType.AUDIO.value:
            msg_sent = bot.send_audio(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.DOCUMENT.value:
            msg_sent = bot.send_document(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.VOICE.value:
            msg_sent = bot.send_voice(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.STICKER.value:
            msg_sent = bot.send_sticker(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.CONTACT.value:
            msg = order.replace('\'', '"')
            contact = loads(msg)
            if 'phone_number' not in contact.keys():
                contact['phone_number'] = None
            if 'first_name' not in contact.keys():
                contact['first_name'] = None
            if 'last_name' not in contact.keys():
                contact['last_name'] = None
                msg_sent = bot.send_contact(chat_id,
                                            contact['phone_number'],
                                            contact['first_name'],
                                            contact['last_name'],
                                            reply_markup=markup)
        elif order_type == MessageType.VIDEO.value:
            msg_sent = bot.send_video(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.VIDEO_NOTE.value:
            msg_sent = bot.send_video_note(chat_id, order, reply_markup=markup)
        elif order_type == MessageType.LOCATION.value:
            msg = order.replace('\'', '"')
            location = loads(msg)
            msg_sent = bot.send_location(chat_id, location['latitude'], location['longitude'], reply_markup=markup)
        elif order_type == MessageType.PHOTO.value:
            msg_sent = bot.send_photo(chat_id, order, reply_markup=markup)
        else:
            msg_sent = send_async(bot, chat_id=chat_id, text=order, disable_web_page_preview=True, reply_markup=markup)
        return msg_sent
    except TelegramError as err:
        bot.logger.error(err.message)
        return None


def update_confirmed(bot: Bot, job: Job):
    order = job.context
    confirmed = order.cleared
    msg = MSG_ORDER_CLEARED_BY_HEADER
    for confirm in confirmed:
        msg += str(confirm.user) + '\n'
    bot.editMessageText(msg, order.chat_id, order.confirmed_msg)


@run_async
@user_allowed
def callback_query(bot: Bot, update: Update, session, chat_data: dict, job_queue: JobQueue):
    update_group(update.callback_query.message.chat, session)
    user = add_user(update.effective_user, session)
    data = json.loads(update.callback_query.data)
    if data['t'] == QueryType.GroupList.value:
        msg = MSG_GROUP_STATUS_CHOOSE_CHAT
        squads = session.query(Squad).all()
        inline_keys = []
        for squad in squads:
            inline_keys.append(InlineKeyboardButton(squad.squad_name,
                                                    callback_data=json.dumps({'t': QueryType.GroupInfo.value,
                                                                              'id': squad.chat_id})))
        inline_markup = InlineKeyboardMarkup([[key] for key in inline_keys])
        bot.editMessageText(msg, update.callback_query.message.chat.id, update.callback_query.message.message_id,
                            reply_markup=inline_markup)
    elif data['t'] == QueryType.GroupInfo.value:
        msg, inline_markup = generate_group_info(data['id'], session)
        bot.editMessageText(msg, update.callback_query.message.chat.id, update.callback_query.message.message_id,
                            reply_markup=inline_markup)
    elif data['t'] == QueryType.DelAdm.value:
        admin_user = session.query(User).filter_by(id=data['uid']).first()
        if admin_user:
            del_adm(bot, data['gid'], admin_user, session)
        msg, inline_markup = generate_group_info(data['gid'], session)
        bot.editMessageText(msg, update.callback_query.message.chat.id, update.callback_query.message.message_id,
                            reply_markup=inline_markup)
    elif data['t'] == QueryType.Order.value:
        order_text = chat_data['order']
        order_type = chat_data['order_type']
        order_pin = chat_data['pin'] if 'pin' in chat_data else True
        order_btn = chat_data['btn'] if 'btn' in chat_data else True
        if not data['g']:
            if order_btn:
                order = Order()
                order.text = order_text
                order.chat_id = data['id']
                order.date = datetime.now()
                msg = send_async(bot, chat_id=order.chat_id, text=MSG_ORDER_CLEARED_BY_HEADER + MSG_EMPTY).result()
                if msg:
                    order.confirmed_msg = msg.message_id
                else:
                    order.confirmed_msg = 0
                session.add(order)
                session.commit()
                markup = generate_ok_markup(order.id, 0)
                msg = send_order(bot, order.text, order_type, order.chat_id, markup).result().result()
            else:
                msg = send_order(bot, order_text, order_type, data['id'], None).result().result()
            if order_pin and msg:
                try:
                    bot.request.post(bot.base_url + '/pinChatMessage', {'chat_id': data['id'],
                                                                        'message_id': msg.message_id,
                                                                        'disable_notification': False})
                except TelegramError as err:
                    bot.logger.error(err.message)
        else:
            group = session.query(OrderGroup).filter_by(id=data['id']).first()
            for item in group.items:
                if order_btn:
                    order = Order()
                    order.text = order_text
                    order.chat_id = item.chat_id
                    order.date = datetime.now()
                    msg = send_async(bot, chat_id=order.chat_id, text=MSG_ORDER_CLEARED_BY_HEADER + MSG_EMPTY).result()
                    if msg:
                        order.confirmed_msg = msg.message_id
                    else:
                        order.confirmed_msg = 0
                    session.add(order)
                    session.commit()
                    markup = generate_ok_markup(order.id, 0)
                    msg = send_order(bot, order.text, order_type, order.chat_id, markup).result().result()
                else:
                    msg = send_order(bot, order_text, order_type, item.chat_id, None).result().result()
                if order_pin and msg:
                    try:
                        bot.request.post(bot.base_url + '/pinChatMessage',
                                         {'chat_id': item.chat_id, 'message_id': msg.message_id,
                                          'disable_notification': False})
                    except TelegramError as err:
                        bot.logger.error(err.message)
        update.callback_query.answer(text=MSG_ORDER_SENT)
    elif data['t'] == QueryType.OrderOk.value:
        order = session.query(Order).filter_by(id=data['id']).first()
        if order is not None:
            squad = session.query(Squad).filter_by(chat_id=order.chat_id).first()
            if squad is not None:
                squad_member = session.query(SquadMember).filter_by(squad_id=squad.chat_id,
                                                                    user_id=update.callback_query.from_user.id,
                                                                    approved=True).first()
                if squad_member is not None:
                    order_ok = session.query(OrderCleared).filter_by(order_id=data['id'],
                                                                     user_id=squad_member.user_id).first()
                    if order_ok is None and datetime.now() - order.date < timedelta(minutes=10):
                        order_ok = OrderCleared()
                        order_ok.order_id = data['id']
                        order_ok.user_id = update.callback_query.from_user.id
                        session.add(order_ok)
                        session.commit()
                        if order.confirmed_msg != 0:
                            if order.id not in order_updated or \
                                    datetime.now() - order_updated[order.id] > timedelta(seconds=4):
                                order_updated[order.id] = datetime.now()
                                job_queue.run_once(update_confirmed, 5, order)
                        update.callback_query.answer(text=MSG_ORDER_CLEARED)
                    else:
                        update.callback_query.answer(text=MSG_ORDER_CLEARED_ERROR)
                else:
                    update.callback_query.answer(text=MSG_ORDER_CLEARED_ERROR)
            else:
                order_ok = session.query(OrderCleared).filter_by(order_id=data['id'],
                                                                 user_id=update.callback_query.from_user.id).first()
                if order_ok is None and datetime.now() - order.date < timedelta(minutes=10):
                    order_ok = OrderCleared()
                    order_ok.order_id = data['id']
                    order_ok.user_id = update.callback_query.from_user.id
                    session.add(order_ok)
                    session.commit()
                    if order.confirmed_msg != 0:
                        if order.id not in order_updated or \
                                datetime.now() - order_updated[order.id] > timedelta(seconds=4):
                            order_updated[order.id] = datetime.now()
                            job_queue.run_once(update_confirmed, 5, order)
                    update.callback_query.answer(text=MSG_ORDER_CLEARED)
                else:
                    update.callback_query.answer(text=MSG_ORDER_CLEARED_ERROR)
    elif data['t'] == QueryType.Orders.value:
        chat_data['order_wait'] = False
        if 'txt' in data and len(data['txt']):
            if data['txt'] == Icons.LES.value:
                chat_data['order'] = Castle.LES.value
            elif data['txt'] == Icons.GORY.value:
                chat_data['order'] = Castle.GORY.value
            elif data['txt'] == Icons.SEA.value:
                chat_data['order'] = Castle.SEA.value
            else:
                chat_data['order'] = data['txt']
        markup = generate_order_chats_markup(session, chat_data['pin'] if 'pin' in chat_data else True,
                                             chat_data['btn'] if 'btn' in chat_data else True)
        bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.OrderGroup.value:
        chat_data['order_wait'] = False
        if 'txt' in data and len(data['txt']):
            chat_data['order_type'] = MessageType.TEXT
            if data['txt'] == Icons.LES.value:
                chat_data['order'] = Castle.LES.value
            elif data['txt'] == Icons.GORY.value:
                chat_data['order'] = Castle.GORY.value
            elif data['txt'] == Icons.SEA.value:
                chat_data['order'] = Castle.SEA.value
            else:
                chat_data['order'] = data['txt']
        admin_user = session.query(Admin).filter(Admin.user_id == update.callback_query.from_user.id).all()
        markup = generate_order_groups_markup(session, admin_user, chat_data['pin'] if 'pin' in chat_data else True,
                                              chat_data['btn'] if 'btn' in chat_data else True)
        bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.OrderGroupManage.value:
        group = session.query(OrderGroup).filter_by(id=data['id']).first()
        markup = generate_group_manage(data['id'], session)
        bot.editMessageText(MSG_ORDER_GROUP_CONFIG_HEADER.format(group.name),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.OrderGroupTriggerChat.value:
        group = session.query(OrderGroup).filter_by(id=data['id']).first()
        deleted = False
        for item in group.items:
            if item.chat_id == data['c']:
                session.delete(item)
                session.commit()
                deleted = True
        if not deleted:
            item = OrderGroupItem()
            item.group_id = group.id
            item.chat_id = data['c']
            session.add(item)
            session.commit()
        markup = generate_group_manage(data['id'], session)
        bot.editMessageText(MSG_ORDER_GROUP_CONFIG_HEADER.format(group.name),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.OrderGroupAdd.value:
        chat_data['wait_group_name'] = True
        send_async(bot, chat_id=update.callback_query.message.chat.id,
                   text=MSG_ORDER_GROUP_NEW)
    elif data['t'] == QueryType.OrderGroupDelete.value:
        group = session.query(OrderGroup).filter_by(id=data['id']).first()
        session.delete(group)
        session.commit()
        bot.editMessageText(MSG_ORDER_GROUP_LIST,
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=generate_groups_manage(session))
    elif data['t'] == QueryType.OrderGroupList.value:
        bot.editMessageText(MSG_ORDER_GROUP_LIST,
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=generate_groups_manage(session))
    elif data['t'] == QueryType.ShowEquip.value:
        user = session.query(User).filter_by(id=data['id']).first()
        update.callback_query.answer(text=MSG_CLEARED)
        back = data['b'] if 'b' in data else False
        bot.editMessageText('{}\n{} {}'.format(user.equip.equip, MSG_LAST_UPDATE, user.equip.date),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=generate_profile_buttons(user, back)
                            )
    elif data['t'] == QueryType.ShowStock.value:
        user = session.query(User).filter_by(id=data['id']).first()
        update.callback_query.answer(text=MSG_CLEARED)
        back = data['b'] if 'b' in data else False
        bot.editMessageText('{}\n{} {}'.
                            format(user.stock.stock, MSG_LAST_UPDATE, user.stock.date.strftime("%Y-%m-%d %H:%M:%S")),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=generate_profile_buttons(user, back)
                            )
    elif data['t'] == QueryType.ShowHero.value:
        user = session.query(User).filter_by(id=data['id']).first()
        update.callback_query.answer(text=MSG_CLEARED)
        back = data['b'] if 'b' in data else False
        bot.editMessageText(fill_char_template(MSG_PROFILE_SHOW_FORMAT,
                                               user, user.character),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=generate_profile_buttons(user, back)
                            )
    elif data['t'] == QueryType.MemberList.value:
        squad = session.query(Squad).filter_by(chat_id=data['id']).first()
        markup = generate_squad_members(squad.members, session)
        bot.editMessageText(squad.squad_name,
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.LeaveSquad.value:
        member = session.query(SquadMember).filter_by(user_id=data['id']).first()
        leave_squad(bot, user, member, update.effective_message, session)
    elif data['t'] == QueryType.RequestSquad.value:
        member = session.query(SquadMember).filter_by(user_id=update.callback_query.from_user.id).first()
        if member is None:
            member = SquadMember()
            member.user_id = update.callback_query.from_user.id
            member.squad_id = data['id']
            session.add(member)
            session.commit()
            admins = session.query(Admin).filter_by(admin_group=data['id']).all()
            usernames = ['@' + session.query(User).filter_by(id=admin.user_id).first().username for admin in admins]
            bot.editMessageText(MSG_SQUAD_REQUESTED.format(member.squad.squad_name, ', '.join(usernames)),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id, parse_mode=ParseMode.HTML)
            admins = session.query(Admin).filter_by(admin_group=member.squad.chat_id).all()
            for adm in admins:
                send_async(bot, chat_id=adm.user_id, text=MSG_SQUAD_REQUEST_NEW)
        else:
            markup = generate_leave_squad(user.id)
            bot.editMessageText(MSG_SQUAD_REQUEST_EXISTS,
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id,
                                reply_markup=markup)
    elif data['t'] == QueryType.RequestSquadAccept.value:
        member = session.query(SquadMember).filter_by(user_id=data['id'], approved=False).first()
        if member:
            member.approved = True
            session.add(member)
            session.commit()
            bot.editMessageText(MSG_SQUAD_REQUEST_ACCEPTED.format('@'+member.user.username),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id)
            admin = session.query(Admin).filter_by(user_id=member.user_id).all()
            is_admin = False
            for _ in admin:
                is_admin = True
                break
            send_async(bot, chat_id=member.user_id, text=MSG_SQUAD_REQUEST_ACCEPTED_ANSWER,
                       reply_markup=generate_user_markup(is_admin))
            send_async(bot, chat_id=member.squad_id, text=MSG_SQUAD_REQUEST_ACCEPTED.format('@'+member.user.username))
    elif data['t'] == QueryType.RequestSquadDecline.value:
        member = session.query(SquadMember).filter_by(user_id=data['id'], approved=False).first()
        if member:
            bot.editMessageText(MSG_SQUAD_REQUEST_DECLINED.format('@' + member.user.username),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id)
            session.delete(member)
            session.commit()
            send_async(bot, chat_id=member.user_id, text=MSG_SQUAD_REQUEST_DECLINED_ANSWER)
    elif data['t'] == QueryType.InviteSquadAccept.value:
        if update.callback_query.from_user.id != data['id']:
            update.callback_query.answer(text=MSG_GO_AWAY)
            return
        member = session.query(SquadMember).filter_by(user_id=data['id']).first()
        if member is None:
            member = SquadMember()
            member.user_id = user.id
            member.squad_id = update.callback_query.message.chat.id
            member.approved = True
            session.add(member)
            session.commit()
            bot.editMessageText(MSG_SQUAD_ADD_ACCEPTED.format('@'+user.username),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id)
    elif data['t'] == QueryType.InviteSquadDecline.value:
        if update.callback_query.from_user.id != data['id']:
            update.callback_query.answer(text=MSG_GO_AWAY)
            return
        user = session.query(User).filter_by(id=data['id']).first()
        bot.editMessageText(MSG_SQUAD_REQUEST_DECLINED.format('@' + user.username),
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id)
    elif data['t'] == QueryType.TriggerOrderPin.value:
        if 'pin' in chat_data:
            chat_data['pin'] = not chat_data['pin']
        else:
            chat_data['pin'] = False
        if data['g']:
            admin_user = session.query(Admin).filter(Admin.user_id == update.callback_query.from_user.id).all()
            markup = generate_order_groups_markup(session, admin_user, chat_data['pin'] if 'pin' in chat_data else True,
                                                  chat_data['btn'] if 'btn' in chat_data else True)
            bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id,
                                reply_markup=markup)
        else:
            markup = generate_order_chats_markup(session, chat_data['pin'] if 'pin' in chat_data else True,
                                                 chat_data['btn'] if 'btn' in chat_data else True)
            bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id,
                                reply_markup=markup)
    elif data['t'] == QueryType.TriggerOrderButton.value:
        if 'btn' in chat_data:
            chat_data['btn'] = not chat_data['btn']
        else:
            chat_data['btn'] = False
        if data['g']:
            admin_user = session.query(Admin).filter(Admin.user_id == update.callback_query.from_user.id).all()
            markup = generate_order_groups_markup(session, admin_user, chat_data['pin'] if 'pin' in chat_data else True,
                                                  chat_data['btn'] if 'btn' in chat_data else True)
            bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id,
                                reply_markup=markup)
        else:
            markup = generate_order_chats_markup(session, chat_data['pin'] if 'pin' in chat_data else True,
                                                 chat_data['btn'] if 'btn' in chat_data else True)
            bot.editMessageText(MSG_ORDER_SEND_HEADER.format(chat_data['order']),
                                update.callback_query.message.chat.id,
                                update.callback_query.message.message_id,
                                reply_markup=markup)
    elif data['t'] == QueryType.SquadList.value:
        admin = session.query(Admin).filter_by(user_id=update.callback_query.from_user.id).all()
        global_adm = False
        for adm in admin:
            if adm.admin_type <= AdminType.FULL.value:
                global_adm = True
                break
        if global_adm:
            squads = session.query(Squad).all()
        else:
            group_ids = []
            for adm in admin:
                group_ids.append(adm.admin_group)
            squads = session.query(Squad).filter(Squad.chat_id in group_ids).all()
        markup = generate_squad_list(squads, session)
        bot.editMessageText(MSG_SQUAD_LIST,
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id,
                            reply_markup=markup)
    elif data['t'] == QueryType.GroupDelete.value:
        squad = session.query(Squad).filter_by(chat_id=data['gid']).first()
        if squad is not None:
            for member in squad.members:
                session.delete(member)
            session.delete(squad)
            session.commit()
            send_async(bot, chat_id=data['gid'], text=MSG_SQUAD_DELETE)
        msg = MSG_GROUP_STATUS_CHOOSE_CHAT
        squads = session.query(Squad).all()
        inline_keys = []
        for squad in squads:
            inline_keys.append(InlineKeyboardButton(squad.squad_name,
                                                    callback_data=json.dumps({'t': QueryType.GroupInfo.value,
                                                                              'id': squad.chat_id})))
        inline_markup = InlineKeyboardMarkup([[key] for key in inline_keys])
        bot.editMessageText(msg, update.callback_query.message.chat.id, update.callback_query.message.message_id,
                            reply_markup=inline_markup)
    elif data['t'] == QueryType.OtherReport.value:
        squad = session.query(Squad).filter(Squad.chat_id == data['c']).first()
        time_from = datetime.fromtimestamp(data['ts'])
        time_to = time_from + timedelta(hours=4)
        reports = session.query(User, Report) \
            .join(SquadMember) \
            .outerjoin(Report, and_(User.id == Report.user_id, Report.date > time_from, Report.date < time_to)) \
            .filter(SquadMember.squad_id == data['c']).order_by(Report.date.desc()).all()
        text = ''
        full_def = 0
        full_atk = 0
        full_exp = 0
        full_gold = 0
        full_stock = 0
        for user, report in reports:
            if report:
                text += MSG_REPORT_SUMMARY_ROW.format(
                    report.name, user.username, report.attack, report.defence,
                    report.earned_exp, report.earned_gold, report.earned_stock)
                full_atk += report.attack
                full_def += report.defence
                full_exp += report.earned_exp
                full_gold += report.earned_gold
                full_stock += report.earned_stock
            else:
                text += MSG_REPORT_SUMMARY_ROW_EMPTY.format(user.character.name, user.username)
        text = MSG_REPORT_SUMMARY_HEADER.format(squad.squad_name, time_from.strftime('%d-%m-%Y %H:%M'), full_atk, full_def,
                                        full_exp, full_gold, full_stock) + text
        markup = generate_other_reports(time_from, squad.chat_id)
        bot.editMessageText(text, update.callback_query.message.chat.id, update.callback_query.message.message_id,
                            parse_mode=ParseMode.HTML, reply_markup=markup)
    elif data['t'] == QueryType.GlobalBuildTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        global_build_top(bot, update)
    elif data['t'] == QueryType.WeekBuildTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        week_build_top(bot, update)
    elif data['t'] == QueryType.SquadGlobalBuildTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        global_squad_build_top(bot, update)
    elif data['t'] == QueryType.SquadWeekBuildTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        week_squad_build_top(bot, update)
    elif data['t'] == QueryType.BattleGlobalTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        global_battle_top(bot, update)
    elif data['t'] == QueryType.BattleWeekTop.value:
        update.callback_query.answer(text=MSG_TOP_GENERATING)
        week_battle_top(bot, update)
    elif data['t'] == QueryType.Yes.value:
        leave_squad(bot, user, user.member, update.effective_message, session)
    elif data['t'] == QueryType.No.value:
        bot.editMessageText(MSG_SQUAD_LEAVE_DECLINE,
                            update.callback_query.message.chat.id,
                            update.callback_query.message.message_id)
