from bs4 import UnicodeDammit
import unicodedata
from urllib import parse

CHAR_REPLACEMENT_MAP = {
    '\u2018': '\u0027',
    '\u2019': '\u0027',
    '\u201C': '\u0022',
    '\u201D': '\u0022',
}

COUNTRY_REPLACEMENTS = {
    'korea': ('Republic of', 'South Korea')
}


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


def replace_countries(country_list):
    for n, item in enumerate(country_list):
        if item:
            replacement = COUNTRY_REPLACEMENTS.get(item.lower(), None)
            if replacement:
                if n+1 < len(country_list) and country_list[n+1].lower() == replacement[0].lower():
                    country_list[n+1] = None
                yield replacement[1]
            else:
                yield item
    return country_list
