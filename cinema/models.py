from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django_countries import countries
from django.core.urlresolvers import reverse

COUNTRY_CODES = tuple(countries)


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, max_length=50, default='')
    last_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')

    def __unicode__(self):
        return self.full_name

    def __str__(self):
        return self.__unicode__()

    @property
    def full_name(self):
        middle_str = ' {0}'.format(self.middle_name) if self.middle_name != '' else ''
        return '{first}{middle} {last}'.format(first=self.first_name,
                                               middle=middle_str,
                                               last=self.last_name)


class Film(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    synopsis = models.TextField(blank=True)
    description = models.TextField(blank=True)
    countries = ArrayField(models.CharField(choices=COUNTRY_CODES, max_length=2), default=list)
    languages = ArrayField(models.CharField(max_length=30), default=list)
    year = models.PositiveIntegerField(blank=True, null=True, help_text=_("Release year"))
    runtime = models.IntegerField(blank=True, null=True, help_text=_("Film runtime, in whole minutes"))
    directors = models.ManyToManyField('Person', related_name='directed',
                                       help_text=_("Usually one person, but can accomodate multiple directors"))
    actors = models.ManyToManyField('Person', related_name='acted_in')

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        ordering = ('title',)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            title_str = self.title
            if len(self.title) > 140:
                title_str = title_str[:140]
            self.slug = slugify(title_str)
        super(Film, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{title} [{year}]'.format(title=self.title, year=self.year)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return reverse('film-detail', kwargs={'slug': str(self.slug)})


class Screening(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    film = models.ForeignKey('Film')
    location = models.CharField(blank=True, default='', max_length=120,
                                help_text=_("Location of film screening"))

    class Meta:
        verbose_name = _('Screening')
        verbose_name_plural = _('Screenings')

    def __unicode__(self):
        '{title}: {start}-{end}'.format(title=self.film.title, start=self.start_time, end=self.end_time)

    def __str__(self):
        return self.__unicode__()
