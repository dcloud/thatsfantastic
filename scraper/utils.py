from bs4 import UnicodeDammit
import unicodedata

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}


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
