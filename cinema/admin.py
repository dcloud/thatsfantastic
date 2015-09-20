from django.contrib import admin
from cinema.models import (Film, Person, Screening, Event, Country)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'runtime', 'year', 'slug')
    search_fields = ('title', 'description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'start_day', 'end_day', 'location')
    search_fields = ('title', 'location')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)


admin.site.register(Person)
admin.site.register(Screening)
