from django.views.generic import ListView, DetailView
from films.models import Film


class FilmDetailView(DetailView):
    model = Film


class FilmSearchView(ListView):
    model = Film

    def get_queryset(self):
        query = self.request.REQUEST.get("q")
        return self.model.objects.filter(title__icontains=query)


class FilmListView(ListView):
    model = Film
