from django.contrib import admin
from django.utils.translation import ugettext as _
from cinema.models import Film, Person, Screening, Event, Country
from datetime import datetime


class DecadeListFilter(admin.SimpleListFilter):
    title = _("Decade")

    parameter_name = "decade"

    def lookups(self, request, model_admin):
        today = datetime.today()
        decades = range(1900, today.year + 1, 10)
        return ((f"{d}s", f"{d}s") for d in decades)

    def queryset(self, request, queryset):
        decade_value = self.value()[:-1] if self.value() else None
        if decade_value:
            try:
                decade = int(decade_value)
                return queryset.filter(year__gte=decade, year__lt=decade + 10)
            except Exception:
                return queryset.none()


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "runtime", "year", "slug")
    search_fields = ("title", "description")
    list_filter = [DecadeListFilter, "countries", "shown_at__title"]
    filter_horizontal = ["directors", "actors", "countries"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "start_day", "end_day", "location")
    search_fields = ("title", "location")
    filter_horizontal = ("films",)
    date_hierarchy = "start_day"


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("last_name", "first_name")


admin.site.register(Screening)
