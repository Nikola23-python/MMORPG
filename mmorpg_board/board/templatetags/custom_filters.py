from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# Список нежелательных слов (можно вынести в settings.py)
CENSORED_WORDS = [
    'редиска', 'негодяй', 'козел',
]


@register.filter(name='censor', needs_autoescape=True)
def censor(value, autoescape=True):
    if not isinstance(value, str):
        return value
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    words = value.split()
    result = []
    for word in words:
        lower_word = word.lower()
        censored = False

        # Проверяем каждое запрещённое слово
        for bad_word in CENSORED_WORDS:
            if bad_word in lower_word:
                # Заменяем все буквы кроме первой на *
                censored_word = word[0] + ('*' * (len(word) - 1))
                result.append(esc(censored_word))
                censored = True
                break

        if not censored:
            result.append(esc(word))

    return mark_safe(' '.join(result))