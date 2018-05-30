import json
from datetime import datetime, timedelta, date
from enum import Enum

from sqlalchemy import func, tuple_
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import CASTLE
from core.constants import BATTLE_TIMES
from core.enums import Castle, Icons
from core.texts import MSG_GROUP_STATUS_ADMIN_FORMAT, MSG_GROUP_STATUS_DEL_ADMIN, MSG_GROUP_STATUS, MSG_ON, MSG_OFF, \
    MSG_ORDER_GROUP_DEL, MSG_BACK, MSG_ORDER_PIN, MSG_ORDER_NO_PIN, MSG_ORDER_BUTTON, MSG_ORDER_NO_BUTTON, \
    MSG_ORDER_TO_SQUADS, MSG_ORDER_ACCEPT, MSG_ORDER_GROUP_ADD, MSG_SYMBOL_ON, MSG_SYMBOL_OFF, \
    MSG_SQUAD_GREEN_INLINE_BUTTON, MSG_SQUAD_RED_INLINE_BUTTON, BTN_HERO, BTN_STOCK, BTN_EQUIPMENT, BTN_YES, BTN_NO, \
    BTN_LEAVE, BTN_ACCEPT, BTN_DECLINE, BTN_WEEK, BTN_ALL_TIME, BTN_SQUAD_WEEK, BTN_SQUAD_ALL_TIME
from core.types import Group, Admin, User, Squad, AdminType, OrderGroup, Character


class QueryType(Enum):
    GroupList = 0
    GroupInfo = 1
    DelAdm = 2
    Order = 3
    OrderOk = 4
    Orders = 5
    OrderGroup = 6
    OrderGroupManage = 7
    OrderGroupTriggerChat = 8
    OrderGroupAdd = 9
    OrderGroupDelete = 10
    OrderGroupList = 11
    ShowStock = 12
    ShowEquip = 13
    ShowHero = 14
    MemberList = 15
    LeaveSquad = 16
    RequestSquad = 17
    RequestSquadAccept = 18
    RequestSquadDecline = 19
    InviteSquadAccept = 20
    InviteSquadDecline = 21
    TriggerOrderPin = 22
    SquadList = 23
    GroupDelete = 24
    TriggerOrderButton = 25
    OtherReport = 26
    GlobalBuildTop = 27
    WeekBuildTop = 28
    SquadGlobalBuildTop = 29
    SquadWeekBuildTop = 30
    BattleGlobalTop = 31
    BattleWeekTop = 32
    Yes = 100
    No = 200


def generate_group_info(group_id, session):
    group = session.query(Group).filter(Group.id == group_id).first()
    admins = session.query(Admin).filter(Admin.admin_group == group_id).all()
    adm_msg = ''
    adm_del_keys = []
    for adm in admins:
        user = session.query(User).filter_by(id=adm.user_id).first()
        adm_msg += MSG_GROUP_STATUS_ADMIN_FORMAT. \
            format(user.id, user.username or '', user.first_name or '', user.last_name or '')
        adm_del_keys.append([InlineKeyboardButton(MSG_GROUP_STATUS_DEL_ADMIN.
                                                  format(user.first_name or '', user.last_name or ''),
                                                  callback_data=json.dumps(
                                                      {'t': QueryType.DelAdm.value, 'uid': user.id,
                                                       'gid': group_id}))])
    msg = MSG_GROUP_STATUS.format(group.title,
                                  adm_msg,
                                  MSG_ON if group.welcome_enabled else MSG_OFF,
                                  MSG_ON if group.allow_trigger_all else MSG_OFF,
                                  MSG_ON if len(group.squad) and group.squad[0].thorns_enabled else MSG_OFF)
    adm_del_keys.append([InlineKeyboardButton(MSG_ORDER_GROUP_DEL, callback_data=json.dumps(
        {'t': QueryType.GroupDelete.value, 'gid': group_id}))])
    adm_del_keys.append([InlineKeyboardButton(MSG_BACK, callback_data=json.dumps(
        {'t': QueryType.GroupList.value}))])
    inline_markup = InlineKeyboardMarkup(adm_del_keys)
    return msg, inline_markup


def generate_flag_orders():
    flag_btns = [InlineKeyboardButton(Castle.BLACK.value, callback_data=json.dumps(
        {'t': QueryType.OrderGroup.value, 'txt': Castle.BLACK.value})),
                 InlineKeyboardButton(Castle.WHITE.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.WHITE.value})),
                 InlineKeyboardButton(Castle.BLUE.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.BLUE.value})),
                 InlineKeyboardButton(Castle.YELLOW.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.YELLOW.value})),
                 InlineKeyboardButton(Castle.RED.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.RED.value})),
                 InlineKeyboardButton(Castle.DUSK.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.DUSK.value})),
                 InlineKeyboardButton(Castle.MINT.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Castle.MINT.value})),
                 InlineKeyboardButton(Castle.GORY.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Icons.GORY.value})),
                 InlineKeyboardButton(Castle.LES.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Icons.LES.value})),
                 InlineKeyboardButton(Castle.SEA.value, callback_data=json.dumps(
                     {'t': QueryType.OrderGroup.value, 'txt': Icons.SEA.value}))]
    btns = []
    i = 0
    for btn in flag_btns:
        if CASTLE:
            if btn.text == CASTLE:
                continue
        if i % 3 == 0:
            btns.append([])
        btns[-1].append(btn)
        i += 1

    if CASTLE:
        btns.append([])
        for btn in flag_btns:
            if btn.text == CASTLE:
                btns[-1].append(btn)

    inline_markup = InlineKeyboardMarkup(btns)
    return inline_markup


def generate_order_chats_markup(session, pin=True, btn=True):
    squads = session.query(Squad).all()
    inline_keys = []
    for squad in squads:
        inline_keys.append([InlineKeyboardButton(squad.squad_name, callback_data=json.dumps(
            {'t': QueryType.Order.value, 'g': False, 'id': squad.chat_id}))])
    inline_keys.append([InlineKeyboardButton(MSG_ORDER_PIN if pin else MSG_ORDER_NO_PIN, callback_data=json.dumps(
        {'t': QueryType.TriggerOrderPin.value, 'g': False}))])
    inline_keys.append([InlineKeyboardButton(MSG_ORDER_BUTTON if btn else MSG_ORDER_NO_BUTTON, callback_data=json.dumps(
        {'t': QueryType.TriggerOrderButton.value, 'g': False}))])
    inline_markup = InlineKeyboardMarkup(inline_keys)
    return inline_markup


def generate_order_groups_markup(session, admin_user: list = None, pin: bool = True, btn=True):
    if admin_user:
        group_adm = True
        for adm in admin_user:
            if adm.admin_type < AdminType.GROUP.value:
                group_adm = False
                break
        if group_adm:
            inline_keys = []
            for adm in admin_user:
                group = session.query(Group).filter_by(id=adm.admin_group, bot_in_group=True).first()
                if group:
                    inline_keys.append([InlineKeyboardButton(group.title, callback_data=json.dumps(
                        {'t': QueryType.Order.value, 'g': False, 'id': group.id}))])
            inline_keys.append(
                [InlineKeyboardButton(MSG_ORDER_PIN if pin else MSG_ORDER_NO_PIN, callback_data=json.dumps(
                    {'t': QueryType.TriggerOrderPin.value, 'g': True}))])
            inline_keys.append(
                [InlineKeyboardButton(MSG_ORDER_BUTTON if btn else MSG_ORDER_NO_BUTTON, callback_data=json.dumps(
                    {'t': QueryType.TriggerOrderButton.value, 'g': True}))])
            inline_markup = InlineKeyboardMarkup(inline_keys)
            return inline_markup
        else:
            groups = session.query(OrderGroup).all()
            inline_keys = []
            for group in groups:
                inline_keys.append([InlineKeyboardButton(group.name, callback_data=json.dumps(
                    {'t': QueryType.Order.value, 'g': True, 'id': group.id}))])
            inline_keys.append([InlineKeyboardButton(MSG_ORDER_TO_SQUADS, callback_data=json.dumps(
                {'t': QueryType.Orders.value}))])
            inline_keys.append([InlineKeyboardButton(MSG_ORDER_PIN if pin else MSG_ORDER_NO_PIN,
                                                     callback_data=json.dumps(
                                                         {'t': QueryType.TriggerOrderPin.value, 'g': True}))])
            inline_keys.append([InlineKeyboardButton(MSG_ORDER_BUTTON if btn else MSG_ORDER_NO_BUTTON,
                                                     callback_data=json.dumps(
                                                         {'t': QueryType.TriggerOrderButton.value, 'g': True}))])
            inline_markup = InlineKeyboardMarkup(inline_keys)
            return inline_markup


def generate_ok_markup(order_id, count):
    inline_markup = InlineKeyboardMarkup([[InlineKeyboardButton(MSG_ORDER_ACCEPT.format(count),
                                                                callback_data=json.dumps(
                                                                    {'t': QueryType.OrderOk.value, 'id': order_id}))]])
    return inline_markup


def generate_groups_manage(session):
    groups = session.query(OrderGroup).all()
    inline_keys = []
    for group in groups:
        inline_keys.append([InlineKeyboardButton(group.name, callback_data=json.dumps(
            {'t': QueryType.OrderGroupManage.value, 'id': group.id}))])
    inline_keys.append([InlineKeyboardButton(MSG_ORDER_GROUP_ADD, callback_data=json.dumps(
        {'t': QueryType.OrderGroupAdd.value}))])
    return InlineKeyboardMarkup(inline_keys)


def generate_group_manage(group_id, session):
    squads = session.query(Squad).all()
    inline_keys = []
    for squad in squads:
        in_group = False
        for item in squad.chat.group_items:
            if item.group_id == group_id:
                in_group = True
                break
        inline_keys.append([InlineKeyboardButton((MSG_SYMBOL_ON if in_group else MSG_SYMBOL_OFF) +
                                                 squad.squad_name, callback_data=json.dumps(
            {'t': QueryType.OrderGroupTriggerChat.value, 'id': group_id, 'c': squad.chat_id}))])
    inline_keys.append([InlineKeyboardButton(MSG_ORDER_GROUP_DEL, callback_data=json.dumps(
        {'t': QueryType.OrderGroupDelete.value, 'id': group_id}))])
    inline_keys.append([InlineKeyboardButton(MSG_BACK, callback_data=json.dumps(
        {'t': QueryType.OrderGroupList.value}))])
    return InlineKeyboardMarkup(inline_keys)


def generate_profile_buttons(user, back_key=False):
    inline_keys = [[InlineKeyboardButton(BTN_HERO, callback_data=json.dumps(
        {'t': QueryType.ShowHero.value, 'id': user.id, 'b': back_key}))]]
    if user.stock:
        inline_keys.append([InlineKeyboardButton(BTN_STOCK, callback_data=json.dumps(
            {'t': QueryType.ShowStock.value, 'id': user.id, 'b': back_key}))])
    if user.equip:
        inline_keys.append([InlineKeyboardButton(BTN_EQUIPMENT, callback_data=json.dumps(
            {'t': QueryType.ShowEquip.value, 'id': user.id, 'b': back_key}))])
    if back_key:
        inline_keys.append(
            [InlineKeyboardButton(MSG_BACK,
                                  callback_data=json.dumps(
                                      {'t': QueryType.MemberList.value, 'id': user.member.squad_id}
                                  ))])
    return InlineKeyboardMarkup(inline_keys)


def generate_squad_list_key(squad, session):
    attack = 0
    defence = 0
    level = 0
    members = squad.members
    user_ids = []
    for member in members:
        user_ids.append(member.user_id)
    actual_profiles = session.query(Character.user_id, func.max(Character.date)). \
        filter(Character.user_id.in_(user_ids)). \
        group_by(Character.user_id).all()
    characters = session.query(Character).filter(tuple_(Character.user_id, Character.date)
                                                 .in_([(a[0], a[1]) for a in actual_profiles])).all()
    for character in characters:
        attack += character.attack
        defence += character.defence
        level += character.level
    return [InlineKeyboardButton(
        '{} : {}⚔ {}🛡 {}👥 {}🏅'.format(
            squad.squad_name,
            attack,
            defence,
            len(members),
            int(level / (len(members) or 1))
        ),
        callback_data=json.dumps({'t': QueryType.MemberList.value, 'id': squad.chat_id}))]


def generate_yes_no(user_id):
    inline_keys = [InlineKeyboardButton(BTN_YES,
                                        callback_data=json.dumps(
                                            {'t': QueryType.Yes.value, 'id': user_id})),
                   InlineKeyboardButton(BTN_NO,
                                        callback_data=json.dumps(
                                            {'t': QueryType.No.value, 'id': user_id}))]
    return InlineKeyboardMarkup([inline_keys])


def generate_squad_list(squads, session):
    inline_keys = []
    for squad in squads:
        inline_keys.append(generate_squad_list_key(squad, session))
    return InlineKeyboardMarkup(inline_keys)


def generate_leave_squad(user_id):
    inline_keys = [[InlineKeyboardButton(BTN_LEAVE,
                                         callback_data=json.dumps({'t': QueryType.LeaveSquad.value,
                                                                   'id': user_id}))]]
    return InlineKeyboardMarkup(inline_keys)


def generate_squad_request(session):
    inline_keys = []
    squads = session.query(Squad).filter_by(hiring=True).all()
    for squad in squads:
        inline_keys.append([InlineKeyboardButton(squad.squad_name,
                                                 callback_data=json.dumps(
                                                     {'t': QueryType.RequestSquad.value, 'id': squad.chat_id}))])
    return InlineKeyboardMarkup(inline_keys)


def generate_other_reports(battletime: datetime, squad_id):
    battletime_time = battletime.time()
    prev_battletime = battletime
    next_battletime = battletime
    for i in range(len(BATTLE_TIMES)):
        if battletime_time == BATTLE_TIMES[i]:
            prev_battletime = datetime(battletime.year, battletime.month,
                                       battletime.day - 1 if i == 0 else 0,
                                       BATTLE_TIMES[i - 1].seconds/3600)
            next_battletime = datetime(battletime.year, battletime.month,
                                       battletime.day + 1 if i == len(BATTLE_TIMES) - 1 else 0,
                                       BATTLE_TIMES[(i + 1) if i == len(BATTLE_TIMES) - 1 else 0].seconds/3600)
    inline_keys = [[InlineKeyboardButton('<< ' + prev_battletime.strftime('%d-%m-%Y %H:%M'),
                                         callback_data=json.dumps(
                                             {'t': QueryType.OtherReport.value,
                                              'ts': prev_battletime.timestamp(),
                                              'c': squad_id}))]]
    if next_battletime < datetime.now():
        inline_keys[0].append(InlineKeyboardButton(next_battletime.strftime('%d-%m-%Y %H:%M') + ' >>',
                                                   callback_data=json.dumps(
                                                       {'t': QueryType.OtherReport.value,
                                                        'ts': next_battletime.timestamp(),
                                                        'c': squad_id})))
    return InlineKeyboardMarkup(inline_keys)


def generate_squad_members(members, session):
    inline_keys = []
    user_ids = []
    for member in members:
        user_ids.append(member.user_id)
    actual_profiles = session.query(Character.user_id, func.max(Character.date)). \
        filter(Character.user_id.in_(user_ids)). \
        group_by(Character.user_id).all()
    characters = session.query(Character).filter(tuple_(Character.user_id, Character.date)
                                                 .in_([(a[0], a[1]) for a in actual_profiles])) \
        .order_by(Character.level.desc()).all()
    for character in characters:
        time_passed = datetime.now() - character.date
        status_emoji = '❇'
        if time_passed > timedelta(days=7):
            status_emoji = '⁉'
        elif time_passed > timedelta(days=4):
            status_emoji = '‼'
        elif time_passed > timedelta(days=3):
            status_emoji = '❗'
        elif time_passed < timedelta(days=1):
            status_emoji = '🕐'
        inline_keys.append(
            [InlineKeyboardButton('{}{}: {}⚔ {}🛡 {}🏅'.
                                  format(status_emoji,
                                         character.name,
                                         character.attack,
                                         character.defence,
                                         character.level),
                                  callback_data=json.dumps(
                                      {'t': QueryType.ShowHero.value,
                                       'id': character.user_id,
                                       'b': True}
                                  ))])
    inline_keys.append(
        [InlineKeyboardButton(MSG_BACK,
                              callback_data=json.dumps(
                                  {'t': QueryType.SquadList.value}
                              ))])
    return InlineKeyboardMarkup(inline_keys)


def generate_squad_request_answer(user_id):
    inline_keys = [InlineKeyboardButton(BTN_ACCEPT,
                                        callback_data=json.dumps(
                                            {'t': QueryType.RequestSquadAccept.value, 'id': user_id})),
                   InlineKeyboardButton(BTN_DECLINE,
                                        callback_data=json.dumps(
                                            {'t': QueryType.RequestSquadDecline.value, 'id': user_id}))]
    return InlineKeyboardMarkup([inline_keys])


def generate_squad_invite_answer(user_id):
    inline_keys = [InlineKeyboardButton(MSG_SQUAD_GREEN_INLINE_BUTTON,
                                        callback_data=json.dumps(
                                            {'t': QueryType.InviteSquadAccept.value, 'id': user_id})),
                   InlineKeyboardButton(MSG_SQUAD_RED_INLINE_BUTTON,
                                        callback_data=json.dumps(
                                            {'t': QueryType.InviteSquadDecline.value, 'id': user_id}))]
    return InlineKeyboardMarkup([inline_keys])


def generate_fire_up(members):
    inline_keys = []
    for member in members:
        inline_keys.append([InlineKeyboardButton('🔥{}: {}⚔ {}🛡'.format(member.user, member.user.character.attack,
                                                                         member.user.character.defence),
                                                 callback_data=json.dumps(
                                                     {'t': QueryType.LeaveSquad.value, 'id': member.user_id}))])
    return InlineKeyboardMarkup(inline_keys)


def generate_build_top():
    inline_keys = [[InlineKeyboardButton(BTN_WEEK,
                                         callback_data=json.dumps(
                                             {'t': QueryType.WeekBuildTop.value})),
                    InlineKeyboardButton(BTN_ALL_TIME,
                                         callback_data=json.dumps(
                                             {'t': QueryType.GlobalBuildTop.value}))],
                   [InlineKeyboardButton(BTN_SQUAD_WEEK,
                                         callback_data=json.dumps(
                                             {'t': QueryType.SquadWeekBuildTop.value})),
                    InlineKeyboardButton(BTN_SQUAD_ALL_TIME,
                                         callback_data=json.dumps(
                                             {'t': QueryType.SquadGlobalBuildTop.value}))]]
    return InlineKeyboardMarkup(inline_keys)


def generate_battle_top():
    inline_keys = [[InlineKeyboardButton(BTN_WEEK,
                                         callback_data=json.dumps(
                                             {'t': QueryType.BattleWeekTop.value})),
                    InlineKeyboardButton(BTN_ALL_TIME,
                                         callback_data=json.dumps(
                                             {'t': QueryType.BattleGlobalTop.value}))]]
    return InlineKeyboardMarkup(inline_keys)
