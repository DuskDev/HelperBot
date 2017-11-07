""" Строки """

MSG_ORDER_STATISTIC = 'Статистика выполнения приказов за {} дней:\n'
MSG_ORDER_STATISTIC_OUT_FORMAT = '{}: {}/{}\n'
MSG_USER_UNKNOWN = 'На глиняных таблицах Р’льеха его нет'

MSG_NEW_GROUP_ADMIN = '⚜️Приветствуйте нового Жреца: @{}!\nДля списка команд бота используй /help'
MSG_NEW_GROUP_ADMIN_EXISTS = 'Великим Ктулху уже выбран @{}, изыди.'

MSG_DEL_GROUP_ADMIN_NOT_EXIST = 'У @{} здесь нет власти!'
MSG_DEL_GROUP_ADMIN = 'Генералы Сумрака больше не нуждаются в твоих услугах, @{}'

MSG_NEW_GLOBAL_ADMIN = 'Новый Генерал: @{}!'
MSG_NEW_GLOBAL_ADMIN_EXISTS = 'Великим Ктулху уже выбран @{}, изыди.'

MSG_DEL_GLOBAL_ADMIN_NOT_EXIST = 'У @{} нет власти!'
MSG_DEL_GLOBAL_ADMIN = '@{} разжалован.'

MSG_NEW_SUPER_ADMIN = 'Новый бог: @{}!'
MSG_NEW_SUPER_ADMIN_EXISTS = '@{} уже бог!'

MSG_LIST_ADMINS_HEADER = 'Список здешних Жрецов:\n'
MSG_LIST_ADMINS_FORMAT = '{} @{} {} {}\n'
MSG_LIST_ADMINS_USER_FORMAT = '@{} {} {}\n'

MSG_EMPTY = '[Пусто]\n'

MSG_START_WELCOME = 'Привет! Я - бот 🇰🇮<b>Сумрачного замка</b>. '\
                    'Перешли мне свой <i>игровой профиль</i> из @ChatWarsBot (🏅 команда "/hero").'
MSG_ADMIN_WELCOME = 'Узнаю тебя, Жрец. По каким делам зашел?'

MSG_HELP_GLOBAL_ADMIN = """http://telegra.ph/Pomoshch-po-komandam-bota-09-28"""

MSG_HELP_GROUP_ADMIN = """http://telegra.ph/Pomoshch-po-komandam-bota-09-28"""

MSG_HELP_USER = "http://telegra.ph/Pomoshch-po-komandam-bota-09-28"

MSG_PING = '/AVE_TWILIGHT'

MSG_STOCK_COMPARE_HARVESTED = '📦<b>Награблено:</b>\n'
MSG_STOCK_COMPARE_LOST = '\n📦<b>Потеряно:</b>\n'
MSG_STOCK_COMPARE_FORMAT = '{} ({})\n'
MSG_STOCK_COMPARE_WAIT = 'Жду, с чем сравнивать...'

MSG_GROUP_STATUS_CHOOSE_CHAT = 'Выбери чат'
MSG_GROUP_STATUS = 'Отряд: {}\n\n' \
                   'Жрецы:\n' \
                   '{}\n' \
                   'Приветствие: {}\n' \
                   'Триггерят все: {}\n' \
                   'Щупальца: {}'
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
MSG_ORDER_NO_PIN = '❌Не Пинить'
MSG_ORDER_BUTTON = '✅С кнопкой'
MSG_ORDER_NO_BUTTON = '❌Без кнопки'

MSG_ORDER_CLEARED_BY_HEADER = 'Приказ выполнили:\n'

MSG_ORDER_SENT = 'Рассылка завершена.'

MSG_ORDER_CLEARED = 'Ты внесён в списки'
MSG_ORDER_CLEARED_ERROR = 'Не донимай Владыку, ты уже записан'

MSG_ORDER_SEND_HEADER = 'Куда желаешь отправить приказ?'

MSG_ORDER_GROUP_CONFIG_HEADER = 'Настройки группы {}'
MSG_ORDER_GROUP_NEW = 'Напиши мне название новой группы отрядов'
MSG_ORDER_GROUP_LIST = 'Список групп'
MSG_ORDER_GROUP_ADD = '➕Добавить группу'
MSG_ORDER_GROUP_DEL = '🔥🚨Удалить группу🚨🔥'

MSG_NEWBIE = """Новый игрок в замке!\n
Все на вербовку %username%!"""

MSG_FLAG_CHOOSE_HEADER = 'Выбери цель'

MSG_PROFILE_OLD = '🏅Твой профиль устарел, пришли мне новый.'
MSG_PROFILE_SAVED = '<b>Владыка Миров</b> доволен тобой! '\
                    'Не забывай приносить ему свой профиль в жертву каждый день — и тогда он будет милостив к тебе ' \
                    '<i>(но это не точно)</i>. '
MSG_PROFILE_CASTLE_MISTAKE = 'Ну и как ты сюда попал, <b>ШПИОН</b>? '\
                             'Неужели в своём замке нет других дел?'
MSG_PROFILE_SHOW_FORMAT = '👤 %first_name% %last_name% (%username%)\n' \
                          '%castle% %name%\n' \
                          '🏅 %prof% %level% уровня\n' \
                          '⚜️ Отряд %squad%\n' \
                          '⚔️ %attack% | 🛡 %defence% | 🔥 %exp%/%needExp%\n' \
                          '💰 %gold% | 🔋 %maxStamina%\n' \
                          '%pet%\n' \
                          '🕑 Последнее обновление %date%'

# ---main.py texts-------
MSG_MAIN_INLINE_BATTLE = 'Разбудить Ктулху'
MSG_MAIN_READY_TO_BATTLE = 'К битве готовсь!'
# -----------------------
MSG_BUILD_REPORT_EXISTS = 'Ты уже кидал этот репорт!'
MSG_BUILD_REPORT_OK = 'Спасибо за помощь на стройке! Это твой {} репорт.'
MSG_BUILD_REPORT_FORWARDED = 'Больше не присылай мне репорты с твинков!!!'

MSG_REPORT_OLD = 'Твой репорт уже попахивает, в следующий раз постарайся прислать его в течении минуты после получения.'
MSG_REPORT_EXISTS = 'Репорт за эту битву уже внесён.'
MSG_REPORT_OK = 'Спасибо. Не забывай кидать репорты каждую битву.'

MSG_PROFILE_NOT_FOUND = 'На глиняных таблицах Р’льеха его нет.'
MSG_SQUAD_REQUEST_EMPTY = 'От культистов заявок не поступало.'

MSG_NO_PROFILE_IN_BOT = 'Сначала дай мне профиль!'
MSG_SQUAD_RECRUITING_ENABLED = 'Набор открыт!'
MSG_SQUAD_RECRUITING_DISABLED = 'Набор закрыт!'
MSG_SQUAD_NO_PROFILE = 'Сначала пусть даст профиль!'
MSG_SQUAD_GREEN_INLINE_BUTTON = '✅Зелёное Да'
MSG_SQUAD_RED_INLINE_BUTTON = '❌Красное Да'
MSG_SQUAD_NEW = 'В этом зале расположился отряд <b>{}</b>!'
MSG_SQUAD_LINK_SAVED = 'Ссылка приглашений сохранена!\n Новые участники теперь не пройдут мимо!'
MSG_SQUAD_RENAMED = 'Теперь этот отряд будет называться <b>{}</b>!'
MSG_SQUAD_DELETE = 'Отряд распущен'
MSG_SQUAD_THORNS_ENABLED = 'Щупальца Ктулху перегородили вход в этот отряд'
MSG_SQUAD_THORNS_DISABLED = 'Ктулху смилостивился, впуская чужеземцев.'
MSG_SQUAD_ALREADY_DELETED = 'Этот пользователь уже выпилен из отряда, кнопка больше не работает =('

MSG_TRIGGER_NEW = 'Триггер на фразу "{}" установлен.'
MSG_TRIGGER_GLOBAL = '<b>Глобальные:</b>\n'
MSG_TRIGGER_LOCAL = '\n<b>Локальные:</b>\n'
MSG_TRIGGER_NEW_ERROR = 'Ошибка, триггер не установлен.'
MSG_TRIGGER_EXISTS = 'Триггер "{}" уже существует, выбери другой.'
MSG_TRIGGER_ALL_ENABLED = 'Теперь триггерить могут все.'
MSG_TRIGGER_ALL_DISABLED = 'Теперь триггерить могут только Жрецы.'
MSG_TRIGGER_DEL = 'Триггер на фразу "{}" удалён.'
MSG_TRIGGER_DEL_ERROR = 'Ошибка. Такого триггера нет.'
MSG_TRIGGER_LIST_HEADER = 'Список текущих триггеров:\n'

MSG_THORNS = 'Великий Ктулху не давал {} доступ в чат'

MSG_WELCOME_DEFAULT = 'Добро пожаловать в твой отряд, %username%!'
MSG_WELCOME_SET = 'Текст приветствия установлен.'
MSG_WELCOME_ENABLED = 'Приветствие включено.'
MSG_WELCOME_DISABLED = 'Приветствие выключено.'

MSG_PIN_ALL_ENABLED = 'Теперь пинить могут все.'
MSG_PIN_ALL_DISABLED = 'Теперь пинят только Жрецы.'

MSG_ORDER_CLEARED_BY_DUMMY = 'эта функция перерабатывается в связи с высокой нагрузкой от постоянного обновления'

MSG_NO_SQUAD = 'Безотрядный тунеядец'
MSG_NO_PET = 'Нет питомца'

MSG_CLEARED = 'Выполнено'

MSG_SQUAD_LIST = 'Список ваших отрядов:'
MSG_SQUAD_REQUEST_EXISTS = 'Ты уже состоишь в отряде или подал запрос. Покинь текущий отряд или отмени запрос, чтобы отправить новый.'
MSG_SQUAD_REQUEST = 'Вот отряды, в которые тебя могут принять:'
MSG_SQUAD_LEAVED = '{} покинул отряд <b>{}</b>'
MSG_SQUAD_REQUESTED = 'Ты отправил заявку в отряд <b>{}</b>. Чтобы ускорить процесс принятия решения, можешь написать Жрецам отряда: {}.'
MSG_SQUAD_REQUEST_ACCEPTED = 'Заявка от {} принята.'
MSG_SQUAD_REQUEST_DECLINED = 'Заявка от {} отклонена.'
MSG_SQUAD_REQUEST_NEW = 'К вам в отряд есть новые заявки.'
MSG_SQUAD_REQUEST_ACCEPTED_ANSWER = 'Вас приняли в отряд.'
MSG_SQUAD_REQUEST_DECLINED_ANSWER = 'Ваша заявка в отряд отклонена.'
MSG_SQUAD_CLEAN = 'Чистка отряда <b>{}</b>.\n' \
                  'Кого принести в жертву Ктулху?'
MSG_SQUAD_ADD = '{}, тебя приглашают в отряд. Принять приглашение?'
MSG_SQUAD_ADD_IN_SQUAD = '{} уже числится в одном из отрядов Сумрака.'
MSG_SQUAD_ADD_ACCEPTED = '{} принял предложение.'
MSG_SQUAD_ADD_DECLINED = '{} отклонил приглашение.'
MSG_SQUAD_NONE = 'Похоже ты не в отряде'

MSG_SQUAD_READY = '{} бойцов отряда <b>{}</b> к битве готовы!\n{}⚔ {}🛡'
MSG_FULL_TEXT_LINE = '{}: {}👥 {}⚔ {}🛡\n'
MSG_FULL_TEXT_TOTAL = '\n<b>Всего</b>: {}👥 {}⚔ {}🛡'
MSG_WANTS_TO_JOIN = '\n\nХочет вступить в отряд {}'

MSG_IN_DEV = 'Функция находится в разработке =('

MSG_TOP_ABOUT = '🏆 Топы 🏆'
MSG_STATISTICS_ABOUT = '📈Статистика📈'
MSG_SQUAD_ABOUT = '⚜Отряд⚜'

MSG_TOP_FORMAT = '{}. {} ({}🌟) - {}{}\n'
MSG_TOP_DEFENCE = '🛡Топ дэферы:\n'
MSG_TOP_ATTACK = '⚔Топ атакеры:\n'
MSG_TOP_EXPERIENCE = '🔥Топ качки:\n'

MSG_UPDATE_PROFILE = 'Пришли свежий игровой профиль (🏅 команда "/hero"), пока Владыка Миров не разгневался.'
MSG_SQUAD_DELETE_OUTDATED = 'Ты был изгнан из отряда за то, что давно не обновлял свой профиль.'
MSG_SQUAD_DELETE_OUTDATED_EXT = '{} был изгнан из отряда {} за то, что давно не обновлял свой профиль.'

MSG_ALREADY_BANNED = 'Пользователь уже забанен. Причина: {2}.'
MSG_USER_BANNED = 'Член нашего ордена {} был замечен в нарушении правил и был с позором изгнан из замка!'
MSG_YOU_BANNED = 'Вас изгнали по причине {}'
MSG_BAN_COMPLETE = 'Изгнание завершено.'
MSG_USER_NOT_BANNED = 'Мы не изгоняли этого господина.'
MSG_USER_UNBANNED = '{} больше не изгнан.'
MSG_YOU_UNBANNED = 'Мы снова можем пообщаться 🌚'
