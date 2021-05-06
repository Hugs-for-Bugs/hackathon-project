# Messages
START_MESSAGE = """
*Бот для поиска ваканский*
"""
EMPLOYER_MESSAGE = """
Вы находитель в меню заполнения заявки
Воспользуйтесь клавиатурой для ввода необходимых данных
"""

# KBs
START_KB = {
    "text": ["Поиск в боте", "Поиск в онлайн", "Работодателю", "Сменить локацию"],
    "callbacks": ["search_bot", "search_online", "employer", "ch_location"],
}

EMPLOYER_KB = {
    "text": ["Название", "Информация", "Локация", "Контакты", "Назад"],
    "callbacks": ["set_title", "set_info", "set_location", "set_contacts", "back_{page}"],
}

BACK_KB = {
    "text": ["Назад"],
    "callbacks": ["back_{page}"]
}
