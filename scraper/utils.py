from bs4 import UnicodeDammit
import unicodedata
import re

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}

# This small words list includes English and other languages
SMALL_WORDS = ['A', 'AN', 'AND', 'BY', 'DE', 'EL', 'FOR', 'IN', 'OF', 'THE', 'UN', 'VS', 'Y']
REPLACEMENTS = {
                    'ABCS': 'ABCs',
                    'V/H/S': 'V/H/S'
                }
ROMANS_REG = r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})(\b|\:|\.)'
CALENDAR_ERA_REG = r'(?<=\d)\s?(A\.?D\.?|B\.?C\.?)([^A-Z]|$)'


def deeducate_quotes(string):
    for k, v in CHAR_REPLACEMENT_MAP.items():
        string = string.replace(k, v)
    return string


def decode_html(html_string, smart_quotes_to="ascii"):
    converted = UnicodeDammit(html_string, is_html=True, smart_quotes_to=smart_quotes_to)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode_markup


def unicode_normalize(string):
    return unicodedata.normalize('NFKC', string)


def clean_string(string):
    return deeducate_quotes(string.strip())


def string_to_list(string):
    return [clean_string(x) for x in string.split(',') if x.strip()]


def titlecase(string, exceptions=SMALL_WORDS, replacements=REPLACEMENTS):
    parts = re.split(': ', string.upper())
    if len(parts) > 1:
        return ': '.join([titlecase(p, exceptions=exceptions) for p in parts])
    else:
        words = re.split(' ', parts[0])
        title_words = [words[0] in replacements and replacements[words[0]] or words[0].capitalize()]
        for w in words[1:]:
            if w in replacements:
                title_words.append(replacements[w])
            # Handle parentheticals
            elif w not in exceptions and len(w) > 1 and w[0] == '(':
                title_words.append(w[0] + w[1:].capitalize())
            else:
                title_words.append(w in exceptions and w.lower() or w.capitalize())
        s = ' '.join(title_words)
        s = re.sub(r'|'.join([ROMANS_REG, CALENDAR_ERA_REG]),
                   lambda mo: mo.group().upper(),
                   s, flags=re.I)
        return s
