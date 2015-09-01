from django.views.generic import ListView, DetailView
from django.views.generic.detail import SingleObjectMixin
from cinema.models import Film, Event


class FilmDetail(DetailView):
    model = Film


class FilmSearch(ListView):
    model = Film

    def get_queryset(self):
        query = self.request.GET.get("q")
        return self.model.objects.filter(title__icontains=query)


class FilmList(ListView):
    model = Film


class EventDetail(SingleObjectMixin, FilmList):
    model = Event

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Event.objects.all())
        return super(EventDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventDetail, self).get_context_data(**kwargs)
        context['event'] = self.object
        return context

    def get_queryset(self):
        return self.object.films.all()
