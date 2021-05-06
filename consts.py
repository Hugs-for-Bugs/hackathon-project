# Messages
START_MESSAGE = """
*Бот для поиска ваканский*
`/search` - для поиска с помощью агрегатора
"""
EMPLOYER_MESSAGE = """
Вы находитель в меню заполнения заявки
Воспользуйтесь клавиатурой для ввода необходимых данных
"""

# KBs
START_KB = {
    "text": ["Поиск", "Работодателю", "Сменить локацию"],
    "callbacks": ["search", "employer", "ch_location"],
}

EMPLOYER_KB = {
    "text": ["Название", "Информация", "Локация", "Назад"],
    "callbacks": ["set_title", "set_info", "set_location", "back_{page}"],
}

BACK_KB = {
    "text": ["Назад"],
    "callbacks": ["back_{page}"]
}
