from bs4 import UnicodeDammit
import unicodedata
import re

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}

SMALL_WORDS_REG = r'(?<!^)(?<!(\:|\.|\!)\s)(a|an|and|by|for|in|of|the)\b'
ROMANS_REG = r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})(\b|\:|\.)'
APOS_REG = r"[A-Za-z]+('[A-Za-z]+)?"
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


def titlecase(s):
    s = re.sub(APOS_REG,
               lambda mo: mo.group(0)[0].upper() +
               mo.group(0)[1:].lower(),
               s)
    s = re.sub(SMALL_WORDS_REG,
               lambda mo: mo.group().lower(),
               s, flags=re.I)
    s = re.sub(r'|'.join([ROMANS_REG, CALENDAR_ERA_REG]),
               lambda mo: mo.group().upper(),
               s, flags=re.I)
    return s
