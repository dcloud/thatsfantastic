from django.contrib import admin
from cinema.models import Film, Person, Screening, Event, Country


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "runtime", "year", "slug")
    search_fields = ("title", "description")
    list_filter = ["year", "countries", "shown_at__title"]
    filter_horizontal = ["directors", "actors", "countries"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "start_day", "end_day", "location")
    search_fields = ("title", "location")
    filter_horizontal = ("films",)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("last_name", "first_name")


admin.site.register(Screening)
