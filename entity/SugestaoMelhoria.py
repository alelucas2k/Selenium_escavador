class SugestaoMelhoria:
    def __init__(self, data_sugestao, sugestao):
        self._id = None
        self._data_sugestao = data_sugestao
        self._sugestao = sugestao

    # Getters
    @property
    def id(self):
        return self._id

    @property
    def data_sugestao(self):
        return self._data_sugestao

    @property
    def sugestao(self):
        return self._sugestao

    # Setters
    @id.setter
    def id(self, value):
        self._id = value

    @data_sugestao.setter
    def data_sugestao(self, value):
        self._data_sugestao = value

    @sugestao.setter
    def sugestao(self, value):
        self._sugestao = value

