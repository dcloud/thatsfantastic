import factory
import factory.django
import factory.fuzzy
import unicodedata

from cinema.models import Film, Person
from django_countries import countries

COUNTRY_VALUES = (x[0] for x in countries)


def make_unicode_letters():
    def generate_unicode_letters(characters):
        for c in characters:
            cat = unicodedata.category(c)
            if cat == 'Ll' or cat == 'Lu':
                yield c

    uni_chars = (chr(i) for i in range(65536))
    uni_letters = generate_unicode_letters(uni_chars)
    return ''.join(uni_letters)

unicode_letters = make_unicode_letters()


class FuzzyList(factory.fuzzy.BaseFuzzyAttribute):
    """FuzzyList provides a list of values generated using another fuzzy attribute"""

    def __init__(self, fuzzy_attribute, max_len, min_len=1, **kwargs):
        self.fuzzy_attribute = fuzzy_attribute
        self.min_len = min_len
        self.max_len = max_len
        super(FuzzyList, self).__init__(**kwargs)

    def fuzz(self):
        num_choices = factory.fuzzy._random.randrange(self.min_len, self.max_len)
        return list(self.fuzzy_attribute.fuzz() for f in range(num_choices))


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person
    first_name = factory.fuzzy.FuzzyText(chars=unicode_letters)
    middle_name = factory.fuzzy.FuzzyText(chars=unicode_letters)
    last_name = factory.fuzzy.FuzzyText(chars=unicode_letters)


class FilmFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Film

    title = factory.fuzzy.FuzzyText(length=40, chars=unicode_letters)
    synopsis = factory.fuzzy.FuzzyText()
    description = factory.fuzzy.FuzzyText()
    countries = FuzzyList(factory.fuzzy.FuzzyChoice(COUNTRY_VALUES), 5)

    @factory.post_generation
    def directors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for director in extracted:
                self.directors.add(director)

    @factory.post_generation
    def actors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for actor in extracted:
                self.actors.add(actor)
