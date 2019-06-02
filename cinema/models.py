from django.db import models
from django.utils.translation import ugettext as _
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(blank=True, max_length=50, default="")
    last_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("People")

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        middle_str = " {0}".format(self.middle_name) if self.middle_name != "" else ""
        return "{first}{middle} {last}".format(
            first=self.first_name, middle=middle_str, last=self.last_name
        )


class Film(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    synopsis = models.TextField(blank=True)
    description = models.TextField(blank=True)
    countries = models.ManyToManyField("Country")
    languages = ArrayField(models.CharField(max_length=30), default=list, blank=True)
    year = models.PositiveIntegerField(
        blank=True, null=True, help_text=_("Release year")
    )
    runtime = models.IntegerField(
        blank=True, null=True, help_text=_("Film runtime, in whole minutes")
    )
    directors = models.ManyToManyField(
        "Person",
        related_name="directed",
        blank=True,
        help_text=_("Usually one person, but can accomodate multiple directors"),
    )
    actors = models.ManyToManyField("Person", related_name="acted_in", blank=True)
    related_urls = ArrayField(models.URLField(), default=list, blank=True)

    class Meta:
        verbose_name = _("Film")
        verbose_name_plural = _("Films")
        ordering = ("title", "-year")

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            title_str = self.title
            if len(self.title) > 140:
                title_str = title_str[:140]
            self.slug = slugify(title_str)
        super(Film, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cinema:film-detail", kwargs={"slug": str(self.slug)})

    def __str__(self):
        return "{title} [{year}]".format(title=self.title, year=self.year)


class Screening(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    film = models.ForeignKey("Film", on_delete=models.CASCADE)
    location = models.CharField(
        blank=True,
        default="",
        max_length=120,
        help_text=_("Location of film screening"),
    )
    event = models.ForeignKey("Event", on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = _("Screening")
        verbose_name_plural = _("Screenings")
        get_latest_by = "start_time"

    def __str__(self):
        return "{title}: {start}-{end}".format(
            title=self.film.title, start=self.start_time, end=self.end_time
        )


class Event(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    start_day = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_day = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    location = models.CharField(
        blank=True,
        default="",
        max_length=50,
        help_text=_("Geographic location of event, i.e. Austin, Texas, USA"),
    )
    films = models.ManyToManyField("Film", related_name="shown_at", blank=True)

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("-start_day", "-end_day", "title")
        get_latest_by = "start_day"

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            title_str = self.title
            if len(self.title) > 140:
                title_str = title_str[:140]
            self.slug = slugify(title_str)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cinema:film-event-detail", kwargs={"slug": str(self.slug)})

    def __str__(self):
        subinfo = ""
        if self.start_day and self.end_day:
            time_format = "%x"
            subinfo = "{} - {}".format(
                self.start_day.strftime(time_format), self.end_day.strftime(time_format)
            )
        elif self.location:
            subinfo = "({})".format(self.location)
        return "{title}: {subinfo}".format(title=self.title, subinfo=subinfo)


class Country(models.Model):
    """Non-standardized country names, for films"""

    name = models.CharField(max_length=60, primary_key=True)
    slug = models.SlugField(max_length=65, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("cinema:films-from-country", kwargs={"slug": str(self.slug)})

    def __str__(self):
        return self.name
