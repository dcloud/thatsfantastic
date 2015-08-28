from bs4 import UnicodeDammit
import unicodedata


def decode_html(html_string, smart_quotes_to="ascii"):
    converted = UnicodeDammit(html_string, is_html=True, smart_quotes_to=smart_quotes_to)
    if not converted.unicode_markup:
        raise UnicodeDecodeError(
            "Failed to detect encoding, tried [%s]",
            ', '.join(converted.triedEncodings))
    return converted.unicode_markup


def unicode_normalize(string):
    return unicodedata.normalize('NFKC', string)
