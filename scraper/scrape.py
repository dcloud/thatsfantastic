import lxml.html
from lxml.cssselect import CSSSelector
import re
from scraper.models import FilmDict
from scraper.utils import (decode_html, unicode_normalize,
                           clean_string, string_to_list, replace_countries)
from cinema.utils import (titlecase,)

META_SELECTOR = CSSSelector('header.carousel-caption > h6', translator='html')
ANCHOR_SELECTOR = CSSSelector('ul.thumbnails > li .thumbnail > a:nth-of-type(1)', translator='html')
SYNOPSIS_GRAPHS_XPATH = "//div[@class='lead']/p"
DESCRIPTION_GRAPHS_XPATH = '//article/h4[2]/following-sibling::p'


class HTMLScraper:
    """docstring for HTMLScraper"""
    def __init__(self, raw_html, source_url=None):
        super(HTMLScraper, self).__init__()
        self.source_url = source_url
        self.raw_html = raw_html
        self._tree = None

    @property
    def tree(self):
        if self._tree is None:
            self._tree = self.make_tree()
        return self._tree

    def make_tree(self):
        decoded_html = decode_html(self.raw_html)
        return lxml.html.fromstring(decoded_html)

    def scrape(self):
        raise NotImplementedError('Subclasses must implement scraping of raw_html')


class FantasticMovieListScraper(HTMLScraper):
    """Scrapes a film list page for links to film pages."""
    def __init__(self, raw_html, source_url=None):
        super(FantasticMovieListScraper, self).__init__(raw_html, source_url=source_url)
        self.anchor_list = []

    def get_film_page_urls(self):
        anchor_els = ANCHOR_SELECTOR(self.tree)
        self.anchor_list = list(a.attrib.get('href', None) for a in anchor_els)
        self.anchor_list = filter(lambda x: 'secret-screening' not in x, self.anchor_list)
        return self.anchor_list

    def scrape(self):
        self.get_film_page_urls()
        return self.anchor_list


class FantasticMovieScraper(HTMLScraper):
    """Scrapes film web pages from http://fantasticfest.com/"""
    def __init__(self, raw_html, source_url=None):
        super(FantasticMovieScraper, self).__init__(raw_html, source_url=source_url)
        self.film = FilmDict()
        if self.source_url:
            self.film['meta'] = {
                'source_url': self.source_url,
            }
        for attrname in FilmDict.attributes:
            attr_iname = '_raw_{}'.format(attrname)
            setattr(self, attr_iname, None)
        self._raw_metadata = None
        self._end_directors = self._end_runtime = None

    def _clean_string(self, string):
        return clean_string(string)

    def _clean_list(self, string):
        return string_to_list(string)

    def _normalize_unicode(self, string):
        return unicode_normalize(string)

    def _clean_and_normalize_unicode(self, text):
        cleaned = self._clean_string(text)
        return self._normalize_unicode(cleaned)

    def _raw_graphs_to_string(self, graphs_list):
        return '\n\n'.join(g.text_content().strip('\n') for g in graphs_list) if len(graphs_list) else ''

    def scrape(self):
        self._scrape_raw()
        return self.clean()

    def _scrape_raw(self):
        for attrname in FilmDict.attributes:
            methodname = 'raw_{}'.format(attrname)
            func = getattr(self, methodname, None)
            if callable(func):
                setattr(self.film, attrname, func())

    def clean(self):
        for attrname in FilmDict.attributes:
            methodname = 'clean_{}'.format(attrname)
            func = getattr(self, methodname, None)
            if callable(func):
                setattr(self.film, attrname, func())
        return self.film

    @property
    def raw_title(self):
        if self._raw_title is None:
            title_el = self.tree.find('*/title')
            self._raw_title = title_el.text if title_el is not None else ''
        return self._raw_title

    def clean_title(self):
        title = self.raw_title.replace(' | Fantastic Fest', '').title()
        title = self._clean_and_normalize_unicode(title)
        return titlecase(title)

    @property
    def raw_description(self):
        if self._raw_description is None:
            graphs = self.tree.xpath(DESCRIPTION_GRAPHS_XPATH)
            self._raw_description = self._raw_graphs_to_string(graphs)
        return self._raw_description

    def clean_description(self):
        return self._clean_string(self.raw_description)

    @property
    def raw_synopsis(self):
        if self._raw_synopsis is None:
            graphs = self.tree.xpath(SYNOPSIS_GRAPHS_XPATH)
            self._raw_synopsis = self._raw_graphs_to_string(graphs)
        return self._raw_synopsis

    def clean_synopsis(self):
        return self._clean_string(self.raw_synopsis)

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
            self._end_directors = match.end()
            self._raw_directors = match.groups()[0] if match else ''
        return self._raw_directors

    def clean_directors(self):
        return self._clean_list(self.raw_directors)

    @property
    def raw_countries(self):
        if self._raw_countries is None:
            search_text = self.raw_metadata
            if self._end_runtime:
                search_text = search_text[self._end_runtime:]
            elif self._end_directors:
                search_text = search_text[self._end_directors:]
            match_list = re.findall(r'(?:\,\s+(\w[\w\s]+)+)', search_text, flags=re.IGNORECASE)
            self._raw_countries = match_list
        return self._raw_countries

    def clean_countries(self):
        return [self._clean_string(c.title()) for c in replace_countries(self._raw_countries)]

    @property
    def raw_year(self):
        if self._raw_year is None:
            match = re.search(r'^\s*\d{4}', self.raw_metadata)
            self._raw_year = match.group() if match else ''
        return self._raw_year

    def clean_year(self):
        return int(self._clean_string(self.raw_year)) if self.raw_year else None

    @property
    def raw_runtime(self):
        if not self._raw_runtime:
            match = re.search(r'(\d{1,})\s+MIN\.', self.raw_metadata, flags=re.IGNORECASE)
            self._end_runtime = match.end()
            self._raw_runtime = match.groups()[0] if match else ''
        return self._raw_runtime

    def clean_runtime(self):
        return int(self._clean_string(self.raw_runtime)) if self.raw_runtime else None
