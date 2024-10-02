import requests
import re
import ahocorasick

SENSITIVE_WORDS = [
    "我是你爸爸", "我是你爸", "我是你爹", "爸爸",
    "我是你爷爷", "操你奶奶", "我是你妈", "我日你爸",
    "草泥马", "草你妈", "操你妈", "傻逼"
]

BAD_JS_PATTERN = re.compile(r'script|alert|window|prompt|location|href|iframe|onload|onerror', re.IGNORECASE)


async def create_automaton(words):
    automaton = ahocorasick.Automaton()
    for idx, word in enumerate(words):
        automaton.add_word(word, (idx, word))
    automaton.make_automaton()
    return automaton


async def filter_sensitive(text):
    automaton = create_automaton(SENSITIVE_WORDS)
    filtered_text = text

    for end_index, (idx, original_value) in automaton.iter(text):
        filtered_text = filtered_text.replace(original_value, '*' * len(original_value))

    if '*' in filtered_text or BAD_JS_PATTERN.search(text):
        return get_saying()
    else:
        return filtered_text


async def get_saying():
    try:
        response = requests.get("https://open.iciba.com/dsapi/")
        if response.status_code == 200:
            return response.json().get("note", "")
    except Exception as e:
        return str(e)  # 或者处理错误

    return ""
