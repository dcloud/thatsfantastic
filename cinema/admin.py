from django.contrib import admin
from cinema.models import (Film, Person, Screening)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'runtime', 'year', 'slug')
    search_fields = ('title', 'long_description')


admin.site.register(Person)
admin.site.register(Screening)
