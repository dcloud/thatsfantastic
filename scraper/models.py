

class Movie:
    """docstring for Movie"""

    attributes = ('title', 'description', 'synopsis', 'directors',
                  'countries', 'runtime', 'year')

    def __init__(self, **kwargs):
        super(Movie, self).__init__()
        for attr in Movie.attributes:
            setattr(self, attr, None)
        self._dictionary = None

    def to_dict(self):
        return {k: self.__dict__[k] for k in Movie.attributes}
