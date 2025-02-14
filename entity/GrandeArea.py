class GrandeArea:
    def __init__(self, id, area):
        self._id = id
        self._area = area


    # Getters
    @property
    def id(self):
        return self._id

    @property
    def area(self):
        return self._area

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @area.setter
    def area(self, value):
        self._area = value
