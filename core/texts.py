""" Строки """

MSG_ORDER_STATISTIC = 'Статистика выполнения приказов за {} дней:\n'
MSG_ORDER_STATISTIC_OUT_FORMAT = '{}: {}/{}\n'
MSG_USER_UNKNOWN = 'Такого овоща нет ¯\_(ツ)_/¯'

MSG_NEW_GROUP_ADMIN = """⚜️Приветствуйте нового фермера: @{}!
Для вызова списка команд используй /help"""
NEW_GROUP_ADMIN_EXISTS = 'Фермер @{} уже на своем посту.'

MSG_DEL_GROUP_ADMIN_NOT_EXIST = 'У @{} здесь нет власти'
MSG_DEL_GROUP_ADMIN = 'Ферма больше не нуждается в твоих услугах, @{}'

MSG_NEW_GLOBAL_ADMIN = 'Новый кабачок выбран: @{}!'
MSG_NEW_GLOBAL_ADMIN_EXISTS = 'Кабачок @{} уже на своем посту.'

MSG_DEL_GLOBAL_ADMIN_NOT_EXIST = 'У @{} здесь нет власти'
MSG_DEL_GLOBAL_ADMIN = '@{} разжалован.'

MSG_NEW_SUPER_ADMIN = 'Новый баклажан: @{}!'
MSG_NEW_SUPER_ADMIN_EXISTS = 'Баклажан @{} уже на своем посту.'

MSG_LIST_ADMINS_HEADER = 'Фермеры отряда:\n'
MSG_LIST_ADMINS_FORMAT = '{} @{} {} {}\n'
MSG_LIST_ADMINS_USER_FORMAT = '@{} {} {}\n'

MSG_EMPTY = '[Пусто]\n'

MSG_START_WELCOME = """Привет! Я - бот 🍆<b>Фермы</b>. 
Перешли мне свой <i>игровой профиль</i> из @ChatWarsBot (кнопка "🏅Герой")"""
MSG_ADMIN_WELCOME = 'С возвращением! По каким делам зашел?'

MSG_HELP_GLOBAL_ADMIN = """Команды приветствия:
/enable_welcome — включить приветствие.
/disable_welcome — выключить приветствие.
/set_welcome <текст> — установить текст приветствия. \
Может содержать %username% — будет заменено на @username, \
если не установлено на Имя Фамилия, %first_name% — на имя, 
%last_name% — на фамилию, %id% — на id.
/show_welcome — показать текущий текст приветствия для данного чата.

Команды триггеров:
/set_trigger <триггер>::<сообщение> — \
установить сообщение, которое бот будет отправлять по триггеру.
/add_trigger <триггер>::<сообщение> — \
добавить сообщение, которое бот будет отправлять по триггеру. \
Старое сообщение не заменяется.
/del_trigger <триггер> — удалить триггер.
/list_triggers — показать все триггеры.

Команды суперадмина:
/add_admin <пользователь> — добавить админа для текущего чата.
/del_admin <пользователь> — забрать привилегии у админа текущего чата.
/list_admins — показать список админов в чате.
/enable_trigger — разрешить триггерить всем в группе.
/disable_trigger — запретить триггерить всем в группе.
"""

MSG_HELP_GROUP_ADMIN = """Команды приветствия:
/enable_welcome — включить приветствие.
/disable_welcome — выключить приветствие.
/set_welcome <текст> — установить текст приветствия. \
Может содержать %username% — будет заменено на @username, \
если не установлено на Имя Фамилия, %first_name% — на имя, 
%last_name% — на фамилию, %id% — на id.
/show_welcome — показать текущий текст приветствия для данного чата.

Команды триггеров:
/add_trigger <триггер>::<сообщение> — \
добавить сообщение, которое бот будет отправлять по триггеру. \
Старое сообщение не заменяется.
/list_triggers — показать список триггеров.
/enable_trigger — разрешить триггерить всем в группе.
/disable_trigger — запретить триггерить всем в группе.
"""

MSG_HELP_USER = "/list_triggers — показать список триггеров."

MSG_PING = '/AVE_FARM'

MSG_STOCK_COMPARE_HARVESTED = '📦<b>Награблено:</b>\n'
MSG_STOCK_COMPARE_LOST = '\n📦<b>Потеряно:</b>\n'
MSG_STOCK_COMPARE_FORMAT = '{} ({})\n'
MSG_STOCK_COMPARE_WAIT = 'Жду с чем сравнивать...'

MSG_GROUP_STATUS_CHOOSE_CHAT = 'Выбери чат'
MSG_GROUP_STATUS = """Отряд: {}

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

MSG_ORDER_CLEARED_BY_HEADER = 'Приказ выполнили:\n'

MSG_ORDER_SENT = 'Рассылка завершена'

MSG_ORDER_CLEARED = 'Отлично! Ты попал на грядку'
MSG_ORDER_CLEARED_ERROR = 'Ты уже на грядке'

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
MSG_PROFILE_SHOW_FORMAT = """
👤 %first_name% %last_name% (%username%)

%castle% %name%
🏅 %prof% %level% уровня
⚜️ %squad%
⚔️ %attack% | 🛡 %defence% | 🔥 %exp%/%needExp%
💰 %gold% | 🔋 %maxStamina%

🕑 Последнее обновление %date%"""

MSG_PROFILE_NOT_FOUND = 'Такого овоща нет ¯\_(ツ)_/¯'
MSG_SQUAD_REQUEST_EMPTY = 'Заявок не поступало.'

MSG_SQUAD_NEW = 'Здесь расположился отряд <b>{}</b>!'
MSG_SQUAD_LINK_SAVED = """Ссылка приглашений сохранена!
Новые участники теперь не пройдут мимо!"""
MSG_SQUAD_RENAMED = 'Теперь этот отряд будет называться <b>{}</b>!'
MSG_SQUAD_DELETE = 'Отряд распущен'
MSG_SQUAD_THORNS_ENABLED = 'Вход для овощей с чужой грядки закрыт.'
MSG_SQUAD_THORNS_DISABLED = 'Проход в отряд открыт.'

MSG_TRIGGER_NEW = 'Триггер на фразу "{}" установлен.'
MSG_TRIGGER_NEW_ERROR = 'Ошибка, триггер не установлен.'
MSG_TRIGGER_EXISTS = 'Триггер "{}" уже существует, выбери другой.'
MSG_TRIGGER_ALL_ENABLED = 'Теперь триггерить могут все.'
MSG_TRIGGER_ALL_DISABLED = 'Теперь триггерить могут только Жрецы.'
MSG_TRIGGER_DEL = 'Триггер на фразу "{}" удалён.'
MSG_TRIGGER_DEL_ERROR = 'Ошибка. Такого триггера нет'
MSG_TRIGGER_LIST_HEADER = 'Список текущих триггеров:\n'

MSG_THORNS = 'Тернии перегородили вход в отряд.'

MSG_WELCOME_DEFAULT = 'Добро пожаловать в отряд, %username%!'
MSG_WELCOME_SET = 'Текст приветствия установлен.'
MSG_WELCOME_ENABLED = 'Приветствие включено.'
MSG_WELCOME_DISABLED = 'Приветствие выключено.'

MSG_ORDER_CLEARED_BY_DUMMY = 'Функция перерабатывается в связи с высокой \
нагрузкой от постоянного обновления'

MSG_NO_SQUAD = '[Пусто]'
MSG_WANTS_TO_JOIN = '\n\nХочет вступить в отряд {}'

MSG_CLEARED = 'Выполнено'

MSG_SQUAD_LIST = 'Список отрядов:'
MSG_SQUAD_REQUEST_EXISTS = 'Ты уже состоишь в отряде или подал запрос. \
Покинь текущий отряд или отмени запрос, чтобы отправить новый.'
MSG_SQUAD_REQUEST = 'Вот отряды, в которые тебя могут принять:'
MSG_SQUAD_LEAVED = '{} покинул отряд <b>{}</b>'
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

MSG_SQUAD_READY = """Отряд: <b>{1}</b>

К битве готово: <b>{2}</b>
{}⚔ {}🛡"""
SG_SQUAD_READY = """Отряд: <b>{1}</b>

К битве готово: <b>{2}</b>
{}⚔ {}🛡"""
MSG_FULL_TEXT_LINE = '<b>{}</b>: {}👥 {}⚔ {}🛡\n'
MSG_FULL_TEXT_TOTAL = '\n<b>Всего</b>: {}👥 {}⚔ {}🛡'
