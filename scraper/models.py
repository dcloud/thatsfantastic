from collections import UserDict


class FilmDict(UserDict):
    """FilmDict is a dictionary with a default set of keys/attributes.
       Each key/attribute is initialized to None if a value isn't provided.
       Values for key/attribute may be set/retrieved using object attribute notation."""

    attributes = ('title', 'description', 'synopsis', 'directors',
                  'countries', 'runtime', 'year')

    def __init__(self, initialdata=None, **elements):
        super(FilmDict, self).__init__(initialdata)
        for key in FilmDict.attributes:
            if key not in self:
                self[key] = None

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("Film instance has no attribute/key '{}'".format(name))

    def __setattr__(self, name, value):
        if name in FilmDict.attributes:
            self[name] = value
        elif name is 'data':
            super(FilmDict, self).__setattr__(name, value)
        else:
            raise AttributeError("Only keys from FilmDict.attributes may be set using attribute notation.")
