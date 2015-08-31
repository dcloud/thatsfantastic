from django.contrib import admin
from cinema.models import (Film, Person, Screening, Event)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'runtime', 'year', 'slug')
    search_fields = ('title', 'long_description')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'start_date', 'end_date', 'location')
    search_fields = ('title', 'location')


admin.site.register(Person)
admin.site.register(Screening)
