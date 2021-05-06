# Messages
START_MESSAGE = """
*Bot for job search*
"""
EMPLOYER_MESSAGE = """
This is menu which you should fill
Please, use the keyboard to enter the required data
"""

# KBs
START_KB = {
    "text": ["🔍 Search in the Bot", "🔎 Online search", "📄 For the employer", "🌍 Change location"],
    "callbacks": ["search_bot", "search_online", "employer", "ch_location"],
}

EMPLOYER_KB = {
    "text": ["🖊 Title", "📖 Information", "🌍 Location", "📞 Contacts", "◀️ Back"],
    "callbacks": ["set_title", "set_info", "set_location", "set_contacts", "back_{page}"],
}

BACK_KB = {
    "text": ["◀️ Back"],
    "callbacks": ["back_{page}"]
}
