MSG_ORDER_STATISTIC = 'Статистика выполнения приказов за {} дней:\n'
MSG_ORDER_STATISTIC_OUT_FORMAT = '{}: {}/{}\n'
MSG_USER_UNKNOWN = 'Не знаю таких'

MSG_NEW_GROUP_ADMIN = 'Приветствуйте нового админа: @{}!\nДля списка команд бота используй /help'
MSG_NEW_GROUP_ADMIN_EXISTS = '@{} и без тебя тут правит!'

MSG_DEL_GROUP_ADMIN_NOT_EXIST = 'У @{} здесь нет власти!'
MSG_DEL_GROUP_ADMIN = '@{}, тебя разжаловали.'

MSG_NEW_GLOBAL_ADMIN = 'Новый глобальный админ: @{}!'
MSG_NEW_GLOBAL_ADMIN_EXISTS = '@{} и без тебя админ!'

MSG_DEL_GLOBAL_ADMIN_NOT_EXIST = 'У @{} нет власти!'
MSG_DEL_GLOBAL_ADMIN = '@{} разжалован.'

MSG_NEW_SUPER_ADMIN = 'Новый бог: @{}!'
MSG_NEW_SUPER_ADMIN_EXISTS = '@{} уже бог!'

MSG_LIST_ADMINS_HEADER = 'Список здешних админов:\n'
MSG_LIST_ADMINS_FORMAT = '{} @{} {} {}\n'
MSG_LIST_ADMINS_USER_FORMAT = '@{} {} {}\n'

MSG_EMPTY = '[Пусто]\n'

MSG_START_WELCOME = 'Привет'
MSG_ADMIN_WELCOME = 'Да здравствует админ!'

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

MSG_PING = 'Иди освежись, @{}!'

MSG_STOCK_COMPARE_HARVESTED = '📦<b>Награблено:</b>\n'
MSG_STOCK_COMPARE_LOST = '\n📦<b>Потеряно:</b>\n'
MSG_STOCK_COMPARE_FORMAT = '{} ({})\n'
MSG_STOCK_COMPARE_WAIT = 'Жду с чем сравнивать...'

MSG_GROUP_STATUS_CHOOSE_CHAT = 'Выбери чат'
MSG_GROUP_STATUS = 'Группа: {}\n\n' \
                   'Админы:\n' \
                   '{}\n' \
                   'Приветствие: {}\n' \
                   'Триггерят все: {}\n' \
                   'Тернии: {}'
MSG_GROUP_STATUS_ADMIN_FORMAT = '{} @{} {} {}\n'
MSG_GROUP_STATUS_DEL_ADMIN = 'Разжаловать {} {}'

MSG_ON = 'Включено'
MSG_OFF = 'Выключено'
MSG_SYMBOL_ON = '✅'
MSG_SYMBOL_OFF = '❌'
MSG_BACK = '🔙Назад'

MSG_ORDER_TO_SQUADS = 'По отрядам'
MSG_ORDER_ACCEPT = 'Принято!'

MSG_ORDER_CLEARED_BY_HEADER = 'Приказ выполнили:\n'

MSG_ORDER_SENT = 'Ваше сообщение отправлено'

MSG_ORDER_CLEARED = 'Я тебя записал'
MSG_ORDER_CLEARED_ERROR = 'Хорош тыкать, уже всё'

MSG_ORDER_SEND_HEADER = 'Приказ: {}\nКуда слать?'

MSG_ORDER_GROUP_CONFIG_HEADER = 'Настройки группы {}'
MSG_ORDER_GROUP_NEW = 'Напиши мне название новой группы отрядов'
MSG_ORDER_GROUP_LIST = 'Список групп'
MSG_ORDER_GROUP_ADD = '➕Добавить группу'
MSG_ORDER_GROUP_DEL = '🔥🚨Удалить группу🚨🔥'

MSG_NEWBIE = 'Новый игрок в замке!\n' \
             'Все на вербовку %username%!'

MSG_FLAG_CHOOSE_HEADER = 'Выбирай'

MSG_PROFILE_OLD = 'Твой профиль завял, нужно что-то посвежей...'
MSG_PROFILE_SAVED = 'Располагайся в зарослях мяты, {}!\nНе забывай поливать свой профиль хотя бы раз в день. 🌱'
MSG_PROFILE_CASTLE_MISTAKE = 'Перед тобой во всей красе предстали обширные заросли мяты.  '\
                               'Ты бесстрашно зашёл в них, в надежде добраться до таинственных новых земель. '\
                               'Однако долгие часы скитаний не привели тебя ни к чему. '\
                               'Повезло хоть, что выбраться смог! Без проводника здесь делать нечего...'
MSG_PROFILE_SHOW_FORMAT = '👤 %first_name% (%username%)\n' \
                          '%castle% %name%\n' \
                          '🏅 %prof% %level% уровня\n' \
                          '⚜️ Отряд %squad%\n' \
                          '⚔️ %attack% | 🛡 %defence% | 🔥 %exp%/%needExp%\n' \
                          '💰 %gold% | 🔋 %maxStamina%\n' \
                          '🕑 Последнее обновление %date%'
MSG_PROFILE_NOT_FOUND = 'В мятных записях ещё нет данных об этом герое'

MSG_SQUAD_NEW = 'Теперь здесь будет обитать отряд {}!\n'\
                  'Не забудьте задать ссылку для приглашения новых участников.'
MSG_SQUAD_LINK_SAVED = 'Ссылка приглашений сохранена!\nНовые участники теперь не пройдут мимо!'
MSG_SQUAD_RENAMED = 'Теперь этот отряд будет называться {}!'
MSG_SQUAD_DELETE = 'Отряд распущен'
MSG_SQUAD_THORNS_ENABLED = 'Непроходимые тернии выросли вокруг'
MSG_SQUAD_THORNS_DISABLED = 'Тернии завяли, теперь каждый может видеть происходящее'

MSG_TRIGGER_NEW = 'Триггер на фразу "{}" установлен.'
MSG_TRIGGER_NEW_ERROR = 'Какие-то у тебя несвежие мысли, попробуй ещё раз.'
MSG_TRIGGER_EXISTS = 'Триггер "{}" уже существует, выбери другой.'
MSG_TRIGGER_ALL_ENABLED = 'Теперь триггерить могут все.'
MSG_TRIGGER_ALL_DISABLED = 'Теперь триггерить могут только админы.'
MSG_TRIGGER_DEL = 'Триггер на фразу "{}" удалён.'
MSG_TRIGGER_DEL_ERROR = 'Где ты такой триггер видел? 0_о'
MSG_TRIGGER_LIST_HEADER = 'Список текущих триггеров:\n'

MSG_THORNS = '{} не смог пробраться через МЯТНЫЕ, МАТЬ ЕГО, тернии и ему пришлось уйти'

MSG_WELCOME_DEFAULT = 'Привет, %username%!'
MSG_WELCOME_SET = 'Текст приветствия установлен.'
MSG_WELCOME_ENABLED = 'Приветствие включено.'
MSG_WELCOME_DISABLED = 'Приветствие выключено.'

MSG_PIN_ALL_ENABLED = 'Пусть пинят...'
MSG_PIN_ALL_DISABLED = 'Совсем уже распустились, вот мучайтесь теперь 😡'

MSG_ORDER_CLEARED_BY_DUMMY = 'эта функция перерабатывается в связи с высокой нагрузкой от постоянного обновления'

MSG_NO_SQUAD = 'Безотрядный тунеядец'
