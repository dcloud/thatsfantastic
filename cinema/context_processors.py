from .models import Event


def cinema(request):
    return {
        'cinema': {
            'events': Event.objects.all()
        }
    }
