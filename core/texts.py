""" Строки """

MSG_ORDER_STATISTIC = 'Статистика выполнения приказов за {} дней:\n'
MSG_ORDER_STATISTIC_OUT_FORMAT = '{}: {}/{}\n'
MSG_USER_UNKNOWN = 'Такого овоща нет ¯\_(ツ)_/¯'

MSG_NEW_GROUP_ADMIN = """⚜️Приветствуйте нового фермера: @{}!
Для вызова списка команд используй /help"""
MSG_NEW_GROUP_ADMIN_EXISTS = 'Фермер @{} уже на своем посту.'

MSG_DEL_GROUP_ADMIN_NOT_EXIST = 'У @{} здесь нет власти'
MSG_DEL_GROUP_ADMIN = 'Ферма больше не нуждается в твоих услугах, @{}'

MSG_NEW_GLOBAL_ADMIN = 'Новый кабачок выбран: @{}!'
MSG_NEW_GLOBAL_ADMIN_EXISTS = 'Кабачок @{} уже на своем посту.'

MSG_DEL_GLOBAL_ADMIN_NOT_EXIST = 'У @{} здесь нет власти'
MSG_DEL_GLOBAL_ADMIN = '@{} разжалован.'

MSG_NEW_SUPER_ADMIN = 'Новый баклажан: @{}!'
MSG_NEW_SUPER_ADMIN_EXISTS = 'Баклажан @{} уже на своем посту.'

MSG_LIST_ADMINS_HEADER = '<b>Фермеры отряда:</b>\n'
MSG_LIST_ADMINS_FORMAT = '{} @{} {} {}\n'
MSG_LIST_ADMINS_USER_FORMAT = '@{} {} {}\n'
MSG_LIST_USER_FORMAT = '@{} '

MSG_EMPTY = '[Пусто]\n'

MSG_START_WELCOME = """Привет! Я — бот 🍆<b>Фермы</b>. 
Перешли мне свой <i>игровой профиль</i> 🏅/hero из @ChatWarsBot."""
MSG_ADMIN_WELCOME = 'С возвращением! По каким делам зашел?'

MSG_HELP_GLOBAL_ADMIN = """http://telegra.ph/Pomoshch-po-komandam-Syna-06-05
"""

MSG_HELP_GROUP_ADMIN = """http://telegra.ph/Pomoshch-po-komandam-Syna-06-05
"""

MSG_HELP_USER = "/list_triggers — показать список триггеров."

MSG_PING = '/AVE_FARM'

MSG_STOCK_COMPARE_HARVESTED = '📦<b>Награблено:</b>\n'
MSG_STOCK_COMPARE_LOST = '\n📦<b>Потеряно:</b>\n'
MSG_STOCK_COMPARE_FORMAT = '{} ({})\n'
MSG_STOCK_COMPARE_WAIT = 'Жду с чем сравнивать...'

MSG_PERSONAL_SITE_LINK = '<b>Твоя персональная ссылка на сайт:</b> {}'

MSG_GROUP_STATUS_CHOOSE_CHAT = 'Выбери отряд'
MSG_GROUP_STATUS = """Отряд: <b>{}</b>

Фермеры:
{}
Приветствие: {}
Триггерят все: {}
Тернии: {}"""

MSG_GROUP_STATUS_ADMIN_FORMAT = '{} @{} {} {}\n'
MSG_GROUP_STATUS_DEL_ADMIN = 'Разжаловать {} {}'

MSG_ON = 'Включено'
MSG_OFF = 'Выключено'
MSG_SYMBOL_ON = '✅'
MSG_SYMBOL_OFF = '❌'
MSG_BACK = '🔙Назад'

MSG_ORDER_TO_SQUADS = '🔅По отрядам'
MSG_ORDER_ACCEPT = 'Принято!'
MSG_ORDER_PIN = '✅Пинить'
MSG_ORDER_NO_PIN = '❌Не пинить'
MSG_ORDER_BUTTON = '✅С кнопкой'
MSG_ORDER_NO_BUTTON = '❌Без кнопки'

MSG_ORDER_CLEARED_BY_HEADER = 'Приказ выполнили:\n'

MSG_ORDER_SENT = 'Рассылка завершена'

MSG_ORDER_CLEARED = 'Отлично!'
MSG_ORDER_CLEARED_ERROR = 'Ты уже подготовился'

MSG_ORDER_SEND_HEADER = 'Куда желаешь отправить приказ?'

MSG_ORDER_GROUP_CONFIG_HEADER = 'Настройки группы {}'
MSG_ORDER_GROUP_NEW = 'Напиши название новой группы отрядов'
MSG_ORDER_GROUP_LIST = 'Список групп'
MSG_ORDER_GROUP_ADD = '➕Добавить группу'
MSG_ORDER_GROUP_DEL = '🔥🚨Удалить группу🚨🔥'

MSG_NEWBIE = """Новый игрок в замке!\n
Все на вербовку %username%!"""

MSG_FLAG_CHOOSE_HEADER = 'Выбери цель'

MSG_PROFILE_OLD = '🏅Профиль устарел, пришли мне новый.'
MSG_PROFILE_SAVED = """Профиль обновлен."""
MSG_PROFILE_CASTLE_MISTAKE = """Ну и как ты сюда попал, <b>ШПИОН</b>?
Неужели в своём замке нет других дел?"""
MSG_PROFILE_SHOW_FORMAT = """\
👤 %first_name% %last_name% (%username%)

%castle% %name%
🏅 %prof% %level% уровня
⚜️ %squad%
⚔️ %attack% | 🛡 %defence% | 🔥 %exp%/%needExp%
💰 %gold% | 🔋 %maxStamina%

🕑 Последнее обновление %date%"""

# main.py texts
MSG_MAIN_INLINE_BATTLE = 'К битве готов'
MSG_MAIN_READY_TO_BATTLE = 'Близится бой!'
# -----------------------
MSG_BUILD_REPORT_EXISTS = 'Этот репорт уже был засчитан!'
MSG_BUILD_REPORT_OK = 'Спасибо за помощь на стройке! Это твой {} репорт.'
MSG_BUILD_REPORT_FORWARDED = 'Больше не присылай репорты с твинков!'
MSG_BUILD_REPORT_TOO_OLD = 'Этот репорт устарел, я не могу его принять.'

MSG_REPORT_OLD = 'Этот репорт устарел, я не могу его принять.'
MSG_REPORT_EXISTS = 'Репорт за эту битву уже внесён.'
MSG_REPORT_OK = 'Спасибо! Репорт успешно засчитан.'

MSG_PROFILE_NOT_FOUND = 'Такого овоща нет ¯\_(ツ)_/¯'
MSG_SQUAD_REQUEST_EMPTY = 'Новых заявок не поступало.'

MSG_NO_PROFILE_IN_BOT = 'Сперва перешли мне свой профиль /hero!'
MSG_SQUAD_RECRUITING_ENABLED = 'Набор открыт!'
MSG_SQUAD_RECRUITING_DISABLED = 'Набор закрыт!'
MSG_SQUAD_NO_PROFILE = 'Сперва пусть покажет профиль!'
MSG_SQUAD_GREEN_INLINE_BUTTON = '✅Да'
MSG_SQUAD_RED_INLINE_BUTTON = '❌Нет'
MSG_SQUAD_NEW = 'Здесь расположился отряд <b>{}</b>!'
MSG_SQUAD_LINK_SAVED = """Ссылка приглашений сохранена!
Новые участники теперь не пройдут мимо!"""
MSG_SQUAD_RENAMED = 'Теперь этот отряд будет называться <b>{}</b>!'
MSG_SQUAD_DELETE = 'Отряд распущен'
MSG_SQUAD_THORNS_ENABLED = 'Вход для овощей с чужой грядки закрыт.'
MSG_SQUAD_THORNS_DISABLED = 'Проход в отряд открыт.'
MSG_SQUAD_ALREADY_DELETED = 'Этот пользователь уже исключен из отряда.'
MSG_SQUAD_LEVEL_TOO_LOW = 'В отряды принимают воинов {} уровня и выше. Приходи, когда подкачаешься!'

MSG_TRIGGER_NEW = 'Триггер на фразу "{}" установлен.'
MSG_TRIGGER_GLOBAL = '<b>Глобальные:</b>\n'
MSG_TRIGGER_LOCAL = '\n<b>Локальные:</b>\n'
MSG_TRIGGER_NEW_ERROR = 'Ошибка, триггер не установлен.'
MSG_TRIGGER_EXISTS = 'Триггер "{}" уже существует, выбери другой.'
MSG_TRIGGER_ALL_ENABLED = 'Теперь триггерить могут все.'
MSG_TRIGGER_ALL_DISABLED = 'Теперь триггерить могут только Фермеры.'
MSG_TRIGGER_DEL = 'Триггер на фразу "{}" удалён.'
MSG_TRIGGER_DEL_ERROR = 'Ошибка. Такого триггера нет.'
MSG_TRIGGER_LIST_HEADER = 'Список текущих триггеров:\n'

MSG_THORNS = 'Тернии перегородили вход в отряд.'

MSG_WELCOME_DEFAULT = 'Добро пожаловать в отряд, %username%!'
MSG_WELCOME_SET = 'Текст приветствия установлен.'
MSG_WELCOME_ENABLED = 'Приветствие включено.'
MSG_WELCOME_DISABLED = 'Приветствие выключено.'

MSG_PIN_ALL_ENABLED = 'Теперь пинить могут все.'
MSG_PIN_ALL_DISABLED = 'Теперь пинить могут только Фермеры.'

MSG_ORDER_CLEARED_BY_DUMMY = 'Функция перерабатывается в связи с высокой \
нагрузкой от постоянного обновления'

MSG_NO_SQUAD = 'Без отряда'
MSG_NO_PET = 'Без питомца'
MSG_WANTS_TO_JOIN = '\n\nХочет вступить в отряд {}'

MSG_CLEARED = 'Выполнено'

MSG_NO_USERNAME = 'Сперва сделай себе username в настройках Telegram.'
MSG_SQUAD_LIST = 'Список отрядов:'
MSG_SQUAD_REQUEST_EXISTS = 'Ты уже состоишь в отряде или подал запрос. \
Покинь текущий отряд или отмени запрос, чтобы отправить новый.'
MSG_SQUAD_REQUEST = 'Отряды, в которые тебя могут принять:'
MSG_SQUAD_LEAVED = '{} покинул отряд <b>{}</b>'
MSG_SQUAD_LEAVE_ASK = 'Ты уверен, что хочешь покинуть отряд?'
MSG_SQUAD_LEAVE_DECLINE = 'Передумал? Ну и славно, пусть это останется в секрете!'
MSG_SQUAD_REQUESTED = 'Ты отправил заявку в отряд <b>{}</b>. \
Чтобы ускорить процесс принятия решения, можешь написать Фермерам отряда: {}.'
MSG_SQUAD_REQUEST_ACCEPTED = 'Заявка от {} принята.'
MSG_SQUAD_REQUEST_DECLINED = 'Заявка от {} отклонена.'
MSG_SQUAD_REQUEST_NEW = 'К вам в отряд есть новые заявки.'
MSG_SQUAD_REQUEST_ACCEPTED_ANSWER = 'Вас приняли в отряд.'
MSG_SQUAD_REQUEST_DECLINED_ANSWER = 'Ваша заявка в отряд отклонена.'
MSG_SQUAD_CLEAN = """Чистка отряда <b>{}</b>.
Кого сорвать с грядки?"""
MSG_SQUAD_ADD = '{}, тебя приглашают в отряд. Принять приглашение?'
MSG_SQUAD_ADD_IN_SQUAD = '{} уже числится в одном из отрядов.'
MSG_SQUAD_ADD_ACCEPTED = '{} принял приглашение.'
MSG_SQUAD_ADD_DECLINED = '{} отклонил приглашение.'
MSG_SQUAD_NONE = 'Похоже, ты не состоишь в отряде'

MSG_SQUAD_READY = """Отряд: <b>{1}</b>

К битве готово: <b>{2}</b>
{}⚔ {}🛡"""
MSG_FULL_TEXT_LINE = '<b>{}</b>: {}👥 {}⚔ {}🛡\n'
MSG_FULL_TEXT_TOTAL = '\n<b>Всего</b>: {}👥 {}⚔ {}🛡'

MSG_IN_DEV = 'Ведутся технические работы.'

MSG_TOP_ABOUT = '🏆Выбери топ:'
MSG_STATISTICS_ABOUT = '📈Статистика📈'
MSG_SQUAD_ABOUT = 'Что тебя интересует?'

MSG_TOP_FORMAT = '{}. {} ({}🌟) - {}{}\n'
MSG_SQUAD_TOP_FORMAT = '{}. {} ({}👥) - {}{} ({}{}/👤)\n'
MSG_TOP_DEFENCE = '🛡Топ дэферы:\n\n'
MSG_TOP_ATTACK = '⚔️Топ атакеры:\n\n'
MSG_TOP_EXPERIENCE = '🔥Топ качки:\n\n'
MSG_TOP_GLOBAL_BUILDERS = ''
MSG_TOP_WEEK_BUILDERS = ''
MSG_TOP_WEEK_WARRIORS = '⛳️Топ по участию в битвах:\n\n'

MSG_UPDATE_PROFILE = 'Пришли свежий игровой профиль 🏅 /hero, пока тебя не исключили из отряда.'
MSG_SQUAD_DELETE_OUTDATED = 'Ты был изгнан из отряда, так как давно не обновлял свой профиль.'
MSG_SQUAD_DELETE_OUTDATED_EXT = '{} (@{}) был изгнан из отряда {}, так как давно не обновлял свой профиль.'

MSG_ALREADY_BANNED = 'Пользователь уже забанен. Причина: {2}.'
MSG_USER_BANNED = '{} был замечен в нарушении правил и был с позором изгнан из замка!'
MSG_YOU_BANNED = 'Вас изгнали по причине: {}'
MSG_BAN_COMPLETE = 'Изгнание завершено.'
MSG_USER_NOT_BANNED = 'Этот бользователь не был изгнан.'
MSG_USER_UNBANNED = '{} больше не изгнан.'
MSG_YOU_UNBANNED = 'Ты был разбанен. Теперь мы снова можем пообщаться :)'

PLOT_X_LABEL = 'Дата'
PLOT_Y_LABEL = 'Опыт'

MSG_DAY_SINGLE = 'день'
MSG_DAY_PLURAL1 = 'дня'
MSG_DAY_PLURAL2 = 'дней'
MSG_DATE_FORMAT = '{} {}'
MSG_PLOT_DESCRIPTION = 'В среднем {} опыта в день. До следующего уровня осталось {} опыта и {}'

MSG_SQUAD_CALL_HEADER = 'Все сюда!\n'
MSG_REPORT_SUMMARY_HEADER = 'Репорты отряда {} за битву {}\n' \
                            'Репорты: {} из {}\n' \
                            '<b>Общие</b>\n' \
                            'Атака: ⚔{}\n' \
                            'Защита: 🛡{}\n' \
                            'Профит: 🔥{} 💰{} 📦{}\n\n' \
                            '<b>Личные</b>\n'
MSG_REPORT_SUMMARY_ROW = '<b>{}</b> (@{})\n⚔{} 🛡{} 🔥{} 💰{} 📦{}\n'
MSG_REPORT_SUMMARY_ROW_EMPTY = '<b>{}</b> (@{}) ❗\n'

BTN_HERO = '🏅Герой'
BTN_STOCK = '📦Склад'
BTN_EQUIPMENT = '🎽Экипировка'

BTN_YES = '✅Да'
BTN_NO = '❌Нет'

BTN_LEAVE = 'Выйти'

BTN_ACCEPT = '✅Принять'
BTN_DECLINE = '❌Отклонить'

BTN_WEEK = "Неделя"
BTN_ALL_TIME = "Всё время"
BTN_SQUAD_WEEK = "Отряды за неделю"
BTN_SQUAD_ALL_TIME = "Отряды за всё время"

MSG_LAST_UPDATE = '🕑 Последнее обновление'
MSG_GO_AWAY = 'Пшёл вон!'
MSG_TOP_GENERATING = 'Генерируем топ...'
MSG_READY = 'Готово!'

MSG_NO_REASON = 'Причина не указана.'
