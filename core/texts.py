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

MSG_START_WELCOME = 'Привет! Я - бот 🇰🇮<b>Сумрачного замка</b>.'\
                    'Перешли мне свой <i>игровой профиль</i> из @ChatWarsBot (кнопка "🏅Герой").'
MSG_ADMIN_WELCOME = 'Узнаю тебя, Жрец. По каким делам зашел?'

MSG_HELP_GLOBAL_ADMIN = 'Команды приветствия:\n'\
                          '/enable_welcome - Включить приветствие\n'\
                          '/disable_welcome - Выключить приветствие\n'\
                          '/set_welcome <текст> - Установить текст приветствия. '\
                          'Может содержать %username% - будет заменено на @username, '\
                          'если не установлено на Имя Фамилия, %first_name% - на имя, '\
                          '%last_name% - на фамилию, %id% - на id\n'\
                          '/show_welcome - Показать текущий текст приветствия для '\
                          'данного чата'\
                          '\n\n'\
                          'Команды триггеров:\n'\
                          '/set_trigger <триггер>::<сообщение> - Установить сообщение, '\
                          'которое бот будет кидать по триггеру.\n'\
                          '/add_trigger <триггер>::<сообщение> - Добавляет сообщение, '\
                          'которое бот будет кидать по триггеру, но не заменяет старый.\n'\
                          '/del_trigger <триггер> - Удалить соответствующий триггер\n'\
                          '/list_triggers - Показать все существующие триггеры'\
                          '\n\n'\
                          'Команды глобаладмина:\n'\
                          '/add_admin <юзернэйм> - Добавить админа для текущего чата\n'\
                          '/del_admin <юзернэйм> - Забрать привелегии у админа текущего '\
                          'чата\n'\
                          '/list_admins - Показать список местных админов\n'\
                          '/enable_trigger - Разрешить триггерить всем в группе\n'\
                          '/disable_trigger - Запретить триггерить всем в группе'

MSG_HELP_GROUP_ADMIN = 'Команды приветствия:\n'\
                         '/enable_welcome - Включить приветствие\n'\
                         '/disable_welcome - Выключить приветствие\n'\
                         '/set_welcome <текст> - Установить текст приветствия. '\
                         'Может содержать %username% - будет заменено на @username, '\
                         'если не установлено на Имя Фамилия, %first_name% - на имя, '\
                         '%last_name% - на фамилию, %id% - на id\n'\
                         '/show_welcome - Показать текущий текст приветствия для '\
                         'данного чата'\
                         '\n\n'\
                         'Команды триггеров:\n'\
                         '/add_trigger <триггер>::<сообщение> - Добавляет сообщение, '\
                         'которое бот будет кидать по триггеру, но не заменяет старый.\n'\
                         '/list_triggers - Показать все существующие триггеры\n'\
                         '/enable_trigger - Разрешить триггерить всем в группе\n'\
                         '/disable_trigger - Запретить триггерить всем в группе'

MSG_HELP_USER = 'Команды триггеров:\n'\
                  '/list_triggers - Показать все существующие триггеры'

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

MSG_NEWBIE = 'Новый игрок в замке!\n' \
             'Все на вербовку %username%!'

MSG_FLAG_CHOOSE_HEADER = 'Выбери цель'

MSG_PROFILE_OLD = '🏅Твой профиль устарел, пришли мне новый.'
MSG_PROFILE_SAVED = '**Владыка Миров** доволен тобой!'\
                    'Не забывай приносить ему свой профиль в жертву каждый день — и тогда он будет милостив к тебе (__но это не точно__).'
MSG_PROFILE_CASTLE_MISTAKE = 'Ну и как ты сюда попал, <b>ШПИОН</b>?'\
                             'Неужели в своём замке нет других дел?'
MSG_PROFILE_SHOW_FORMAT = '👤 %first_name% %last_name% (%username%)\n' \
                          '%castle% %name%\n' \
                          '🏅 %prof% %level% уровня\n' \
                          '⚜️ Отряд %squad%\n' \
                          '⚔️ %attack% | 🛡 %defence% | 🔥 %exp%/%needExp%\n' \
                          '💰 %gold% | 🔋 %maxStamina%\n' \
                          '%pet%\n' \
                          '🕑 Последнее обновление %date%'
MSG_PROFILE_NOT_FOUND = 'На глиняных таблицах Р’льеха его нет.'
MSG_SQUAD_REQUEST_EMPTY = 'От культистов заявок не поступало.'

MSG_SQUAD_NEW = 'В этом зале расположился отряд <b>{}</b>!'
MSG_SQUAD_LINK_SAVED = 'Ссылка приглашений сохранена!\n Новые участники теперь не пройдут мимо!'
MSG_SQUAD_RENAMED = 'Теперь этот отряд будет называться <b>{}</b>!'
MSG_SQUAD_DELETE = 'Отряд распущен'
MSG_SQUAD_THORNS_ENABLED = 'Щупальца Ктулху перегородили вход в этот отряд'
MSG_SQUAD_THORNS_DISABLED = 'Ктулху смилостивился, впуская чужеземцев.'

MSG_TRIGGER_NEW = 'Триггер на фразу "{}" установлен.'
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
