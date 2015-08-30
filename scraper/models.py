

class Film:
    """docstring for Film"""

    attributes = ('title', 'description', 'synopsis', 'directors',
                  'countries', 'runtime', 'year')

    def __init__(self, **kwargs):
        super(Film, self).__init__()
        for attr in Film.attributes:
            setattr(self, attr, None)
        self._dictionary = None

    def to_dict(self):
        return {k: self.__dict__[k] for k in Film.attributes}
