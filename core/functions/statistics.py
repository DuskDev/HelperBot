from telegram import Update, Bot

from core.functions.reply_markup import generate_statistics_markup
from core.texts import MSG_STATISTICS_ABOUT, PLOT_X_LABEL, PLOT_Y_LABEL, MSG_DAY_SINGLE, MSG_DAY_PLURAL1, \
    MSG_DAY_PLURAL2, MSG_DATE_FORMAT, MSG_PLOT_DESCRIPTION
from core.types import user_allowed, Character
from core.utils import send_async

import matplotlib.pyplot as plot

from datetime import datetime, time, timedelta

import os


@user_allowed
def statistic_about(bot: Bot, update: Update, session):
    markup = generate_statistics_markup()
    send_async(bot,
               chat_id=update.message.chat.id,
               text=MSG_STATISTICS_ABOUT,
               reply_markup=markup)


@user_allowed
def exp_statistic(bot: Bot, update: Update, session):
    profiles = session.query(Character).filter_by(user_id=update.message.from_user.id)\
        .order_by(Character.date).all()
    plot.switch_backend('ps')
    plot.xlabel(PLOT_X_LABEL)
    plot.ylabel(PLOT_Y_LABEL)
    x = [profile.date for profile in profiles]
    y = [profile.exp for profile in profiles]
    need_exp = profiles[-1].needExp
    x.append(datetime.now())
    y.append(y[-1])
    plot.plot(x, y)
    plot.gcf().autofmt_xdate()
    filename = str(datetime.now()).replace(':', '').replace(' ', '').replace('-', '') + '.png'
    with open(filename, 'wb') as file:
        plot.savefig(file, format='png')

    now_date = x[-2]
    prev_date = x[0]
    now_exp = y[-2]
    prev_exp = y[0]
    for date, exp in zip(x[-3::-1], y[-3::-1]):
        if date <= now_date - timedelta(days=3):
            prev_date = date
            prev_exp = exp
            break

    delta = now_date - prev_date
    interval = (delta.days * 86400 + delta.seconds) or 1
    day_exp = (now_exp - prev_exp) * 86400 / interval
    delta_exp = need_exp - now_exp

    text = ''
    if day_exp:
        delta_days = round(delta_exp / day_exp) or 1
        if (delta_days % 10 == 0) or (delta_days % 10 >= 5) or ((delta_days % 100) in (11, 12, 13, 14)):
            days_text = MSG_DAY_PLURAL2
        elif (delta_days % 10) in (2, 3, 4):
            days_text = MSG_DAY_PLURAL1
        else:
            days_text = MSG_DAY_SINGLE
        text = (MSG_DATE_FORMAT.format(delta_days, days_text))

    with open(filename, 'rb') as file:
        bot.sendPhoto(update.message.chat.id, file, MSG_PLOT_DESCRIPTION
                      .format(int(day_exp), delta_exp, text))
    plot.clf()
    os.remove(filename)
