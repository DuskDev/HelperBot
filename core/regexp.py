# -*- coding: utf-8 -*-
profile = '(🇬🇵|🇮🇲|🇨🇾|🇻🇦|🇪🇺|🇲🇴|🇰🇮)(.+), (.+) .+ замка\n' \
          '🏅Уровень: ([0-9]+)\n' \
          '(?:.*)Атака: ([0-9]+) 🛡Защита: ([0-9]+)\n' \
          '🔥Опыт: ([0-9]+)/([0-9]+)\n' \
          '🔋Выносливость: ([0-9]+)/([0-9]+)\n' \
          '(?:💧Мана: [0-9]+/[0-9]+\n)?' \
          '💰([0-9]+) 💠([0-9]+)\n\n' \
          '🎽Экипировка (.+)\n' \
          '🎒Рюкзак: ([0-9]+)/([0-9]+) /inv' \
          '(?:\n\nПомощник:\n(.+?) (?:.+?) (.+)? \(([0-9]+) ур\.\) (.+) /pet)?'
