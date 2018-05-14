from datetime import datetime

from sqlalchemy import or_, and_
from telegram import Update, Bot, ParseMode, TelegramError

from core.functions.reply_markup import generate_squad_markup
from core.template import fill_char_template
from core.types import User, AdminType, Admin, admin_allowed, Group, Squad, SquadMember, user_allowed, Report, Character
from core.utils import send_async, ping_users
from core.functions.inline_markup import generate_squad_list, generate_leave_squad, generate_squad_request, \
    generate_other_reports, generate_squad_request_answer, generate_squad_invite_answer, generate_fire_up, \
    generate_yes_no
from core.texts import *
from core.constants import *


@user_allowed
def squad_about(bot: Bot, update: Update, session):
    admin = session.query(Admin).filter(Admin.user_id == update.message.from_user.id,
                                        Admin.admin_group != 0).first()
    squad_member = session.query(SquadMember).filter_by(user_id=update.message.from_user.id, approved=True).first()
    markup = generate_squad_markup(is_group_admin=admin is not None, in_squad=True if squad_member else False)
    send_async(bot,
               chat_id=update.message.chat.id,
               text=MSG_SQUAD_ABOUT,
               reply_markup=markup)


@admin_allowed()
def add_squad(bot: Bot, update: Update, session):
    if update.message.chat.type == 'supergroup':
        squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
        if squad is None:
            squad = Squad()
            squad.chat_id = update.message.chat.id
            squad.thorns_enabled = False
            msg = update.message.text.split(' ', 1)
            if len(msg) == 2:
                squad.squad_name = msg[1]
            else:
                group = session.query(Group).filter_by(id=update.message.chat.id).first()
                squad.squad_name = group.title
            session.add(squad)
            session.commit()
            send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_NEW.format(squad.squad_name),
                       parse_mode=ParseMode.HTML)


@admin_allowed()
def set_invite_link(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if update.message.chat.type == 'supergroup' and squad is not None:
        msg = update.message.text.split(' ', 1)
        if len(msg) == 2:
            squad.invite_link = msg[1]
            session.add(squad)
            session.commit()
            send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_LINK_SAVED)


@admin_allowed()
def set_squad_name(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if update.message.chat.type == 'supergroup' and squad is not None:
        msg = update.message.text.split(' ', 1)
        if len(msg) == 2:
            squad.squad_name = msg[1]
            session.add(squad)
            session.commit()
            send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_RENAMED.format(squad.squad_name),
                       parse_mode=ParseMode.HTML)


@admin_allowed()
def del_squad(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if update.message.chat.type == 'supergroup' and squad is not None:
        for member in squad.members:
            session.delete(member)
        for order_group_item in squad.chat.group_items:
            session.delete(order_group_item)
        session.delete(squad)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_DELETE)


@admin_allowed(AdminType.GROUP)
def enable_thorns(bot: Bot, update: Update, session):
    group = session.query(Group).filter_by(id=update.message.chat.id).first()
    if update.message.chat.type == 'supergroup' and group is not None and len(group.squad) == 1:
        group.squad[0].thorns_enabled = True
        session.add(group.squad[0])
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_THORNS_ENABLED)


@admin_allowed(AdminType.GROUP)
def disable_thorns(bot: Bot, update: Update, session):
    group = session.query(Group).filter_by(id=update.message.chat.id).first()
    if update.message.chat.type == 'supergroup' and group is not None and len(group.squad) == 1:
        group.squad[0].thorns_enabled = False
        session.add(group.squad[0])
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_THORNS_DISABLED)


@admin_allowed(AdminType.GROUP)
def squad_list(bot: Bot, update: Update, session):
    admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
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
        squads = session.query(Squad).filter(Squad.chat_id.in_(group_ids)).all()
    markup = generate_squad_list(squads, session)
    send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_LIST, reply_markup=markup)


@user_allowed
def squad_request(bot: Bot, update: Update, session):
    user = session.query(User).filter_by(id=update.message.from_user.id).first()
    if user is not None:
        if user.username is None:
            send_async(bot, chat_id=update.message.chat.id, text=MSG_NO_USERNAME)
        elif user.character:
            if user.member:
                markup = generate_leave_squad(user.id)
                send_async(bot, chat_id=update.message.chat.id,
                           text=MSG_SQUAD_REQUEST_EXISTS, reply_markup=markup)
            else:
                if user.character.level < MINIMUM_SQUAD_MEMBER_LEVEL:
                    send_async(bot, chat_id=update.message.chat.id,
                               text=MSG_SQUAD_LEVEL_TOO_LOW.format(MINIMUM_SQUAD_MEMBER_LEVEL))
                else:
                    markup = generate_squad_request(session)
                    send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_REQUEST, reply_markup=markup)
        else:
            send_async(bot, chat_id=update.message.chat.id, text=MSG_NO_PROFILE_IN_BOT)


@admin_allowed(AdminType.GROUP)
def list_squad_requests(bot: Bot, update: Update, session):
    admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
    group_admin = []
    for adm in admin:
        if adm.admin_type == AdminType.GROUP.value and adm.admin_group != 0:
            group_admin.append(adm)
    count = 0
    for adm in group_admin:
        members = session.query(SquadMember).filter_by(squad_id=adm.admin_group, approved=False)
        for member in members:
            count += 1
            markup = generate_squad_request_answer(member.user_id)
            send_async(bot, chat_id=update.message.chat.id,
                       text=fill_char_template(MSG_PROFILE_SHOW_FORMAT, member.user, member.user.character, True),
                       reply_markup=markup)
    if count == 0:
        send_async(bot, chat_id=update.message.chat.id,
                   text=MSG_SQUAD_REQUEST_EMPTY)


@admin_allowed(AdminType.GROUP)
def open_hiring(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if squad is not None:
        squad.hiring = True
        session.add(squad)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_RECRUITING_ENABLED)


@admin_allowed(AdminType.GROUP)
def close_hiring(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if squad is not None:
        squad.hiring = False
        session.add(squad)
        session.commit()
        send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_RECRUITING_DISABLED)


@admin_allowed(AdminType.GROUP)
def remove_from_squad(bot: Bot, update: Update, session):
    admin = session.query(Admin).filter_by(user_id=update.message.from_user.id).all()
    group_admin = []
    for adm in admin:
        squad = session.query(Squad).filter_by(chat_id=adm.admin_group).first()
        if squad is not None:
            group_admin.append(adm)
    for adm in group_admin:
        members = session.query(SquadMember).filter_by(squad_id=adm.admin_group, approved=True).all()
        markup = generate_fire_up(members)
        squad = session.query(Squad).filter_by(chat_id=adm.admin_group).first()
        send_async(bot, chat_id=update.message.chat.id,
                   text=MSG_SQUAD_CLEAN.format(squad.squad_name),
                   reply_markup=markup, parse_mode=ParseMode.HTML)


@user_allowed
def leave_squad_request(bot: Bot, update: Update, session):
    member = session.query(SquadMember).filter_by(user_id=update.message.from_user.id).first()
    user = session.query(User).filter_by(id=update.message.from_user.id).first()
    if member:
        squad = member.squad
        markup = generate_yes_no(user_id=user.id)
        send_async(bot, chat_id=member.user_id,
                   text=MSG_SQUAD_LEAVE_ASK.format(user.character.name, squad.squad_name), parse_mode=ParseMode.HTML,
                   reply_markup=markup)
    else:
        send_async(bot, chat_id=user.id,
                   text=MSG_SQUAD_NONE, parse_mode=ParseMode.HTML)


def leave_squad(bot: Bot, user: User, member: SquadMember, message, session):
    if member:
        squad = session.query(Squad).filter(Squad.chat_id == member.squad_id).first()
        member_user = session.query(User).filter(User.id == member.user_id).first()
        session.delete(member)
        session.commit()
        if member.approved:
            admins = session.query(Admin).filter_by(admin_group=squad.chat_id).all()
            for adm in admins:
                if adm.user_id != user.id:
                    send_async(bot, chat_id=adm.user_id,
                               text=MSG_SQUAD_LEAVED.format(member_user.character.name, squad.squad_name),
                               parse_mode=ParseMode.HTML)
            send_async(bot, chat_id=member.squad_id,
                       text=MSG_SQUAD_LEAVED.format(member_user.character.name, squad.squad_name),
                       parse_mode=ParseMode.HTML)
        try:
            bot.kick_chat_member(squad.chat_id, member.user_id)
        except TelegramError as err:
            bot.logger.error(err.message)

        if member.user_id == user.id:
            bot.editMessageText(MSG_SQUAD_LEAVED.format(member_user.character.name, squad.squad_name),
                                message.chat.id,
                                message.message_id, parse_mode=ParseMode.HTML)
        else:
            send_async(bot, chat_id=member.user_id,
                       text=MSG_SQUAD_LEAVED.format(member_user.character.name, squad.squad_name),
                       parse_mode=ParseMode.HTML)
            members = session.query(SquadMember).filter_by(squad_id=member.squad_id, approved=True).all()
            bot.editMessageText(message.text,
                                message.chat.id,
                                message.message_id,
                                reply_markup=generate_fire_up(members))
    else:
        send_async(bot, chat_id=user.id, text=MSG_SQUAD_ALREADY_DELETED)


@admin_allowed(AdminType.GROUP)
def add_to_squad(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if squad is not None:
        username = update.message.text.split(' ', 1)
        if len(username) == 2:
            username = username[1].replace('@', '')
            user = session.query(User).filter_by(username=username).first()
            if user is not None:
                if user.character is None:
                    send_async(bot, chat_id=update.message.chat.id, text=MSG_SQUAD_NO_PROFILE)
                elif user.member is not None:
                    send_async(bot, chat_id=update.message.chat.id,
                               text=MSG_SQUAD_ADD_IN_SQUAD.format('@' + username))
                else:
                    markup = generate_squad_invite_answer(user.id)
                    send_async(bot, chat_id=update.message.chat.id,
                               text=MSG_SQUAD_ADD.format('@' + username),
                               reply_markup=markup)


@admin_allowed(AdminType.GROUP)
def call_squad(bot: Bot, update: Update, session):
    squad = session.query(Squad).filter_by(chat_id=update.message.chat.id).first()
    if squad is not None:
        users = session.query(User).join(SquadMember).filter(User.id == SquadMember.user_id)\
            .filter(SquadMember.squad_id == squad.chat_id).all()
        msg = MSG_SQUAD_CALL_HEADER
        send_async(bot, chat_id=update.message.chat.id, text=msg)
        ping_users(bot, users, update.message.chat.id)


@admin_allowed(AdminType.GROUP)
def battle_reports_show(bot: Bot, update: Update, session):
    admin = session.query(Admin, Squad).filter(Admin.user_id == update.message.from_user.id,
                                               Squad.chat_id == Admin.admin_group).all()
    group_admin = []
    for adm, squad in admin:
        if squad is not None:
            group_admin.append([adm, squad])
    for adm, squad in group_admin:
        now = datetime.now()
        time_from = datetime(now.year, now.month,
                             now.day, int(now.hour / 4) * 4, 0, 0)
        reports = session.query(User, Report) \
            .join(SquadMember) \
            .outerjoin(Report, and_(User.id == Report.user_id, Report.date > time_from)) \
            .filter(SquadMember.squad_id == adm.admin_group).order_by(Report.date.desc()).all()
        text = ''
        full_def = 0
        full_atk = 0
        full_exp = 0
        full_gold = 0
        full_stock = 0
        total_reports = 0
        total_members = 0
        for user, report in reports:
            total_members += 1
            if report:
                text += MSG_REPORT_SUMMARY_ROW.format(
                    report.name, user.username, report.attack, report.defence,
                    report.earned_exp, report.earned_gold, report.earned_stock)
                full_atk += report.attack
                full_def += report.defence
                full_exp += report.earned_exp
                full_gold += report.earned_gold
                full_stock += report.earned_stock
                total_reports += 1
            else:
                text += MSG_REPORT_SUMMARY_ROW_EMPTY.format(user.character.name, user.username)
        text = MSG_REPORT_SUMMARY_HEADER.format(squad.squad_name, time_from.strftime('%d-%m-%Y %H:%M'), total_reports,
                                                total_members, full_atk, full_def, full_exp, full_gold,
                                                full_stock) + text
        markup = generate_other_reports(time_from, squad.chat_id)
        send_async(bot, chat_id=update.message.chat.id, text=text, parse_mode=ParseMode.HTML, reply_markup=markup)
