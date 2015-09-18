from bs4 import UnicodeDammit
import unicodedata
from urllib import parse

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}

COUNTRY_NAME_OFFICIALDOM = (
    "democratic people's republic of",
    "republic of",
    "people's republic of",
)


def correct_countries_list(countries_list):
    for n, item in enumerate(countries_list):
        if countries_list[n]:
            if n + 1 < len(countries_list):
                l_item = countries_list[n+1].lower()
                if l_item in COUNTRY_NAME_OFFICIALDOM:
                    yield ' '.join((countries_list[n+1], countries_list[n]))
                    countries_list[n+1] = None
                else:
                    yield countries_list[n]
            else:
                yield countries_list[n]


def is_web_url(url_cand):
    if isinstance(url_cand, parse.ParseResult):
        parsed = url_cand
    else:
        parsed = parse.urlparse(url_cand)
    if not parsed.scheme.startswith('http'):
        return False
    if not parsed.netloc:
        return False
    return True


def correct_web_url(url, http_scheme='https', append_slash=False):
    parsed = parse.urlparse(url)
    if not parsed.scheme:
        if append_slash and url[-1] != '/':
            url += '/'
        parsed = parse.urlparse("{scheme}://{path}".format(scheme=http_scheme, path=url))
    valid = is_web_url(parsed)
    if valid:
        return parse.urlunparse(parsed)
    else:
        raise TypeError('Supplied value connect be coerced into a web URL')


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


def country_title(string):
    return ' '.join(s.lower() not in ('of', 'the') and s.capitalize() or s.lower() for s in string.split(' '))
