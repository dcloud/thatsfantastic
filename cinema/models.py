from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.core.urlresolvers import reverse


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
    countries = ArrayField(models.CharField(max_length=60),
                           default=list, blank=True,
                           help_text=_('Country names, not standardized'))
    languages = ArrayField(models.CharField(max_length=30), default=list, blank=True)
    year = models.PositiveIntegerField(blank=True, null=True, help_text=_("Release year"))
    runtime = models.IntegerField(blank=True, null=True, help_text=_("Film runtime, in whole minutes"))
    directors = models.ManyToManyField('Person', related_name='directed', blank=True,
                                       help_text=_("Usually one person, but can accomodate multiple directors"))
    actors = models.ManyToManyField('Person', related_name='acted_in', blank=True)
    related_urls = ArrayField(models.URLField(), default=list, blank=True)

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        ordering = ('title', '-year')

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            title_str = self.title
            if len(self.title) > 140:
                title_str = title_str[:140]
            self.slug = slugify(title_str)
        super(Film, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('film-detail', kwargs={'slug': str(self.slug)})

    def __unicode__(self):
        return '{title} [{year}]'.format(title=self.title, year=self.year)

    def __str__(self):
        return self.__unicode__()


class Screening(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    film = models.ForeignKey('Film')
    location = models.CharField(blank=True, default='', max_length=120,
                                help_text=_("Location of film screening"))
    event = models.ForeignKey('Event')

    class Meta:
        verbose_name = _('Screening')
        verbose_name_plural = _('Screenings')
        get_latest_by = 'start_time'

    def __unicode__(self):
        return '{title}: {start}-{end}'.format(title=self.film.title, start=self.start_time, end=self.end_time)

    def __str__(self):
        return self.__unicode__()


class Event(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    location = models.CharField(blank=True, default='', max_length=50,
                                help_text=_("Geographic location of event, i.e. Austin, Texas"))
    films = models.ManyToManyField('Film', related_name='shown_at')

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ('-start_date', '-end_date', 'title')
        get_latest_by = 'start_date'

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            title_str = self.title
            if len(self.title) > 140:
                title_str = title_str[:140]
            self.slug = slugify(title_str)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('film-event-detail', kwargs={'slug': str(self.slug)})

    def __unicode__(self):
        subinfo = ''
        if self.start_date and self.end_date:
            time_format = '%x'
            subinfo = '{} - {}'.format(self.start_date.strftime(time_format),
                                       self.end_date.strftime(time_format))
        elif self.location:
            subinfo = '({})'.format(self.location)
        return '{title}: {subinfo}'.format(title=self.title, subinfo=subinfo)

    def __str__(self):
        return self.__unicode__()


class Country(models.Model):
    """Model that is actually backed by a PostgreSQL view based on the Film model's countries"""
    name = models.CharField(max_length=60, primary_key=True)

    class Meta:
        db_table = "cinema_country"
        managed = False
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    @property
    def slug(self):
        return slugify(self.name)

    def get_absolute_url(self):
        return reverse('film-event-detail', kwargs={'slug': str(self.slug)})

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()
