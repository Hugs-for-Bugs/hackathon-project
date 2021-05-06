START_MESSAGE = """
*Бот для поиска ваканский*
`/search` - для поиска с помощью агрегатора
"""

START_KB = {
    "text": ["Поиск", "Работодателю", "Сменить локацию"],
    "callbacks": ["search", "employer", "ch_location"],
}
