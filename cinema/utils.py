import re
import string

# This small words list includes English and other languages
SMALL_WORDS = ['A', 'AN', 'AND', 'BY', 'DE', 'EL', 'FOR', 'IN', 'OF', 'THE', 'UN', 'VS', 'WITH', 'Y']
REPLACEMENTS = {
    'ABCS': 'ABCs',
    'V/H/S': 'V/H/S',
    'VIC+FLO': 'Vic+Flo'
}
ROMANS_REG = r'\bM{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})(\b|\:|\.)'
ORDINAL_SUFFIXES = ('st', 'nd', 'rd', 'th')


def titlecase(in_string, exceptions=SMALL_WORDS, replacements=REPLACEMENTS):
    parts = re.split(': ', in_string.upper())
    if len(parts) > 1:
        return ': '.join([titlecase(p, exceptions=exceptions) for p in parts])
    else:
        # XXX: use string.split() instead of re.split?
        words = re.split(' ', parts[0])
        title_words = []
        for n, w in enumerate(words):
            if n < len(words) - 1 and '.' in w.rstrip('.'):
                # Uppercase acronyms
                title_words.append(w.upper())
            elif '-' in w:
                # titlecase (not small) words in hypenated phrase
                w_parts = w.split('-')
                w_fixed = '-'.join([titlecase(p, exceptions=exceptions) for p in w_parts])
                title_words.append(w_fixed)
            elif w in replacements:
                # Replace those exceptional words
                title_words.append(replacements[w])
            elif w not in exceptions and len(w) > 1 and w[0] == '(':
                # Handle parentheticals
                title_words.append(w[0] + w[1:].capitalize())
            elif w[0].isnumeric() or w[-1].isnumeric():
                if w.strip(string.punctuation).lower().endswith(ORDINAL_SUFFIXES):
                    # Lowercase ordinals
                    title_words.append(w.lower())
                else:
                    # Uppercase words with non-ordinals
                    title_words.append(w.upper())
            elif n == 0:
                # Always captialize first word
                title_words.append(w.capitalize())
            else:
                title_words.append(w in exceptions and w.lower() or w.capitalize())
        s = ' '.join(title_words)
        s = re.sub(ROMANS_REG,
                   lambda mo: mo.group().upper(),
                   s, flags=re.I)
        return s


def country_title(in_string):
    return ' '.join(s.lower() not in ('of', 'the') and s.capitalize() or s.lower() for s in in_string.split(' '))
