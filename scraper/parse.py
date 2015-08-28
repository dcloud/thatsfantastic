import lxml.html
from lxml.cssselect import CSSSelector
import re
from scraper.utils import decode_html, unicode_normalize

META_SELECTOR = CSSSelector('header.carousel-caption > h6', translator='html')
ANCHOR_SELECTOR = CSSSelector('ul.thumbnails > li .thumbnail > a:nth-of-type(1)', translator='html')
BODY_TEXT_SELECTOR = CSSSelector('article h4 + p', translator='html')
SYNOPSIS_SELECTOR = CSSSelector('.lead p', translator='html')


class Movie(object):
    """docstring for Movie"""

    attributes = ('title', 'description', 'synopsis', 'directors',
                  'countries', 'runtime', 'year')

    def __init__(self, **kwargs):
        super(Movie, self).__init__()
        for attr in Movie.attributes:
            setattr(self, attr, None)
        self._dictionary = None

    def to_dict(self):
        return {k: self.__dict__[k] for k in Movie.attributes}


class FantasticMovieParser:
    """Parses movie web pages from http://fantasticfest.com/"""
    def __init__(self, raw_html):
        super(FantasticMovieParser, self).__init__()
        self.raw_html = raw_html
        self.movie = Movie()
        for attrname in Movie.attributes:
            attr_iname = '_raw_{}'.format(attrname)
            setattr(self, attr_iname, None)
        self._raw_metadata = None
        self._tree = None

    def _clean_text(self, text):
        return text.strip()

    def _clean_list(self, text):
        return [self._clean_text(x) for x in text.split(',') if x.strip()]

    def _normalize_unicode(self, text):
        return unicode_normalize(text)

    def _clean_and_normalize_unicode(self, text):
        cleaned = self._clean_text(text)
        return self._normalize_unicode(cleaned)

    @property
    def tree(self):
        if self._tree is None:
            self._tree = self.make_tree()
        return self._tree

    def make_tree(self):
        decoded_html = decode_html(self.raw_html)
        return lxml.html.fromstring(decoded_html)

    def parse(self):
        self.clean()
        return self.movie

    def clean(self):
        for attrname in self.movie.__dict__:
            methodname = 'clean_{}'.format(attrname)
            func = getattr(self, methodname, None)
            if callable(func):
                setattr(self.movie, attrname, func())

    @property
    def raw_title(self):
        if self._raw_title is None:
            title_el = self.tree.find('*/title')
            self._raw_title = title_el.text if title_el is not None else ''
        return self._raw_title

    def clean_title(self):
        title = self.raw_title.replace(' | Fantastic Fest', '').title()
        return self._clean_and_normalize_unicode(title)

    @property
    def raw_description(self):
        if self._raw_description is None:
            body_elements = BODY_TEXT_SELECTOR(self.tree)
            self._raw_description = body_elements[0].text_content() if len(body_elements) else ''
        return self._raw_description

    def clean_description(self):
        return self._clean_text(self.raw_description)

    @property
    def raw_synopsis(self):
        if self._raw_synopsis is None:
            body_elements = SYNOPSIS_SELECTOR(self.tree)
            self._raw_synopsis = body_elements[0].text_content() if len(body_elements) else ''
        return self._raw_synopsis

    def clean_synopsis(self):
        return self._clean_text(self.raw_synopsis)

    @property
    def raw_metadata(self):
        '''Unlike other 'raw' properties, `raw_metadata` has had unicode normalization applied.'''
        if self._raw_metadata is None:
            meta_el = META_SELECTOR(self.tree)
            if len(meta_el) > 0:
                el_text = meta_el[0].text_content()
                self._raw_metadata = self._normalize_unicode(el_text)
        return self._raw_metadata

    @property
    def raw_directors(self):
        if self._raw_directors is None:
            match = re.search(r'dir\.\s+([^\d]+)', self.raw_metadata, flags=re.IGNORECASE)
            self._raw_directors = match.groups()[0] if match else ''
        return self._raw_directors

    def clean_directors(self):
        return self._clean_list(self.raw_directors)

    @property
    def raw_countries(self):
        if self._raw_countries is None:
            match = re.search(r'\,\s+(\w[\w\s]+)\s*$', self.raw_metadata, flags=re.IGNORECASE)
            self._raw_countries = match.group() if match else ''
        return self._raw_countries

    def clean_countries(self):
        return self._clean_list(self.raw_countries.title())

    @property
    def raw_year(self):
        if self._raw_year is None:
            match = re.search(r'^\s*\d{4}', self.raw_metadata)
            self._raw_year = match.group() if match else ''
        return self._raw_year

    def clean_year(self):
        return int(self._clean_text(self.raw_year)) if self.raw_year else None

    @property
    def raw_runtime(self):
        if not self._raw_runtime:
            match = re.search(r'(\d{1,})\s+MIN\.', self.raw_metadata, flags=re.IGNORECASE)
            self._raw_runtime = match.groups()[0] if match else ''
        return self._raw_runtime

    def clean_runtime(self):
        return int(self._clean_text(self.raw_runtime)) if self.raw_runtime else None
